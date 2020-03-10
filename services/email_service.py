class EmailService:
    @staticmethod
    def send_email(to, subject):
        print("sending " + subject + "email to: " + to)
