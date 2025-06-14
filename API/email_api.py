class InboxAPI:
    def __init__(self):
        self.emails = [
            {
                "from": "HR Department",
                "subject": "Welcome Aboard",
                "body": "Hello and welcome to MegaCorp.",
                "time": "9:03 AM",
                "responses": ["Thank you!", "When do I start?", "Looking forward to it"]
            },
            {
                "from": "Finance",
                "subject": "Expense Report",
                "body": "Please resubmit your expense report with correct receipts.",
                "time": "10:15 AM",
                "responses": ["Will do", "I already submitted everything", "Need more time"]
            }
        ]

    def get_emails(self):
        return self.emails

    def reply_email(self, index, response):
        print(f"Replied to email {index}: {response}")
        return {"status": "ok"}
