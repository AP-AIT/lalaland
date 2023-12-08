import imaplib
import email
from email.header import decode_header
from pdfminer.high_level import extract_text
import getpass

def fetch_attachments(username, password, folder, sender_email, start_date):
    # Connect to the IMAP server
    mail = imaplib.IMAP4_SSL("imap.gmail.com") # Update server based on your email provider

    # Log in to the email account
    mail.login(username, password)

    # Select the mailbox (inbox in this case)
    mail.select(folder)

    # Search for emails from a specific sender since a specific date
    result, data = mail.search(None, f'(FROM "{sender_email}" SINCE "{start_date}")')

    # Iterate through the list of email IDs
    for num in data[0].split():
        # Fetch the email by ID
        result, msg_data = mail.fetch(num, "(RFC822)")
        raw_email = msg_data[0][1]
        
        # Parse the raw email using the email library
        msg = email.message_from_bytes(raw_email)

        # Iterate through the email parts
        for part in msg.walk():
            if part.get_content_maintype() == 'multipart' or part.get('Content-Disposition') is None:
                continue

            # Extract attachment filename and content
            filename, encoding = decode_header(part.get_filename())[0]
            if isinstance(filename, bytes):
                filename = filename.decode(encoding or 'utf-8')

            # Check if the part is a PDF attachment
            if part.get_content_type() == 'application/pdf':
                pdf_content = part.get_payload(decode=True)
                
                # Save the PDF file
                with open(filename, 'wb') as pdf_file:
                    pdf_file.write(pdf_content)
                print(f"Attachment '{filename}' saved.")

    # Logout from the email account
    mail.logout()

if __name__ == "__main__":
    # Get user email and password
    user_email = "your_email@example.com"
    user_password = "your_password"

    # Specify the details of the email you want to extract
    sender_email = "sender_email@example.com"
    start_date = "2022-01-01"

    # Specify the mailbox (folder) to search (e.g., 'inbox')
    mailbox = 'inbox'

    # Fetch attachments
    fetch_attachments(user_email, user_password, mailbox, sender_email, start_date)
