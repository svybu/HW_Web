from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from migrations.db import get_db, Base, Contact
from shemas import ContactBase, ContactCreate, ContactCreate, ContactUpdate, ContactResponse, ContactListResponse
from datetime import date, timedelta

# Модель для отримання та створення контакту


app = FastAPI()


@app.get("/api/healthchecker")
async def root():
    return {"message": "Welcome to FastAPI!"}


# Маршрут для створення нового контакту
@app.post("/contacts/")
async def create_contact(contact: ContactCreate, db: Session = Depends(get_db)):
    db_contact = Contact(
        first_name=contact.first_name,
        last_name=contact.last_name,
        email=contact.email,
        phone_number=contact.phone_number,
        date_of_birth=contact.date_of_birth,
    )
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact


# Маршрут для отримання списку всіх контактів
@app.get("/contacts/")
async def get_contacts(db: Session = Depends(get_db)):
    contacts = db.query(Contact).all()
    return contacts


# Маршрут для отримання інформації про окремий контакт
@app.get("/contacts/{contact_id}")
async def get_contacts(
        search: str = Query(None, description="Search contacts by name, last name, or email"),
        db: Session = Depends(get_db),
):
    query = db.query(Contact)
    if search:
        query = query.filter(
            Contact.first_name.ilike(f"%{search}%")
            | Contact.last_name.ilike(f"%{search}%")
            | Contact.email.ilike(f"%{search}%")
        )
    contacts = query.all()
    return contacts


@app.put("/contacts/{contact_id}")
async def update_contact(contact_id: int, contact: ContactCreate, db: Session = Depends(get_db)):
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
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


# Видалення контакту
@app.delete("/contacts/{contact_id}")
async def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if not db_contact:
        raise HTTPException(status_code=404, detail="Contact not found")

    db.delete(db_contact)
    db.commit()
    return {"message": "Contact deleted successfully"}


@app.get("/contacts/birthdays/")
async def get_upcoming_birthdays(db: Session = Depends(get_db)):
    today = date.today()
    end_date = today + timedelta(days=7)
    query = db.query(Contact).filter(
        Contact.date_of_birth.between(today, end_date)
    )
    upcoming_birthdays = query.all()
    return upcoming_birthdays
