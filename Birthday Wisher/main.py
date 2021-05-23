import smtplib
from datetime import datetime
import random
import pandas as pd

MY_EMAIL = "test@gmail.com"
PASSWORD = "abcd1234"

EMAIL_SERVER = {
    "gmail.com": "smtp.gmail.com",
    "yahoo.com": "smtp.mail.yahoo.com",
    "hotmail.com": "smtp.live.com"
}

now = datetime.now()
today = (now.month, now.day)

data_birthdays = pd.read_csv('data/birthdays.csv')
birthdays_dict = data_birthdays.to_dict(orient="records")

for person in birthdays_dict:

    birthday = (person["month"], person["day"])

    if today == birthday:
        server = person["email"].split('@')[1]
        file_path = f"data/letter_templates/letter_{random.randint(1,3)}.txt"

        with open(file_path) as letter_file:
            letter = letter_file.read()
            letter = letter.replace("[NAME]", person["name"])

        with smtplib.SMTP(EMAIL_SERVER[server]) as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=PASSWORD)
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs=person["email"],
                msg=f"Subject:Happy Birthday!\n\n{letter}"
            )
