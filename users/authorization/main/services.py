import requests
from requests.adapters import HTTPAdapter, Retry
import asyncio
import logging
import datetime


async def create_user_wallet_make(token, user):
    web_address = "https://mipt.site"

    retries = Retry(
        total=5,
        backoff_factor=0.1,
        status_forcelist=[ 500, 502, 503, 504 ])

    adapter = HTTPAdapter(max_retries=retries)
    session = requests.Session()
    session.mount('https://', adapter)

    response = session.post(
        web_address + ":8000/wallet/",
        data={
            "type":"create_user_wallet",
            "token":token,
            "username":user.username,
            "email":user.email
        },
        verify=False,
        headers={"Accept": "application/json"})
    response.encoding = 'utf-8'

    log(f"Кошелёк создан. U:{user.username}, T:{token}", "i")

    print(response.status_code, response.reason)

    return response


async def create_user_wallet_prev(token, user):
    response = asyncio.create_task(create_user_wallet_make(token, user))

    res = await asyncio.gather(response)
    return res


def create_user_wallet(token, user):
    check_token_result = asyncio.run(create_user_wallet_prev(token, user))
    return check_token_result


async def send_email_make(email_address, email_text, email_title):
    web_address = "https://mipt.site"
    # web_address = "https://127.0.0.1"
    # web_address = "https://localhost"

    retries = Retry(
        total=5,
        backoff_factor=0.1,
        status_forcelist=[ 500, 502, 503, 504 ])

    adapter = HTTPAdapter(max_retries=retries)
    session = requests.Session()
    session.mount('https://', adapter)

    response = session.post(
        web_address + ":8083/send_email/",
        data={
            "type":"send_email",
            "email_address":email_address,
            "email_text":email_text,
            "email_title": email_title
        },
        verify=False,
        headers={"Accept": "application/json"})
    response.encoding = 'utf-8'

    log(f"Email отправлен. A:{email_address}, T:{email_title}", "i")

    return response


async def send_email_prev(email_address, email_text, email_title):
    response = asyncio.create_task(send_email_make(email_address, email_text, email_title))

    res = await asyncio.gather(response)
    return res


def send_email(email_address, email_text, email_title):
    send_email_result = asyncio.run(send_email_prev(email_address, email_text, email_title))
    return send_email_result


def log(string, log_type="w"):
    _ = f"{str(datetime.datetime.now())[:-7]} {string}"
    if log_type == "d":
        logging.debug(_)
    elif log_type == "i":
        logging.info(_)
    elif log_type == "w":
        logging.warning(_)
    elif log_type == "e":
        logging.error(_)
    elif log_type == "c":
        logging.critical(_)
    else:
        logging.debug(_)
