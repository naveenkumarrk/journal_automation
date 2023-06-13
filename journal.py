import requests
import os
import smtplib
import pandas as pd
import pytz
from email.message import EmailMessage
from datetime import datetime, timedelta
from dotenv import load_dotenv
import sqlite3
import random

# Load environment variables
load_dotenv()
EMAIL_ADDRESS = os.environ.get("EMAIL_USER")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASS")

SPRINGER_API_KEY = os.environ.get("SPRINGER_API_KEY")
IEEE_API_KEY = os.environ.get("IEEE_API_KEY")

# Connect to the database
conn = sqlite3.connect('journal_emails.db')
conn.execute('''CREATE TABLE IF NOT EXISTS users
                (email text PRIMARY KEY, last_sent_date text, start integer, end integer, interest text)''')
conn.execute('''CREATE TABLE IF NOT EXISTS journals
                (email text, journal_name text, UNIQUE(email, journal_name))''')


def send_email(subject, body, recipients):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = ', '.join(recipients)
    msg.set_content(body)

    msg.add_alternative(body, subtype='html')

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)


def get_springer_api_url(interest, start, end):
    return f"https://api.springer.com/meta/v2/json?q={interest}&api_key={SPRINGER_API_KEY}&s={start}&p={end}"


def check_sent_journals(email, journal_name):
    cursor = conn.execute(
        "SELECT * FROM journals WHERE email=? AND journal_name=?", (email, journal_name))
    return cursor.fetchone() is not None


# Retrieve user data from the website's database
def retrieve_user_data():
    users_data = pd.read_csv('users.csv')
    return users_data[['email', 'interest']].values.tolist()


# Load subscribers' email and interest from the website's database
subscribers = retrieve_user_data()

subject = 'Automated Journal Papers According to Your Interest'

for user in subscribers:
    email = user[0]
    interest = user[1]

    # Retrieve the start, end, and interest values from the database
    cursor = conn.execute(
        "SELECT last_sent_date, start, end FROM users WHERE email=?", (email,))
    result = cursor.fetchone()

    if result is None:
        # New user, set default values
        start = 1
        end = 5
        conn.execute("INSERT INTO users (email, last_sent_date, start, end, interest) VALUES (?, ?, ?, ?, ?)",
                     (email, datetime.now(), start, end, interest))
    else:
        # Retrieve the start, end, and interest values from the database
        start = result[1]
        end = result[2]

        # Generate the Springer API URL using the stored start and end values
        springer_api_url = get_springer_api_url(interest, start, end)

        # Fetch papers from Springer API
        springer_response = requests.get(springer_api_url)
        springer_data = springer_response.json()

        # Check if there are new journals to send
        if len(springer_data['records']) == 0:
            # Reset start and end values to retrieve from the beginning
            start = 1
            end = 5

        # Prepare email body with new journals
        body = f'''
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <style>
                    .container {{
                        max-width: 600px;
                        margin: 0 auto;
                        padding: 20px;
                    }}
                    
                    table {{
                        width: 100%;
                        border-collapse: collapse;
                    }}
                    
                    th, td {{
                        padding: 8px;
                        border-bottom: 1px solid black;
                    }}
                    
                    .journal-title {{
                        font-weight: 700;
                        margin-bottom: 5px;
                        font-size: 18px
                    }}
                    
                    .journal-abstract {{
                        margin-bottom: 10px;
                        font-size: 16px
                    }}
                    
                    a{{
                        text-decoration:none                        
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <h1 style="color: SlateGray">
                        Journal Papers for Your Interest:<br> {interest} {''.join(random.choice('🔥🌟✨💡👌🙌😎🤯👍✍👈') for _ in range(3))}
                    </h1>
                    <h2>Springer Journals:</h2>
                    <table>
                        <tbody>
        '''

        new_journals = []  # Temporary list to store new journal entries
        journals_sent = 0

        for item in springer_data['records']:
            journal_name = item['title']
            link = item['url'][0]['value']
            abstract = item['abstract']

            if not check_sent_journals(email, journal_name):
                if journals_sent < 5:
                    abstract_sentences = abstract.split('. ')
                    # Include the first two sentences
                    abstract_paragraph = '. '.join(abstract_sentences[:2])
                    # Add period if necessary
                    abstract_paragraph += '.' if len(
                        abstract_sentences) > 2 else ''

                    body += f'''
                        <tr>
                            <td>
                                <div class="journal-entry">
                                    <a href="{link}"><h3 class="journal-title">{journal_name}</h3></a>
                                    <p class="journal-abstract">{abstract_paragraph}</p>
                                </div>
                            </td>
                        </tr>
                    '''
                    new_journals.append(
                        (email, journal_name))  # Add to the temporary list
                    journals_sent += 1
                else:
                    break

        body += '''
                        </tbody>
                    </table>
                </div>
            </body>
            </html>
        '''

        send_email(subject, body, [email])
        print(f"Email sent successfully to {email}")

        if len(new_journals) > 0:
            # Insert new journal entries into the database
            conn.executemany(
                "INSERT INTO journals (email, journal_name) VALUES (?, ?)", new_journals)

        # Update start and end values for the next iteration
        start += 5
        end += 5
        conn.execute(
            "UPDATE users SET start=?, end=? WHERE email=?", (start, end, email))

conn.commit()
conn.close()
