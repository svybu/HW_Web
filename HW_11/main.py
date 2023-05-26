from fastapi import FastAPI, Depends, HTTPException, Security, Response, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel
from starlette import status
from starlette.responses import JSONResponse

from database.db import get_db
from database.models import User, Contact
from shemas import ContactCreate, ContactUpdate
from auth import create_access_token, create_refresh_token, get_email_form_refresh_token, get_current_user, Hash

app = FastAPI()

app = FastAPI()
hash_handler = Hash()
security = HTTPBearer()


class UserModel(BaseModel):
    username: str
    password: str


# Аутентифікація та отримання JWT токена
from passlib.context import CryptContext

# Створення об'єкту CryptContext для хешування паролів
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@app.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(body: UserModel, db: Session = Depends(get_db)):
    exist_user = db.query(User).filter(User.email == body.username).first()
    if exist_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Account already exists")

    hashed_password = pwd_context.hash(body.password)
    new_user = User(email=body.username, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return JSONResponse(content={"new_user": new_user.email}, status_code=status.HTTP_201_CREATED)


@app.post("/login")
async def login(body: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == body.username).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email")
    if not hash_handler.verify_password(body.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password")
    # Generate JWT
    access_token = await create_access_token(data={"sub": user.email})
    refresh_token = await create_refresh_token(data={"sub": user.email})
    user.refresh_token = refresh_token
    db.commit()
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@app.get('/refresh_token')
async def refresh_token(credentials: HTTPAuthorizationCredentials = Security(security), db: Session = Depends(get_db)):
    token = credentials.credentials
    email = await get_email_form_refresh_token(token)
    user = db.query(User).filter(User.email == email).first()
    if user.refresh_token != token:
        user.refresh_token = None
        db.commit()
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

    access_token = await create_access_token(data={"sub": email})
    refresh_token = await create_refresh_token(data={"sub": email})
    user.refresh_token = refresh_token
    db.commit()
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/secret")
async def read_item(current_user: User = Depends(get_current_user)):
    return {"message": 'secret router', "owner": current_user.email}


# Маршрут для створення нового контакту (доступ обмежений)
@app.post("/contacts/")
async def create_contact(
        contact: ContactCreate,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    db_contact = Contact(
        first_name=contact.first_name,
        last_name=contact.last_name,
        email=contact.email,
        phone_number=contact.phone_number,
        date_of_birth=contact.date_of_birth,
        user_id=current_user.id
    )
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact


# Маршрут для отримання списку всіх контактів (доступ обмежений)
@app.get("/contacts/")
async def get_contacts(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    contacts = db.query(Contact).filter(Contact.user_id == current_user.id).all()
    return {"contacts": contacts}


# Маршрут для отримання інформації про окремий контакт (доступ обмежений)
@app.get("/contacts/{contact_id}")
async def get_contact(
        contact_id: int,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    contact = db.query(Contact).filter(Contact.id == contact_id, Contact.user_id == current_user.id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact


# Маршрут для оновлення контакту (доступ обмежений)
@app.put("/contacts/{contact_id}")
async def update_contact(
        contact_id: int,
        contact: ContactUpdate,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    db_contact = db.query(Contact).filter(Contact.id == contact_id, Contact.user_id == current_user.id).first()
    if not db_contact:
        raise HTTPException(status_code=404, detail="Contact not found")

    db_contact.first_name = contact.first_name
    db_contact.last_name = contact.last_name
    db_contact.email = contact.email
    db_contact.phone_number = contact.phone_number
    db_contact.date_of_birth = contact.date_of_birth

    db.commit()
    db.refresh(db_contact)
    return db_contact


# Маршрут для видалення контакту (доступ обмежений)
@app.delete("/contacts/{contact_id}")
async def delete_contact(
        contact_id: int,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    db_contact = db.query(Contact).filter(Contact.id == contact_id, Contact.user_id == current_user.id).first()
    if not db_contact:
        raise HTTPException(status_code=404, detail="Contact not found")

    db.delete(db_contact)
    db.commit()
    return {"message": "Contact deleted successfully"}
