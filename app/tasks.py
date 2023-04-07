import datetime
import requests
from django.conf import settings

import httplib2
import apiclient.discovery
from celery import shared_task
from oauth2client.service_account import ServiceAccountCredentials

from app.models import Order
from app.get_curs import get_rub

import datetime as DT


@shared_task
def send_massage_telegram():
    print('send_massage_telegram')
    orders = Order.objects.all()
    now_day = datetime.date.today()
    # перебор каждого заказа, для дальнейшей проверки срока поставки
    for item in orders:
        print(item.delivery_time)
        # если прошел срок поставки, отправлем сообщение в телеграм
        if now_day > item.delivery_time:
            try:
                token = settings.TOKEN_TELEGRAM
                chat_id = settings.CHAT_ID_TELEGRAM
                message = f'Срок поставки заказа №{item.order_number} истек'
                url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={message}"
                req = requests.get(url).json()
            except:
                ValueError


def get_value_google_sheets():
    """функция считывания файла из Google Sheets"""

    # Файл, полученный в Google Developer Console
    CREDENTIALS_FILE = 'python-key.json'
    # ID Google Sheets документа
    spreadsheet_id = settings.SPREADSHEET_ID

    # Авторизуемся и получаем service — экземпляр доступа к API
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        CREDENTIALS_FILE,
        ['https://www.googleapis.com/auth/spreadsheets',
         'https://www.googleapis.com/auth/drive'])
    httpAuth = credentials.authorize(httplib2.Http())
    service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)

    # Чтение файла
    values = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range='A2:D1000',
        majorDimension='COLUMNS'
    ).execute()
    return values


@shared_task
def full_db_google_sheets():
    """функция наполнения БД"""
    value = get_value_google_sheets()

    # Чтение данных из Google Sheets
    id = tuple(value['values'][0])
    order_number = tuple(value['values'][1])
    prise_usd = tuple(value['values'][2])
    delivery_time = tuple(value['values'][3])

    # процесс преобразование данных, для записи в БД
    order = []

    for item in range(len(id)):
        # изменения формата даты
        dt = DT.datetime.strptime(delivery_time[item], '%d.%m.%Y')
        data = dt.strftime('%Y-%m-%d')

        order.append({'id': id[item], 'order_number': order_number[item], 'prise_usd': prise_usd[item],
                      'delivery_time': data, 'prise_rub': get_rub(int(prise_usd[item]))})

    order_list = []
    for item in order:
        try:
            # проверка, есть ли уже в заказах такой же первичный ключ
            Order.objects.get(id=item['id'])
        except:
            # если ключа нет, то добавляем в модель
            order_list.append(Order(**item))
    Order.objects.bulk_create(order_list)
