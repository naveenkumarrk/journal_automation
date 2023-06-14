import requests
import os
import smtplib
from email.message import EmailMessage
from datetime import datetime, timedelta
from dotenv import load_dotenv
import sqlite3
import random
import csv
import logging

# Load environment variables
load_dotenv()
EMAIL_ADDRESS = os.environ.get("EMAIL_USER")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASS")

SPRINGER_API_KEY = os.environ.get("SPRINGER_API_KEY")

# Connect to the database
conn = sqlite3.connect('journal_emails.db')
conn.execute('''CREATE TABLE IF NOT EXISTS users
                (email text PRIMARY KEY, last_sent_date text, start integer, end integer, interest text)''')
conn.execute('''CREATE TABLE IF NOT EXISTS journals
                (email text, journal_name text, UNIQUE(email, journal_name))''')

# Configure logging
logging.basicConfig(filename='journal.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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
    url=f"https://api.springer.com/meta/v2/json?q={interest}&api_key={SPRINGER_API_KEY}&s={start}&p={end}"
    return url

def get_springer_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as errh:
        print("HTTP Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print("Error:", err)
    
    return None

def check_sent_journals(email, journal_name):
    cursor = conn.execute(
        "SELECT * FROM journals WHERE email=? AND journal_name=?", (email, journal_name))
    return cursor.fetchone() is not None


def retrieve_user_data():
    cursor = conn.execute("SELECT email, interest FROM users")
    return cursor.fetchall()


def save_user_details_to_csv(email, interest):
    with open('users.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([email, interest])


# Load subscribers' email and interest from the website's database
subscribers = retrieve_user_data()

subject = 'Automated Journal Papers According to Your Interest'

for user in subscribers:
    email = user[0]
    interest = user[1]
    save_user_details_to_csv(email, interest)

    cursor = conn.execute(
        "SELECT last_sent_date, start, end FROM users WHERE email=?", (email,))
    result = cursor.fetchone()

    if result is None:
        start = 1
        end = 5
        conn.execute("INSERT INTO users (email, last_sent_date, start, end, interest) VALUES (?, ?, ?, ?, ?)",
                     (email, datetime.now(), start, end, interest))
    else:
        start = result[1]
        end = result[2]

        springer_api_url = get_springer_api_url(interest, start, end)

        springer_data = get_springer_data(springer_api_url)

        if springer_data is not None and 'records' in springer_data:
            if len(springer_data['records']) == 0:
                start = 1
                end = 5
            else:

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
                                        
                                        a {{
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
                                            <tbody>'''
                                            
                            new_journals = []
                            journals_sent = 0

                            for item in springer_data['records']:
                                journal_name = item['title']
                                link = item['url'][0]['value']
                                abstract = item['abstract']

                                if not check_sent_journals(email, journal_name):
                                    if journals_sent < 5:
                                        abstract_sentences = abstract.split('. ')
                                        abstract_paragraph = '. '.join(abstract_sentences[:2])
                                        abstract_paragraph += '.' if len(abstract_sentences) > 2 else ''
                                        body += f'''
                                            <tr>
                                                <td>
                                                    <div class="journal-entry">
                                                    <a href="{link}"><h3 class="journal-title">{journal_name}</h3></a>
                                                    <p class="journal-abstract">{abstract_paragraph}</p>
                                                </div>
                                                </td>
                                            </tr>        '''

                                        new_journals.append((email, journal_name))
                                        journals_sent += 1
                                    else:
                                        break
                             
                             
                            body+='''
                                            </tbody>
                                        </table>
                                    </div>
                                </body>
                                </html>
                            '''

                            try:
                                send_email(subject, body, [email])
                                logging.info(f"Email sent successfully t{email}")
                            except Exception as e:
                                logging.error(f"Error sending email t{email}: {str(e)}")

                            if len(new_journals) > 0:
                                conn.executemany(
                        "INSERT INTO journals (email, journal_name) VALUES (?, ?)", new_journals)

                            start += 5
                            end += 5
                            conn.execute(
                    "UPDATE users SET start=?, end=? WHERE email=?", (start, end, email))
        else:
            print("Invalid or empty response from Springer API.")

conn.commit()
conn.close()





# old file format



# import requests
# import os
# import smtplib
# from email.message import EmailMessage
# from datetime import datetime, timedelta
# from dotenv import load_dotenv
# import sqlite3
# import random
# import csv
# import logging

# # Load environment variables
# load_dotenv()
# EMAIL_ADDRESS = os.environ.get("EMAIL_USER")
# EMAIL_PASSWORD = os.environ.get("EMAIL_PASS")

# SPRINGER_API_KEY = os.environ.get("SPRINGER_API_KEY")
# IEEE_API_KEY = os.environ.get("IEEE_API_KEY")

# # Connect to the database
# conn = sqlite3.connect('journal_emails.db')
# conn.execute('''CREATE TABLE IF NOT EXISTS users
#                 (email text PRIMARY KEY, last_sent_date text, start integer, end integer, interest text)''')
# conn.execute('''CREATE TABLE IF NOT EXISTS journals
#                 (email text, journal_name text, UNIQUE(email, journal_name))''')

# # Configure logging
# logging.basicConfig(filename='journal.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# def send_email(subject, body, recipients):
#     msg = EmailMessage()
#     msg['Subject'] = subject
#     msg['From'] = EMAIL_ADDRESS
#     msg['To'] = ', '.join(recipients)
#     msg.set_content(body)

#     msg.add_alternative(body, subtype='html')

#     with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
#         smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
#         smtp.send_message(msg)


# def get_springer_api_url(interest, start, end):
#     return f"https://api.springer.com/meta/v2/json?q={interest}&api_key={SPRINGER_API_KEY}&s={start}&p={end}"


# def check_sent_journals(email, journal_name):
#     cursor = conn.execute(
#         "SELECT * FROM journals WHERE email=? AND journal_name=?", (email, journal_name))
#     return cursor.fetchone() is not None


# def retrieve_user_data():
#     cursor = conn.execute("SELECT email, interest FROM users")
#     return cursor.fetchall()


# def save_user_details_to_csv(email, interest):
#     with open('users.csv', 'a', newline='') as file:
#         writer = csv.writer(file)
#         writer.writerow([email, interest])


# # Load subscribers' email and interest from the website's database
# subscribers = retrieve_user_data()

# subject = 'Automated Journal Papers According to Your Interest'

# for user in subscribers:
#     email = user[0]
#     interest = user[1]
#     save_user_details_to_csv(email, interest)

#     cursor = conn.execute(
#         "SELECT last_sent_date, start, end FROM users WHERE email=?", (email,))
#     result = cursor.fetchone()

#     if result is None:
#         start = 1
#         end = 5
#         conn.execute("INSERT INTO users (email, last_sent_date, start, end, interest) VALUES (?, ?, ?, ?, ?)",
#                      (email, datetime.now(), start, end, interest))
#     else:
#         start = result[1]
#         end = result[2]

#         springer_api_url = get_springer_api_url(interest, start, end)

#         springer_response = requests.get(springer_api_url)
#         springer_data = springer_response.json()

#         if len(springer_data['records']) == 0:
#             start = 1
#             end = 5

#         body = '''
#             <!DOCTYPE html>
#             <html lang="en">
#             <head>
#                 <style>
#                     .container {{
#                         max-width: 600px;
#                         margin: 0 auto;
#                         padding: 20px;
#                     }}
                    
#                     table {{
#                         width: 100%;
#                         border-collapse: collapse;
#                     }}
                    
#                     th, td {{
#                         padding: 8px;
#                         border-bottom: 1px solid black;
#                     }}
                    
#                     .journal-title {{
#                         font-weight: 700;
#                         margin-bottom: 5px;
#                         font-size: 18px
#                     }}
                    
#                     .journal-abstract {{
#                         margin-bottom: 10px;
#                         font-size: 16px
#                     }}
                    
#                     a {{
#                         text-decoration:none                        
#                     }}
#                 </style>
#             </head>
#             <body>
#                 <div class="container">
#                     <h1 style="color: SlateGray">
#                         Journal Papers for Your Interest:<br> {interest} {''.join(random.choice('🔥🌟✨💡👌🙌😎🤯👍✍👈') for _ in range(3))}
#                     </h1>
#                     <h2>Springer Journals:</h2>
#                     <table>
#                         <tbody>
#         '''

#         new_journals = []
#         journals_sent = 0

#         for item in springer_data['records']:
#             journal_name = item['title']
#             link = item['url'][0]['value']
#             abstract = item['abstract']

#             if not check_sent_journals(email, journal_name):
#                 if journals_sent < 5:
#                     abstract_sentences = abstract.split('. ')
#                     abstract_paragraph = '. '.join(abstract_sentences[:2])
#                     abstract_paragraph += '.' if len(
#                         abstract_sentences) > 2 else ''

#                     body += f'''
#                         <tr>
#                             <td>
#                                 <div class="journal-entry">
#                                     <a href="{link}"><h3 class="journal-title">{journal_name}</h3></a>
#                                     <p class="journal-abstract">{abstract_paragraph}</p>
#                                 </div>
#                             </td>
#                         </tr>
#                     '''
#                     new_journals.append((email, journal_name))
#                     journals_sent += 1
#                 else:
#                     break

#         body += '''
#                         </tbody>
#                     </table>
#                 </div>
#             </body>
#             </html>
#         '''

#         try:
#             send_email(subject, body, [email])
#             logging.info(f"Email sent successfully to {email}")
#         except Exception as e:
#             logging.error(f"Error sending email to {email}: {str(e)}")

#         if len(new_journals) > 0:
#             conn.executemany(
#                 "INSERT INTO journals (email, journal_name) VALUES (?, ?)", new_journals)

#         start += 5
#         end += 5
#         conn.execute(
#             "UPDATE users SET start=?, end=? WHERE email=?", (start, end, email))

# conn.commit()
# conn.close()
