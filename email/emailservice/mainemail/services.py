from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives
from emailservice.settings import EMAIL_HOST_USER
import logging
import os
import datetime
from fpdf import FPDF


class PDF(FPDF):
    def header(self):
        # Logo
        self.image('assets/images/logo_bg.png', 170, 7, 33)
        self.image('assets/images/miptsite.jpg', 10, 10, 25)
        self.add_font('DejaVu', '', 'assets/fonts/DejaVuSansCondensed.ttf', uni=True)
        self.set_font('DejaVu', '', 14)
        self.cell(80)
        self.cell(30, 10, str('Бронирование аудитории'), 0, 0, 'C')
        self.ln(20)

    # Page footer
    def footer(self):
        self.set_y(-15)
        self.add_font('DejaVu', '', 'assets/fonts/DejaVuSansCondensed.ttf', uni=True)
        self.set_font('DejaVu', '', 14)
        self.cell(0, 10, 'Администрация сервиса бронирования аудиторий МФТИ', 0, 0, 'C')


def make_pdf(
        user_name="Александр Сергеевич",
        aud_name="524 ГК",
        start_time="18:35",
        end_time="23:59",
        pair_number="3",
        bb_number=5,
        preferences_list="свежий воздух, тихая музыка"):

    # Instantiation of inherited class
    pdf = PDF()
    # pdf.set_character_set('utf8')
    pdf.alias_nb_pages()
    pdf.add_page()

    pdf.add_font('DejaVu', '', 'assets/fonts/DejaVuSansCondensed.ttf', uni=True)
    pdf.set_font('DejaVu', '', 14)

    pdf.set_y(75)
    pdf.cell(1, 10, f"Уважаемый, {user_name}!", 0, 1)
    pdf.cell(1, 10, f"Вы забронировали аудиторию со следующими параметрами:", 0, 1)
    pdf.cell(1, 10, f"", 0, 1)
    pdf.cell(1, 10, f"    Полное название аудитории:         {aud_name}", 0, 1)
    pdf.cell(1, 10, f"    Время начала бронирования:         {start_time}", 0, 1)
    pdf.cell(1, 10, f"    Время окончания бронирования:   {end_time}", 0, 1)
    pdf.cell(1, 10, f"    Число пар для бронивания:            {pair_number} шт.", 0, 1)
    pdf.cell(1, 10, f"    Баллов бронирования:                    {bb_number} ед./пару", 0, 1)
    pdf.cell(1, 10, f"    Предпочтения:                                 {preferences_list}", 0, 1)
    pdf.cell(1, 10, f"", 0, 1)
    pdf.cell(1, 10, f"Уведомляем Вас о том, что в {start_time} состоиться аукцион бронирования", 0, 1)
    pdf.cell(1, 10, f"по правилам аукциона второй цены на несколько позоций. Подробнее", 0, 1)
    pdf.cell(1, 10, f"с правилами бронирования аудиторий Вы можете озникомиться на сайте: ", 0, 1)
    pdf.cell(1, 10, f"https://mipt.site/info", 0, 1)

    file_name = f"proof/{datetime.date.today().isoformat()}/{start_time}/Подтверждение_{user_name}_{aud_name}_{end_time}_{pair_number}.pdf"
    log(f"filename='{file_name}'", "i")
    
    directory = os.path.dirname(file_name)
    if not os.path.exists(directory):
        os.makedirs(directory)

    pdf.output(file_name)
    return file_name


def send_booking_email(title, text, address,
              user_name="Александр Сергеевич",
              aud_name="524 ГК",
              start_time="18:35",
              end_time="23:59",
              pair_number="3",
              bb_number=5,
              preferences_list="свежий воздух, тихая музыка"):
    log(f"Send: {str(title)[:10]} {str(text)[:10]} EMAIL HOST: {EMAIL_HOST_USER} ADDRESS:{address}", "i")
    message = EmailMultiAlternatives(
        title,
        text,
        EMAIL_HOST_USER,
        [address]
    )
    message.attach_file(make_pdf(user_name, aud_name, start_time, end_time, pair_number, bb_number, preferences_list))
    message.send()


def send_text_email(title, text, address):
    log(f"Send: {str(title)[:10]} {str(text)[:10]} EMAIL HOST: {EMAIL_HOST_USER} ADDRESS:{address}", "i")
    message = send_mail(
        title,
        text,
        EMAIL_HOST_USER,
        [address]
    )
    message.send()


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
