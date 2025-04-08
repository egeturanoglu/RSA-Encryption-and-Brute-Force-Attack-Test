from keys import generate_keys, save_keys_to_pem
from instructor import Instructor
from student import Student
import secrets

def main():
    private_key, public_key = generate_keys(key_size=2048)
    save_keys_to_pem(private_key, public_key)
    
    registered_students = ["Alice", "Bob", "Charlie", "Diana"]
    
    instructor = Instructor(registered_students, private_key, public_key)
    credentials = instructor.issue_credentials()
    
    student_list = []
    tokens = list(credentials.keys())
    for i, student_name in enumerate(registered_students):
        token = tokens[i]
        signature = credentials[token]["signature"]
        student_list.append(Student(student_name, (token, signature)))
    
    submissions = []
    for student in student_list:
        work_content = f"This work is prepared by {student.name}."
        submission = student.submit_work(work_content)
        submissions.append(submission)
    
    fake_token = "FAKE1234567890AB"
    fake_signature = secrets.token_bytes(256)  
    fake_submission = {
        "credential": {
            "token": fake_token,
            "signature": fake_signature.hex()
        },
        "work": "Fake work content."
    }
    submissions.append(fake_submission)
    
    print("Submission Verification Results:")
    for i, submission in enumerate(submissions, start=1):
        cred = submission["credential"]
        token = cred["token"]
        signature = bytes.fromhex(cred["signature"])
        valid = instructor.verify_credential(token, signature)
        status = "Valid" if valid else "Invalid"
        print(f"Submission {i}: {status} - Token: {token}")

if __name__ == '__main__':
    main()
