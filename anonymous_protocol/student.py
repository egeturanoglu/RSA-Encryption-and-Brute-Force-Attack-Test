class Student:
    def __init__(self, name, credential):
        self.name = name
        self.credential = credential

    def submit_work(self, work_content):
        submission = {
            "credential": {
                "token": self.credential[0],
                "signature": self.credential[1].hex() 
            },
            "work": work_content
        }
        return submission
