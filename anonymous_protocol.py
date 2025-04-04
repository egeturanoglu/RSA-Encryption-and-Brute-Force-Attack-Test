# anonymous_protocol.py
import random
import hashlib

class Instructor:
    def __init__(self, student_count):
        self.student_ids = [f"student{i}" for i in range(1, student_count + 1)]
        self.secret_key = "instructor-secret"
        self.issued_tokens = {}

    def assign_token(self, student_id):
        token = hashlib.sha256((student_id + self.secret_key).encode()).hexdigest()
        self.issued_tokens[token] = student_id
        return token

    def verify_submission(self, token):
        return token in self.issued_tokens

class Student:
    def __init__(self, student_id, instructor):
        self.student_id = student_id
        self.token = instructor.assign_token(student_id)

    def submit_assignment(self):
        return self.token

# Test
if __name__ == "__main__":
    instructor = Instructor(student_count=3)
    students = [Student(f"student{i+1}", instructor) for i in range(3)]

    for i, student in enumerate(students):
        submission = student.submit_assignment()
        result = instructor.verify_submission(submission)
        print(f"Student {i+1} submission verified: {result}")
