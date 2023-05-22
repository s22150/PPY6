from typing import List
from enum import Enum
import smtplib
from email.mime.text import MIMEText


class Status(Enum):
    NO_STATUS = 'NO_STATUS'
    GRADED = 'GRADED'
    MAILED = 'MAILED'
    GRADED_AND_MAILED = 'GRADED_AND_MAILED'


class Student:
    def __init__(self, email: str, first_name: str, last_name: str, points: List[int], grade: float):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.points = points
        self.grade = grade
        self.statusEnum = Status.NO_STATUS

    def __repr__(self):
        return f'Student(email={self.email}, name={self.first_name} {self.last_name}, points={self.points}, grade={self.grade}, status={self.statusEnum.value})'


class MySortedList:
    def __init__(self, max_size):
        self.max_size = max_size
        self.data = []

    def insert(self, value):
        self.data.append(value)
        self.data.sort(reverse=True, key=lambda student: student.grade)
        if len(self.data) > self.max_size:
            self.data.pop()

    def __len__(self):
        return len(self.data)

    def __iter__(self):
        return iter(self.data)


def read_file(filename: str) -> List[Student]:
    students = []
    with open(filename, 'r') as file:
        for line in file:
            fields = line.strip().split(',')

            if len(fields) == 19:
                student = Student(fields[0], fields[1], fields[2], [int(x) for x in fields[3:16]], float(fields[17]))
                status_str = fields[18]
                set_status(status_str, student)
            else:
                continue
            students.append(student)

    return students


def grade_students(students: List[Student]):
    for student in students:
        if student.statusEnum not in [Status.GRADED, Status.MAILED, Status.GRADED_AND_MAILED] and -1 not in student.points:
            points = student.points
            project_grade = points[0]
            lists_grades = points[1:4]
            hw_grade = sum(points[4:14])/10
            list_grade = sum(lists_grades)

            if hw_grade > 80:
                list_grade = 60
            elif hw_grade > 70:
                lists_grades.sort()
                lists_grades[0] = 20
                lists_grades[1] = 20
                list_grade = sum(lists_grades)
            elif hw_grade > 60:
                lists_grades.sort()
                lists_grades[0] = 20
                list_grade = sum(lists_grades)

            student.grade = (project_grade + list_grade)*5/100

            student.status = Status.GRADED
            log_message(f"Graded student with email {student.email} and assigned grade {student.grade}.")


def delete_student(students: List[Student]):
    email = input("Podaj adres email studenta, którego chcesz usunąć: ")
    emails = [student.email for student in students]
    if email in emails:
        for student in students:
            if email == student.email:
                students.remove(student)
                break

        print(f"Usunięto studenta o adresie email {email}")
        log_message(f"Deleted student with email {email}.")
    else:
        print(f"Nie znaleziono studenta o adresie email {email}")
        log_message(f"Could not find student with email {email} to delete.")


def add_student(students: List[Student]):
    email = input("Podaj adres email studenta: ")
    emails = [student.email for student in students]
    if email in emails:
        print(f"Student o adresie email {email} już istnieje")
        log_message(f"Failed to add new student with email {email} because this email already exists.")
        return
    first_name = input("Podaj imię studenta: ")
    last_name = input("Podaj nazwisko studenta: ")
    points = input("Podaj liczbę punktów: ")
    status = input("Podaj status: ").upper()
    s1 = Student(email=email, first_name=first_name, last_name=last_name,
                 points=[int(p) for p in points.split(",")], grade=-1)
    set_status(status, s1)
    students.append(s1)
    print(f"Dodano studenta {first_name} {last_name} z adresem email {email}")
    log_message(f"Added new student with email {email}, first name {first_name}, last name {last_name}, and points {points}.")


def set_status(status_str, student):
    if status_str.__contains__(Status.GRADED.value) and status_str.__contains__(Status.MAILED.value):
        student.statusEnum = Status.GRADED_AND_MAILED
    elif status_str.__contains__(Status.GRADED.value):
        student.statusEnum = Status.GRADED
    elif status_str.__contains__(Status.MAILED.value):
        student.statusEnum = Status.MAILED


def print_students(students: List[Student]):
    for s in students:
        print(s)
    log_message(f"Printed all students data.")


def send_email(students: List[Student]):
    for student in students:
        if 'GRADED' in student.statusEnum.value and 'MAILED' not in student.statusEnum.value:
            grade_ = student.grade
            name_ = student.first_name
            last_name_ = student.last_name
            body = (f"Ocena: {grade_} dla {name_} {last_name_}")
            msg = MIMEText(body)
            msg['Subject'] = "Wystawianie ocen"
            msg['From'] = "sender"
            msg['To'] = ', '.join(student.email)
            smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            mail = 's24124@pjwstk.edu.pl'
            smtp_server.login(mail, 'vyftdjpumglskylb')
            smtp_server.sendmail(mail, [student.email], msg.as_string())
            smtp_server.quit()
            student.status = 'MAILED'
            custom_status = input("Provide custom status: ")
            student.status = 'MAILED_' + custom_status
            log_message(f"Mail was sent to {student.email}.")


def main():
    data = read_file('ocenystudenci')
    while True:
        print("\n--- Menu ---")
        print("1. Wypisz studentów")
        print("2. Wystaw oceny")
        print("3. Usuń studenta")
        print("4. Dodaj studenta")
        print("5. Send mail")
        print("0. Wyjdź")

        choice = input("\nWybierz opcję: ")
        if choice == "1":
            print_students(data)
        elif choice == "2":
            grade_students(data)
        elif choice == "3":
            delete_student(data)
        elif choice == "4":
            add_student(data)
        elif choice == "5":
            send_email(data)
        elif choice == "0":
            break
        else:
            print("Nieprawidłowa opcja")


def log_message(message):
    with open('mylog.txt', 'a') as log_file:
        log_file.write(f'{message}\n')

if __name__ == '__main__':
    main()