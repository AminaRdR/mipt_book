from django.core.mail import send_mail
from emailservice.settings import EMAIL_HOST_USER
import logging
import datetime
from fpdf import FPDF


class PDF(FPDF):
    def header(self):
        # Logo
        # self.image('logo_bg.png', 170, 7, 33)
        # self.image('miptsite.jpg', 10, 10, 25)
        self.add_font('DejaVu', '', 'fonts/DejaVuSansCondensed.ttf', uni=True)
        self.set_font('DejaVu', '', 14)
        self.cell(80)
        self.cell(30, 10, str('Бронирование аудитории'), 0, 0, 'C')
        self.ln(20)

    # Page footer
    def footer(self):
        self.set_y(-15)
        self.add_font('DejaVu', '', 'fonts/DejaVuSansCondensed.ttf', uni=True)
        pdf.set_font('DejaVu', '', 14)
        self.cell(0, 10, 'Администрация сервиса бронирования аудиторий МФТИ', 0, 0, 'C')


def sendEmail(title, text, address):
    print(f"Send: {str(title)[:10]} {str(text)[:10]} EMAIL HOST: {EMAIL_HOST_USER} ADDRESS:{address}")
    send_mail(
        title,
        text,
        EMAIL_HOST_USER,
        [address],
        fail_silently=False,
    )


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
