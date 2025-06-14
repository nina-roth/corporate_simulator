from dataclasses import dataclass
from typing import List, Callable, Optional
from enum import Enum

class EmailStatus(Enum):
    UNREAD = "unread"
    READ = "read"
    ANSWERED = "answered"

@dataclass
class Email:
    sender: str
    subject: str
    time: str
    body: str
    responses: List[str]
    status: EmailStatus = EmailStatus.UNREAD
    consequences: Optional[dict] = None  # Store effects of different responses

class EmailManager:
    def __init__(self):
        self.emails = []
        self.on_email_changed: Optional[Callable[[], None]] = None
    
    def add_email(self, email: Email):
        self.emails.append(email)
        if self.on_email_changed:
            self.on_email_changed()
    
    def handle_response(self, email_index: int, response: str):
        if 0 <= email_index < len(self.emails):
            email = self.emails[email_index]
            email.status = EmailStatus.ANSWERED
            
            # Handle consequences
            if email.consequences and response in email.consequences:
                return email.consequences[response]
        return None