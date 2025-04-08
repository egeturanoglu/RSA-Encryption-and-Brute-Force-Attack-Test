import secrets
import string

class Instructor:
    def __init__(self, student_list):
        self.student_list = student_list
        self.token_map = {}
        self.generate_tokens()

    def generate_tokens(self):
        for student in self.student_list:
            token = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(16))
            self.token_map[student] = token

    def get_token_for_student(self, student):
        return self.token_map.get(student)

    def verify_submission(self, submitted_token):
        return submitted_token in self.token_map.values()

class Student:
    def __init__(self, name, instructor: Instructor):
        self.name = name
        self.instructor = instructor
        self.token = instructor.get_token_for_student(name)

    def submit_work(self, work_content):
        submission = {
            'token': self.token,
            'work': work_content
        }
        return submission

def main():
    registered_students = ['Ahmet', 'Ayşe', 'Mehmet', 'Elif']
    instructor = Instructor(registered_students)
    
    print("Dağıtılan Token'lar:")
    for student, token in instructor.token_map.items():
        print(f"{student}: {token}")
    print("--------------------------------------------------\n")

    submissions = []
    student_objects = [Student(name, instructor) for name in registered_students]
    
    for student in student_objects:
        work_content = f"Bu benim ödevim, ben {student.name}."  
        submission = student.submit_work(work_content)
        submissions.append(submission)
    
    fake_submission = {
        'token': "FAKE1234567890AB",  
        'work': "Sahte ödev içeriği."
    }
    submissions.append(fake_submission)
    
    print("Gönderimlerin Doğrulanması:")
    for i, sub in enumerate(submissions, 1):
        is_valid = instructor.verify_submission(sub['token'])
        status = "Geçerli" if is_valid else "Geçersiz"
        print(f"Submission {i}: {status} (Token: {sub['token']})")
    
if __name__ == "__main__":
    main()
