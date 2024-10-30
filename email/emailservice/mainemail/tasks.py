from emailservice.celery import app
from celery.schedules import crontab
from mainemail.services import send_booking_email, send_text_email
from mainemail.services import log


@app.task
def send_verification_email(user_id):
    try:
        sendEmail("TEST", f"+ celery celery{user_id}", "kristal.as@phystech.edu")
    except Exception as e:
        print(e)


@app.task
def send_task_email(
        email_address: str,
        email_text: str,
        email_title: str,
        user_name="Александр Сергеевич",
        aud_name="524 ГК",
        start_time="18:35",
        end_time="23:59",
        pair_number="3",
        bb_number=5,
        preferences_list="свежий воздух, тихая музыка"):
    try:
        send_booking_email(
            email_title,
            email_text,
            email_address,
            user_name,
            aud_name,
            start_time,
            end_time,
            pair_number,
            bb_number,
            preferences_list)
    except Exception as e:
        log(e, "e")


@app.task
def send_task_text_email(
        email_address: str,
        email_text: str,
        email_title: str):
    try:
        send_text_email(email_title, email_text, email_address)
    except Exception as e:
        log(e, "e")


@app.task
def send_weekly():
    try:
        sendEmail("TEST", "периодично периодично", "kristal.as@phystech.edu")
        return 1
    except Exception as e:
        print(e)
        return 0


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    log("Начало выполнения периодической задачи", 'i')
    sender.add_periodic_task(50.0, send_weekly.s(), name='test_send_weekly')
