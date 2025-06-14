class ChatAPI:
    def __init__(self):
        self.messages = []

    def send_message(self, msg):
        print(f"Chat message: {msg}")
        self.messages.append(msg)
        return {"status": "sent"}

    def get_messages(self):
        return self.messages
