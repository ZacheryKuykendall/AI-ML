import os
from dotenv import load_dotenv
import imaplib
import email
from email.header import decode_header
import time
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

class EmailTaskExtractor:
    def __init__(self):
        self.email_address = os.getenv('EMAIL_ADDRESS')
        self.password = os.getenv('EMAIL_PASSWORD')
        self.imap_server = os.getenv('IMAP_SERVER')
        self.imap_port = 993
        self.last_uid = 0

    def connect(self):
        self.mail = imaplib.IMAP4_SSL(self.imap_server, self.imap_port)
        self.mail.login(self.email_address, self.password)

    def check_emails(self):
        self.mail.select('INBOX')
        _, search_data = self.mail.search(None, 'ALL')

        for num in search_data[0].split()[::-1]:  # Reverse order to get newest first
            _, data = self.mail.fetch(num, '(RFC822)')
            _, bytes_data = data[0]

            email_message = email.message_from_bytes(bytes_data)
            subject, encoding = decode_header(email_message["Subject"])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding or "utf-8")
            from_ = email_message.get("From")

            # Check if this is a new email
            if int(num) > self.last_uid:
                self.last_uid = int(num)
                body = self.get_email_body(email_message)
                tasks = self.extract_tasks(subject, body)
                self.print_email_info(subject, from_, tasks)
            else:
                break  # We've reached emails we've already seen

    def get_email_body(self, email_message):
        if email_message.is_multipart():
            for part in email_message.walk():
                content_type = part.get_content_type()
                if content_type == "text/plain":
                    return part.get_payload(decode=True).decode()
        else:
            return email_message.get_payload(decode=True).decode()

    def extract_tasks(self, subject, body):
        prompt = f"""
        Analyze the following email and extract any tasks or action items. If there are no clear tasks, suggest potential follow-up actions based on the content. Present the tasks as a numbered list.

        Subject: {subject}

        Body:
        {body}

        Tasks:
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that extracts tasks and action items from emails."},
                {"role": "user", "content": prompt}
            ]
        )

        return response.choices[0].message.content.strip()

    def print_email_info(self, subject, from_, tasks):
        print("\n" + "="*50)
        print(f"New Email from: {from_}")
        print(f"Subject: {subject}")
        print("\nTasks:")
        print(tasks)
        print("="*50 + "\n")

    def run(self):
        while True:
            try:
                self.connect()
                self.check_emails()
                self.mail.logout()
            except Exception as e:
                print(f"An error occurred: {e}")
            print("Waiting for 60 seconds before checking again...")
            time.sleep(60)  # Check every minute

if __name__ == "__main__":
    extractor = EmailTaskExtractor()
    extractor.run()