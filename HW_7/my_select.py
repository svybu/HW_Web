from sqlalchemy import func, create_engine
from sqlalchemy.orm import sessionmaker
from model import Group, Grade, Student, Subject, Teacher
from seed import url

engine = create_engine(url)
Session = sessionmaker(bind=engine)
session = Session()

def select_1():
    top_students = (
        session.query(
            Student.id,
            Student.name,
            func.avg(Grade.grade).label('avg_grade')
        )
        .join(Grade)
        .group_by(Student.id, Student.name)
        .order_by(func.avg(Grade.grade).desc())
        .limit(5)
        .all()
    )
    for student in top_students:
        print(f"{student.name}: {student.avg_grade}")

def select_2(subject_name):
    top_student = (
        session.query(
            Student.id,
            Student.name,
            func.avg(Grade.grade).label('avg_grade')
        )
        .join(Grade)
        .join(Subject)
        .filter(Subject.name == subject_name)
        .group_by(Student.id, Student.name)
        .order_by(func.avg(Grade.grade).desc())
        .limit(1)
        .all()
    )
    if top_student:
        student_id, student_name, avg_grade = top_student[0]
        print(
            f"Студент з найвищим середнім балом за предмет '{subject_name}': {student_name}, середній бал {avg_grade}")
    else:
        print(f"Предмет з назвою '{subject_name}' не знайдено.")

def select_3(subject_name):
    top_groups = (
        session.query(
            Group.name,
            func.avg(Grade.grade).label('avg_grade')
        )
        .join(Student, Student.group_id == Group.id)
        .join(Grade, Grade.student_id == Student.id)
        .join(Subject, Subject.id == Grade.subject_id)
        .filter(Subject.name == subject_name)
        .group_by(Group.name)
        .order_by(func.avg(Grade.grade).desc())
        .all()
    )
    for group in top_groups:
        print(f"{group.name}: {group.avg_grade}")

def select_4():
    avg_grade = (
        session.query(
            func.avg(Grade.grade).label('avg_grade')
        )
        .first()
    )
    print(f"{avg_grade}")

def select_5(teacher_name):
    subjects = (
        session.query(
            Subject.name
        )
        .join(Teacher, Teacher.id == Subject.teacher_id)
        .filter(Teacher.name==teacher_name)
        .all()
    )
    for subject in subjects:
        print(f"{subject}")

def select_6(group_name):
    students = (
        session.query(
            Student.name
        )
        .join(Group, Group.id == Student.group_id)
        .filter(Group.name==group_name)
        .all()
    )
    for student in students:
        print(f"{student}")

def select_7(group_name, subject_name):
    students = (
        session.query(
            Grade.grade
        )
        .join(Student, Student.id == Grade.student_id)
        .join(Group, Group.id == Student.group_id)
        .join(Subject, Subject.id == Grade.subject_id)
        .filter(Subject.name==subject_name)
        .filter(Group.name==group_name)
        .all()
    )
    for student in students:
        print(f"{student}")

def select_8(teacher_name):
    grade = (
        session.query(
            func.avg(Grade.grade).label('avg_grade')
        )
        .join(Teacher, Teacher.id == Grade.subject_id)
        .join(Subject, Subject.id == Grade.subject_id)
        .filter(Teacher.name==teacher_name)
        .all()
    )
    print(f"{grade}")

def select_9(student_name):
    subjects = (
        session.query(
            Subject.name
        )
        .join(Grade, Subject.id == Grade.subject_id)
        .join(Student, Student.id == Grade.student_id)
        .filter(Student.name==student_name)
        .all()
    )
    for subject in subjects:
        print(f"{subject}")

def select_10(student_name, teacher_name):
    subjects = (
        session.query(
            Subject.name
        )
        .join(Grade, Subject.id == Grade.subject_id)
        .join(Student, Student.id == Grade.student_id)
        .join(Teacher, Teacher.id == Subject.teacher_id)
        .filter(Student.name==student_name)
        .filter(Teacher.name == teacher_name)
        .all()
    )
    for subject in subjects:
        print(f"{subject}")

def select_11(student_name, teacher_name):
    avg_grade = (
        session.query(
            func.avg(Grade.grade).label('avg_grade')
        )
        .join(Student, Student.id == Grade.student_id)
        .join(Subject, Subject.id == Grade.subject_id)
        .join(Teacher, Teacher.id == Subject.teacher_id)
        .filter(Student.name==student_name)
        .filter(Teacher.name == teacher_name)
        .all()
    )
    print(f"{avg_grade}")

def select_12(group_name, subject_name):
    last_date_received = (
        session.query(func.max(Grade.date_received))
        .join(Student)
        .join(Group)
        .join(Subject, Student.group_id == Group.id)
        .filter(Group.name == group_name)
        .filter(Subject.name == subject_name)
        .scalar()
    )

    results = (
        session.query(Student.name, Grade.grade, Grade.date_received)
        .select_from(Student)
        .join(Group)
        .join(Subject, Student.group_id == Group.id)
        .join(Grade)
        .filter(Group.name == group_name)
        .filter(Subject.name == subject_name)
        .filter(Grade.date_received == last_date_received)
        .all()
    )

    for result in results:
        print(result)


select_12('former Group', 'agree')





