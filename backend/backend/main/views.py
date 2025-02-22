import asyncio

from django.shortcuts import render
from .models import \
    Institute, \
    Building, \
    AudienceStatus, \
    Audience, \
    UsersWallet, \
    Book, \
    BookHistory
from .serializers import \
    InstituteSerializer, \
    BuildingSerializer, \
    AudienceStatusSerializer, \
    AudienceSerializer, \
    UsersWalletSerializer, \
    BookSerializer, \
    BookHistorySerializer
import requests
from .services import \
    get_timetable, \
    check_token, \
    get_book_audience_response, \
    create_user_wallet, \
    log, \
    send_email, \
    update_email, \
    get_time_slots, \
    get_week_time_slots, \
    mark_not_my_booking, \
    mark_this_is_my_booking, update_user_wallet
import logging
import datetime

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import permissions, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework import generics
import json
from .config import get_stop_booking_text, TIME_SLOT_DICT
from django.conf import settings
EMAIL_KEY = settings.EMAIL_KEY


class InstituteViewSet(viewsets.ModelViewSet):
    queryset = Institute.objects.all()
    serializer_class = InstituteSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        log(f"Запрос на получение институтов.", "i")
        queryset = super().get_queryset()
        return self.filter_queryset(queryset)


class BuildingViewSet(viewsets.ModelViewSet):
    queryset = Building.objects.all()
    serializer_class = BuildingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        log(f"Запрос на получение здания. Параметры:{self.request.query_params}", "i")
        queryset = super().get_queryset()
        name = self.request.query_params.get('name')
        institute = self.request.query_params.get('institute')
        if name is not None:
            queryset = super().get_queryset().filter(name=name)
        if institute is not None:
            queryset = queryset.filter(institute__name=institute)
        return self.filter_queryset(queryset)


class AudienceStatusViewSet(viewsets.ModelViewSet):
    queryset = AudienceStatus.objects.all()
    serializer_class = AudienceStatusSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()
        log(f"Запрос на получение статусов аудитории. Параметры:{queryset}", "i")
        return self.filter_queryset(queryset)


class UsersWalletViewSet(viewsets.ModelViewSet):
    queryset = UsersWallet.objects.all()
    serializer_class = UsersWalletSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()
        username = self.request.query_params.get('username')
        if username is not None:
            queryset = queryset.filter(username=username)
        log(f"Запрос на получение параметров кошелька. Параметры:{queryset}, U:{username}", "i")
        return self.filter_queryset(queryset)


class AudienceViewSet(viewsets.ModelViewSet):
    queryset = Audience.objects.all()
    serializer_class = AudienceSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()
        building_name = self.request.query_params.get('building_name')
        institute = self.request.query_params.get('institute')
        status = self.request.query_params.get('status')
        if building_name is not None:
            queryset = super().get_queryset().filter(building__name=building_name)
        if institute is not None:
            queryset = queryset.filter(building__institute__name=institute)
        if status is not None:
            queryset = queryset.filter(audience_status__name=status)
        log(f"Запрос на получение аудиторий по фильтрам. Параметры:{queryset}", "i")
        return self.filter_queryset(queryset)


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()
        audience_number = self.request.query_params.get('audience_number')
        user = self.request.query_params.get('user')
        pair_number = self.request.query_params.get('pair_number')
        building_name = self.request.query_params.get('building_name')
        institute = self.request.query_params.get('institute')
        if audience_number is not None:
            queryset = queryset.filter(audience__number=audience_number)
        if user is not None:
            queryset = queryset.filter(user__username=user)
        if pair_number is not None:
            queryset = queryset.filter(pair_number=pair_number)
        if building_name is not None:
            queryset = queryset.filter(audience__building__name=building_name)
        if institute is not None:
            queryset = queryset.filter(audience__building__institute__name=institute)
        log(f"Запрос на получение бронирований по фильтрам. Параметры:{queryset}", "i")
        return self.filter_queryset(queryset)


