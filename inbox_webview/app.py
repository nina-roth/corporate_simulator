
import webview

emails = [
    {
        "from": "hr@megacorp.com",
        "subject": "Welcome Aboard!",
        "time": "9:03 AM",
        "body": "We're excited to have you on board.",
        "responses": ["Thanks!", "Can I have a raise already?", "Ignore"]
    },
    {
        "from": "finance@megacorp.com",
        "subject": "Your Expense Report",
        "time": "10:15 AM",
        "body": "There are discrepancies in your expense report.",
        "responses": ["I'll revise it.", "It's correct.", "Ignore"]
    },
    {
        "from": "boss@megacorp.com",
        "subject": "URGENT: TPS Report",
        "time": "10:45 AM",
        "body": "Where is your TPS report?",
        "responses": ["Sending it now.", "Already submitted.", "Ignore"]
    }
]

class API:
    def reply(self, email_index, response_text):
        print(f"Reply to {emails[email_index]['from']}: {response_text}")

if __name__ == '__main__':
    api = API()
    window = webview.create_window("Inbox Simulator", "index.html", js_api=api)
    webview.start()
