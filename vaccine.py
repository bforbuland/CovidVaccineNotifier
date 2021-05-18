import requests
import smtplib
from datetime import date
from datetime import datetime

districtId = 1
today = date.today().strftime("%d-%m-%y")
EMAIL_ADDRESS="your mail"
PASSWORD="your pw"

def create_session_info(center, session):
    return {"name": center["name"],
            "date": session["date"],
            "capacity": session["available_capacity"],
            "age_limit": session["min_age_limit"]}


def get_sessions(data):
    for center in data["centers"]:
        for session in center["sessions"]:
            yield create_session_info(center, session)


def is_available(session):
    return session["capacity"] > 0


def is_eighteen_plus(session):
    return session["age_limit"] == 18


def get_for_seven_days(start_date):
    url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict"
    params = {"district_id": districtId , "date": today}
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0"}
    resp = requests.get(url, params=params, headers=headers)
    data = resp.json()
    return [session for session in get_sessions(data) if is_eighteen_plus(session) and is_available(session)]


def create_output(session_info):
    return f"{session_info['date']} - {session_info['name']} ({session_info['capacity']})"

def send_email(subject,msg):
    try:
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(EMAIL_ADDRESS, PASSWORD)
        message= 'Subject: {}\n\n{}'.format(subject, msg)
        server.sendmail(EMAIL_ADDRESS,EMAIL_ADDRESS, message)
        server.quit()
        print("Email sent successfully.")
    except:
        print("Email failed to send.")


print(get_for_seven_days(datetime.today()))

# fetch data
content = "\n".join([create_output(session_info) for session_info in get_for_seven_days(datetime.today())])


while not content:
    print("No availability of Vaccine")
else:
    print("Available")
    print(content)
    send_email("Vaccine Available",content)
