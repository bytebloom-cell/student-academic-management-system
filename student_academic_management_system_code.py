
import json
import os
from abc import ABC, abstractmethod


# 1. ABSTRACTION
class Person(ABC):
    def __init__(self, name, age):
        self.name = name
        self.age = age

    @abstractmethod
    def display_info(self):
        pass


# 2. INHERITANCE
class Student(Person):
    def __init__(self, name, age, student_id, batch,
                 department, subjects, cgpa):
        super().__init__(name, age)

        self.student_id = student_id
        self.batch = batch
        self.department = department
        self.subjects = subjects
        self.__cgpa = 0.0
        self.cgpa = cgpa

    # 3. ENCAPSULATION
    @property
    def cgpa(self):
        return self.__cgpa

    @cgpa.setter
    def cgpa(self, value):
        value = float(value)

        if 0 <= value <= 10:
            self.__cgpa = value
        else:
            raise ValueError("CGPA must be between 0 and 10.")

    # Base display method
    def display_info(self):
        print("\n------ Student Information ------")
        print("Name:", self.name)
        print("Age:", self.age)
        print("Student ID:", self.student_id)
        print("Batch:", self.batch)
        print("Department:", self.department)
        print("Subjects:", ", ".join(self.subjects))
        print(f"CGPA: {self.cgpa:.2f}")


# 4. INHERITANCE + POLYMORPHISM
class BTechStudent(Student):
    def __init__(self, name, age, student_id, batch,
                 department, subjects, cgpa, specialization):
        super().__init__(
            name, age, student_id, batch,
            department, subjects, cgpa
        )
        self.specialization = specialization

    # Method overriding
    def display_info(self):
        super().display_info()
        print("Specialization:", self.specialization)


# STUDENT MANAGEMENT
class StudentManager:
    FILE_NAME = "students.json"

    def __init__(self):
        self.students = {}
        self.load_data()

    # SAVE DATA TO JSON
    def save_data(self):
        records = []

        for student in self.students.values():
            records.append({
                "name": student.name,
                "age": student.age,
                "student_id": student.student_id,
                "batch": student.batch,
                "department": student.department,
                "subjects": student.subjects,
                "cgpa": student.cgpa,
                "specialization": student.specialization
            })

        with open(self.FILE_NAME, "w") as file:
            json.dump(records, file, indent=4)

    # LOAD DATA FROM JSON
    def load_data(self):
        if not os.path.exists(self.FILE_NAME):
            return

        try:
            with open(self.FILE_NAME, "r") as file:
                records = json.load(file)

            for data in records:
                student = BTechStudent(**data)
                self.students[student.student_id] = student

        except (OSError, ValueError, TypeError, KeyError) as error:
            print("Error loading data:", error)

    # ADD STUDENT
    def add_student(self):
        try:
            student_id = input("Enter student ID: ").strip()

            if not student_id:
                print("Student ID cannot be empty!")
                return

            if student_id in self.students:
                print("Student ID already exists!")
                return

            name = input("Enter name: ").strip()
            if not name:
                print("Name cannot be empty!")
                return

            age = int(input("Enter age: "))
            if age <= 0:
                print("Age must be positive!")
                return

            batch = input("Enter batch: ").strip()
            department = input("Enter department: ").strip()
            specialization = input("Enter specialization: ").strip()

            subjects = input(
                "Enter subjects separated by commas: "
            ).split(",")

            subjects = [
                subject.strip()
                for subject in subjects
                if subject.strip()
            ]

            if not batch or not department or not subjects:
                print("Batch, department and subjects are required!")
                return

            cgpa = float(input("Enter CGPA: "))

            student = BTechStudent(
                name, age, student_id, batch,
                department, subjects, cgpa, specialization
            )

            self.students[student_id] = student
            self.save_data()

            print("Student registered successfully!")

        except ValueError as error:
            print("Invalid input:", error)
        except OSError as error:
            print("File error:", error)

    # DISPLAY ALL STUDENTS
    def display_all(self):
        if not self.students:
            print("No students registered!")
            return

        for student in self.students.values():
            student.display_info()
            print("-" * 35)

    # SEARCH STUDENT
    def search_student(self):
        query = input("Enter student ID or name: ").strip().lower()
        found = False

        for student in self.students.values():
            if (student.student_id.lower() == query or
                    student.name.lower() == query):
                student.display_info()
                found = True

        if not found:
            print("Student not found!")

    # UPDATE CGPA
    def update_cgpa(self):
        student_id = input("Enter student ID: ").strip()

        if student_id not in self.students:
            print("Student not found!")
            return

        try:
            cgpa = float(input("Enter new CGPA: "))

            self.students[student_id].cgpa = cgpa
            self.save_data()

            print("CGPA updated successfully!")

        except ValueError as error:
            print("Invalid CGPA:", error)
        except OSError as error:
            print("File error:", error)

    # DELETE STUDENT
    def delete_student(self):
        student_id = input("Enter student ID to delete: ").strip()

        if student_id not in self.students:
            print("Student not found!")
            return

        del self.students[student_id]

        try:
            self.save_data()
            print("Student deleted successfully!")
        except OSError as error:
            print("File error:", error)

    # RANK STUDENTS BY CGPA
    def rank_students(self):
        if not self.students:
            print("No students available!")
            return

        ranked = sorted(
            self.students.values(),
            key=lambda student: student.cgpa,
            reverse=True
        )

        print("\n------ Student Rankings ------")

        for rank, student in enumerate(ranked, start=1):
            print(
                f"{rank}. {student.name} "
                f"| ID: {student.student_id} "
                f"| CGPA: {student.cgpa:.2f}"
            )

        print("Topper:", ranked[0].name)

    # ACADEMIC STATISTICS
    def statistics(self):
        if not self.students:
            print("No students available!")
            return

        total = len(self.students)

        average = sum(
            student.cgpa for student in self.students.values()
        ) / total

        print("Total students:", total)
        print(f"Average CGPA: {average:.2f}")

    # MAIN MENU
    def run(self):
        while True:
            print("\n===== STUDENT ACADEMIC MANAGEMENT =====")
            print("1. Add Student")
            print("2. Display All Students")
            print("3. Search Student")
            print("4. Update CGPA")
            print("5. Delete Student")
            print("6. Rank Students")
            print("7. Academic Statistics")
            print("8. Exit")

            choice = input("Enter your choice: ").strip()

            if choice == "1":
                self.add_student()
            elif choice == "2":
                self.display_all()
            elif choice == "3":
                self.search_student()
            elif choice == "4":
                self.update_cgpa()
            elif choice == "5":
                self.delete_student()
            elif choice == "6":
                self.rank_students()
            elif choice == "7":
                self.statistics()
            elif choice == "8":
                print("Thank you for using the system!")
                break
            else:
                print("Invalid choice! Try again.")


# MAIN PROGRAM
if __name__ == "__main__":
    manager = StudentManager()
    manager.run()
