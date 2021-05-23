import smtplib
import datetime as dt
import random

MY_EMAIL = "test@gmail.com"
PASSWORD = "abcd1234"
EMAIL_SERVER = "smtp.gmail.com"

now = dt.datetime.now()
weekday = now.weekday()

if weekday == 0:
    with open('data/quotes.txt') as f:
        all_quotes = f.readlines()
        quote = random.choice(all_quotes)

    print("Subject:Hello\n\n"+quote)

    with smtplib.SMTP(EMAIL_SERVER) as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs="pepe@yahoo.com",
            msg=f"Subject:Monday Motivation\n\n{quote}"
        )
