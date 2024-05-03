import smtplib, ssl
import argparse
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from getpass import getpass
from pathlib import Path

sender = input("Type sender email and press enter: ")
password = getpass("Type sender password and press enter: ")

parser = argparse.ArgumentParser()
parser.add_argument("-r", "--receiver", type=str)
parser.add_argument("-f", "--file", type=str)
parser.add_argument("-s", "--subject", type=str, default="")
args = parser.parse_args()

message = MIMEMultipart("alternative")
message["Subject"] = args.subject
message["From"] = sender
message["To"] = args.receiver

try:
    with open(args.file, "rb") as file:
        content = Path(args.file).read_text()
        if args.file.endswith(".txt"):
            message.attach(MIMEText(content, "text"))
        elif args.file.endswith(".html"):
            message.attach(MIMEText(content, "html"))
        else:
            print("Unknown file format.")
except:
    print("Failed to read message.")
    exit(1)

context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(sender, password)
    server.sendmail(sender, args.receiver, message.as_string())