class BookHistoryViewSet(viewsets.ModelViewSet):
    queryset = BookHistory.objects.all()
    serializer_class = BookHistorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()
        audience_number = self.request.query_params.get('audience_number')
        user = self.request.query_params.get('user')
        pair_number = self.request.query_params.get('pair_number')
        date = self.request.query_params.get('date')
        booking_time = self.request.query_params.get('booking_time')
        if audience_number is not None:
            queryset = queryset.filter(audience=audience_number)
        if user is not None:
            queryset = queryset.filter(user=user)
        if pair_number is not None:
            queryset = queryset.filter(pair_number=pair_number)
        if date is not None:
            queryset = queryset.filter(date=date)
        if booking_time is not None:
            queryset = queryset.filter(booking_time=booking_time)
        log(f"Запрос на получение истории бронирований по фильтрам. Параметры:{queryset}", "i")
        return self.filter_queryset(queryset)


@csrf_exempt
@api_view(('POST', 'GET'))
def book_audience(request):
    if request.method == 'POST':
        data_request = json.loads(list(request.POST.dict())[0])
        if data_request.get('type') == "book_audience":
            log(f"Бронирование аудитории. Параметры:{data_request}, token:{data_request.get('token')}", "i")
            token = data_request.get('token')
            check_token_result = asyncio.run(check_token(token))
            if check_token_result["result"]:
                # update email of user wallet
                email = check_token_result['value']['email']
                update_email_by_token(check_token_result)
                
                time_slot = -1
                for number, time_slot_name in TIME_SLOT_DICT.items():
                    if time_slot_name == data_request.get('time_slot', "00:00"):
                        time_slot = number
                log(f"========================{time_slot} {data_request.get('time_slot', '00:00')}", "i")
                
                return get_book_audience_response(
                    number=data_request.get('audience'),
                    user=data_request.get('user'),
                    email=email,
                    number_bb=int(data_request.get('number_bb', 0)),
                    pair_number=int(data_request.get('pair_number', 0)),
                    time_slot=time_slot)
            else:
                log(f"Проверка токена выдала ошибку. T:{token}", "e")
                return Response(
                    {"Error": "BAD_TOKEN"},
                    status=status.HTTP_401_UNAUTHORIZED)
        else:
            log(f"Неправильный тип обращения. T:{request.POST.get('type')}", "e")
            return Response(
                {
                    "Error": "BAD_REQUEST_TYPE",
                    "YOUR_REQUEST_TYPE": request.POST.get('type'),
                    "data": json.loads(list(request.POST.dict())[0]),
                    "data_dict": list(request.POST.dict())[0],
                },
                status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
    if request.method == 'GET':
        return render(request, 'book/test.html')


@csrf_exempt
@api_view(('POST', 'GET'))
def index_user_wallet(request):
    # DATA FORMAT (POST):
    # {
    #   "token":    "this_is_your_token",
    #   "type":     "create_user_wallet",
    #   "username": "test_user"
    # }
    if request.method == 'POST':
        if request.POST.get('type') == "create_user_wallet":
            token = request.POST['token']
            try:
                log(f"Начало создания кошелька пользователя: D:{request.POST} T:{token}", "i")
                check_token_result = asyncio.run(check_token(token))
                if check_token_result["result"]:
                    update_email_by_token(check_token_result)
                    username = str(request.POST.get('username', None))
                    email = str(request.POST.get('email', ''))
                    username.replace('Пользователь: ', '')
                    log(f"Username for register: '{username}'", "i")
                    if username is not None:
                        user_wallet = create_user_wallet(username, token=token, email=email)
                        if user_wallet:
                            log(f"User wallet created. Id:{user_wallet.id}, Name:{user_wallet.username}", "i")
                            return Response(
                                {
                                    "result": True,
                                    "create_user_wallet_id": user_wallet.id,
                                    "username": user_wallet.username,
                                    "number_bb": user_wallet.number_bb
                                },
                                status=status.HTTP_201_CREATED)
                        else:
                            log(f"Problems with creating user wallet. User:{username}", "w")
                            return Response(
                                {"Error": "FORBIDDEN_USERNAME"},
                                status=status.HTTP_403_FORBIDDEN)
                    else:
                        log(f"No username in request data. User:{username}, Data:{request.POST}", "w")
                        return Response(
                                {"Error": "NON_AUTHORITATIVE_INFORMATION"},
                                status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
                else:
                    log(f"Problems with checking token. Token:{token}", "w")
                    return Response(
                        {"Error": "BAD_TOKEN", "value": check_token_result},
                        status=status.HTTP_401_UNAUTHORIZED)
            except ConnectionError as e:
                log(f"ConnectionError. Error:{e}", "e")
                return Response(
                    {"Error": "ConnectionError", "value": str(e)},
                    status=status.HTTP_503_SERVICE_UNAVAILABLE)
            except Exception as e:
                log(f"Error:{e}", "e")
                return Response({"Error": "Error", "value": str(e)},
                                status=status.HTTP_503_SERVICE_UNAVAILABLE)
        elif request.POST.get('type') == "update_user_wallet":
            token = request.POST['token']
            try:
                log(f"Начало обновления кошелька пользователя: D:{request.POST} T:{token}", "i")
                if False:
                    username = str(request.POST.get('username', None))
                    email = str(request.POST.get('email', ''))
                    log(f"Update userwallet: '{username}'", "i")

                    for hist_item in BookHistory.objects.filter(user=str(email).split("@")[0]):
                        hist_item.user = username
                        hist_item.save()

                    update_user_wallet(username, token=token, email=email)
                return Response(
                        {"Error": "Обновление кошелька временно откоючено"},
                        status=status.HTTP_201_CREATED)
            except Exception as e:
                log(f"Error:{e}", "e")
                return Response({"Error": "Error", "value": str(e)},
                                status=status.HTTP_503_SERVICE_UNAVAILABLE)
        else:
            log(f"BAD_REQUEST_TYPE. Request type:{request.POST.get('type')}", "e")
            return Response(
                {"Error": "BAD_REQUEST_TYPE"},
                status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
    if request.method == 'GET':
        return render(request, 'wallet/index.html')


@csrf_exempt
@api_view(('POST', 'GET'))
def index_timetable(request):
    if request.method == 'GET':
        if request.GET.get('type') == "get_timetable":
            log(f"Get timetable ended with success", "i")
            audience_number = request.GET.get('audience_number', '')
            if audience_number != '':
                return Response(
                    {
                        "result": True,
                        "audience": audience_number,
                        "data": get_time_slots(audience_number),
                        "user": 2
                    },
                    status=status.HTTP_201_CREATED)
            return Response(
                {
                    "result": True,
                    "audience": get_timetable(),
                    "user": 1
                },
                status=status.HTTP_201_CREATED)
        elif request.GET.get('type') == "get_week_timetable":
            audience_number = request.GET.get('audience_number', '')
            return Response(
                {
                    "result": True,
                    "audience": get_week_time_slots(audience_number),
                    "user": 1
                },
                status=status.HTTP_201_CREATED)
        else:
            return render(request,
                  'timetable/index.html')
    if request.method == 'POST':
        return Response(
                {"Error": "BAD_REQUEST_TYPE"}
        )


@csrf_exempt
@api_view(('POST', 'GET'))
def index_stop_booking(request):
    # DATA FORMAT (POST):
    # {
    #   "token":    "this_is_your_token",
    #   "type":     "stop_booking",
    #   "audience": "audience_number"
    # }
    if request.method == 'POST':
        data_request = json.loads(list(request.POST.dict())[0])
        # data_request = request.POST
        try:
            token = data_request.get('token', '')
            audience_number = data_request.get('audience', '')
            check_token_result = asyncio.run(check_token(token))
            # Проверяем токен на корректность
            if check_token_result["result"]:
                # Обновляем почту подгружая с сервиса авторизации
                update_email_by_token(check_token_result)

                # Проверяем корректность бронирования
                books = Book.objects.filter(audience__number=audience_number)
                booking_number = len(books)
                if booking_number == 1:
                    # В случае если бронирование корректно работаем дальше с бронированием
                    book_item = Book.objects.get(audience__number=audience_number)

                    # Проверяем тип запроса на корректность
                    if data_request.get('type') == "cancel_booking":
                        log(f"CANCEL BOOKING: token={token} audience_number={audience_number}", "i")

                        email_address = book_item.user.email # book_item.user.email "kristal.as@phystech.edu"
                        username = book_item.user.username
                        book_item.to_history()

                        # Собираем данные для отправки email сообщения
                        email_text = get_stop_booking_text(username, audience_number)
                        email_title = f"Прекращение бронирования аудитории {audience_number}"
                        send_email(email_address, email_text, email_title)

                        log(f"Stopping booking ended with success.", "i")
                        return Response(
                            {
                                "result": True,
                                "audience": audience_number,
                                "token": token
                            },
                            status=status.HTTP_201_CREATED)
                    elif data_request.get('type') == "finalize_booking":
                        log(f"FINALIZE BOOKING: token={token} audience_number={audience_number}", "i")

                        email_address = book_item.user.email # book_item.user.email "kristal.as@phystech.edu"
                        username = book_item.user.username
                        book_item.to_history()

                        # Собираем данные для отправки email сообщения
                        email_text = get_stop_booking_text(username, audience_number)
                        email_title = f"Прекращение бронирования аудитории {audience_number}"
                        send_email(email_address, email_text, email_title)

                        log(f"Stopping booking ended with success.", "i")
                        return Response(
                            {
                                "result": True,
                                "audience": audience_number,
                                "token": token
                            },
                            status=status.HTTP_201_CREATED)
                    elif data_request.get('type') == "not_my_booking":
                        token = data_request.get('token', '')
                        audience_number = data_request.get('audience', '')

                        user = UsersWallet.objects.get(username=check_token_result['value']['username'])
                        mark_not_my_booking(user=user, booking=book_item)

                        log(f"NOT MY BOOKING: token={token} audience_number={audience_number}", "i")

                        return Response({"Result": "good | not_my_booking"})

                    elif data_request.get('type') == "this_is_my_booking":
                        token = data_request.get('token', '')
                        audience_number = data_request.get('audience', '')

                        user = UsersWallet.objects.get(username=check_token_result['value']['username'])
                        mark_this_is_my_booking(user=user, booking=book_item)

                        log(f"THIS IS MY BOOKING: token={token} audience_number={audience_number}", "i")

                        return Response({"Result": "good | this_is_my_booking"})
                    else:
                        log(f"BAD_REQUEST_TYPE. Type:{data_request.get('type')}", "e")
                        return Response(
                            {"Error": "BAD_REQUEST_TYPE"},
                            status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
                else:
                    for booking in books:
                        booking.to_history()
                    log(f"Double booking of the audience: {audience_number}. Booking number: {booking_number}", "e")
                    return Response(
                        {
                            "Error": "BookingError",
                            "value": f"length must be is 1, you got {booking_number}",
                            "audience": f"{audience_number}"
                        },
                        status=status.HTTP_501_NOT_IMPLEMENTED)
            else:
                log(f"Problems with checking token in stop booking. Token:{token}", "e")
        except ConnectionError as e:
            log(f"ConnectionError. Error:{e}", "e")
            return Response(
                {"Error": "ConnectionError", "value": str(e)},
                status=status.HTTP_503_SERVICE_UNAVAILABLE)
        except Exception as e:
            log(f"Error:{e}", "e")
            return Response(
                {"Error": "Error", "value": str(e)},
                status=status.HTTP_503_SERVICE_UNAVAILABLE)
    if request.method == 'GET':
        return render(request, 'book/stop_booking.html')


def update_email_by_token(check_token_result):
    # update email of user wallet
    user_name = check_token_result['value']['username']
    email = check_token_result['value']['email']
    update_email(user_name, email)
    return user_name

