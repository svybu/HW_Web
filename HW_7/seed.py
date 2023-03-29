from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from faker import Faker
from model import Group, Grade, Student, Subject, Teacher

host = 'localhost'
port = '5432'
database = 'postgres'
user = 'postgres'
password = '1234'

url = f'postgresql://{user}:{password}@{host}:{port}/{database}'
engine = create_engine(url)
Session = sessionmaker(bind=engine)

class Test_inf():
    def __init__(self):
        self.fake = Faker()
        self.engine = engine
        self.session = Session()

    def add_groups(self, num_records=30):
        for i in range(num_records):
            name = self.fake.word() + ' Group'
            group = Group(name=name)
            self.session.add(group)
        self.session.commit()
        print(f'{num_records} записів додано до таблиці groups')

    def add_students(self, num_records=30):
        for i in range(num_records):
            name = self.fake.name()
            group_id = self.fake.random_int(1, 10)
            student = Student(name=name, group_id=group_id)
            self.session.add(student)
        self.session.commit()
        print(f'{num_records} записів додано до таблиці students')

    def add_teachers(self, num_records=30):
        for i in range(num_records):
            name = self.fake.name()
            teacher = Teacher(name=name)
            self.session.add(teacher)
        self.session.commit()
        print(f'{num_records} записів додано до таблиці teachers')

    def add_subjects(self, num_records=30):
        for i in range(num_records):
            name = self.fake.word()
            teacher_id = self.fake.random_int(1, 10)
            subject = Subject(name=name, teacher_id=teacher_id)
            self.session.add(subject)
        self.session.commit()
        print(f'{num_records} записів додано до таблиці subjects')

    def add_grades(self, num_records=30):
        for i in range(num_records):
            student_id = self.fake.random_int(1, 30)
            subject_id = self.fake.random_int(1, 30)
            grade = self.fake.random_int(1, 100)
            date_received = self.fake.date_between(start_date='-1y', end_date='today')
            grade = Grade(student_id=student_id, subject_id=subject_id, grade=grade, date_received=date_received)
            self.session.add(grade)
        self.session.commit()
        print(f'{num_records} записів додано до таблиці grades')

    def add_all(self):
        self.add_groups()
        self.add_students()
        self.add_teachers()
        self.add_subjects()
        self.add_grades()


test = Test_inf()
test.add_all()