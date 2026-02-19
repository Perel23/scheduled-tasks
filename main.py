import smtplib
import datetime as dt
import pandas
import random
import os
from dotenv import load_dotenv

load_dotenv()

MY_EMAIL = os.environ["MY_EMAIL"]
PASSWORD = os.environ["PASSWORD"]
SENDER_NAME = os.environ["SENDER_NAME"]

# 1. Check if today matches a birthday in birthdays.csv
today = dt.datetime.now()
data = pandas.read_csv("birthdays.csv")
birthdays_today = data[(data.month == today.month) & (data.day == today.day)]

if birthdays_today.empty:
    print("No birthdays today.")
else:
    for _, row in birthdays_today.iterrows():
        # 2. Pick a random letter template and replace [NAME]
        template_path = f"letter_{random.randint(1, 3)}.txt"
        with open(template_path) as file:
            letter = file.read().replace("[NAME]", row["name"]).replace("[SENDER]", SENDER_NAME)

        # 3. Send the email
        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=PASSWORD)
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs=row["email"],
                msg=f"Subject:Happy Birthday!\n\n{letter}",
            )


