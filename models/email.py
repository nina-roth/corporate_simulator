import json
import os
from dataclasses import dataclass
from typing import List, Callable, Optional, TypedDict
from enum import Enum

class EmailStatus(Enum):
    UNREAD = "unread"
    READ = "read"
    ANSWERED = "answered"

class Consequences(TypedDict):
    reputation: int
    stress: int

@dataclass
class ResponseOption:
    text: str
    consequences: Consequences

@dataclass
class Email:
    sender: str
    subject: str
    time: str
    body: str
    responses: List[ResponseOption]
    status: EmailStatus = EmailStatus.UNREAD

class EmailManager:
    def __init__(self):
        self.emails = []
        self.on_email_changed: Optional[Callable[[], None]] = None

    def load_emails(self):
        try:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            emails_path = os.path.join(base_dir, 'data', 'emails', 'emails.jsonl')
            with open(emails_path, "r") as f:
                for line in f:
                    email_data = json.loads(line)
                    # Convert raw response data to ResponseOption objects
                    responses = [
                        ResponseOption(
                            text=r["text"],
                            consequences=r["consequences"]
                        ) for r in email_data["responses"]
                    ]
                    email_data["responses"] = responses
                    self.emails.append(Email(**email_data))
        except Exception as e:
            print(f"Error loading emails from {emails_path}: {str(e)}")
        
    def add_email(self, email: Email):
        self.emails.append(email)
        if self.on_email_changed:
            self.on_email_changed()
    
    def handle_response(self, email_index: int, response_index: int) -> Optional[Consequences]:
        if 0 <= email_index < len(self.emails):
            email = self.emails[email_index]
            if 0 <= response_index < len(email.responses):
                email.status = EmailStatus.ANSWERED
                
                response_option = email.responses[response_index]
                print(f"Selected response: '{response_option.text}' with consequences: {response_option.consequences}")
                return response_option.consequences
        return None