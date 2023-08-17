import asyncio
import json
import time
from datetime import date
import os
import random
import requests
import uuid
import zipfile

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework.views import APIView
from telethon import TelegramClient

from inpage.serializers import ZipFileSerializer
from inpage.checkers import vk_account_checker
from shop.models import (
    Product, AccountGroup, Category,
    PSIFParamsForProducts, PIFParamsForProducts,
    SexParam
)


def vk_upload_method(request, login, password, access_token, user_id):
    # переменные ниже получаем из формы
    price = request.POST.get('upload-vk-form-acc-price')
    name = request.POST.get('upload-vk-form-name-ru')
    # method = request.POST.get('acc-origin')
    description = request.POST.get('upload-acc-desriptions')
    slug = request.POST.get('upload-vk-form-name-en')
    mes_to_customer = request.POST.get('info_for_buyer')
    # получаем страну,пол,кол-во подписчиков,моб. телефон,дату рождения
    url = (
        'https://api.vk.com/method/users.get?'
        f'access_token={access_token}&'
        f'user_ids={user_id}&'
        'fields=country,sex,followers_count,'
        'friends_count,contacts,bdate,votes&'
        'v=5.131'
    )
    response = requests.get(url)
    if response.status_code == 200:
        country = response.json().get('response')[0]['country']['title']
        # значения sex: 1-женский, 2-мужской, 0-неизвестно
        sex_values = {
                    1: 'woman',
                    2: 'man',
                    0: None
                }
        sex = sex_values[response.json().get('response')[0]['sex']]
        followers = response.json().get('response')[0]['followers_count']
        phone = response.json().get('response')[0]['mobile_phone']
        # вычесляем возраст указанный у аккаунта
        bdate_vk = list(map(
            int, response.json().get('response')[0]['bdate'].split('.')
        ))  # получаем список такого формата [day, month, year]
        today = date.today()
        age = (
            today.year
            - bdate_vk[2]
            - ((today.month, today.day) < (bdate_vk[1], bdate_vk[0]))
        )  # вычитаем года, а также месяца и дни.
        # получаем кол-во друзей
    time.sleep(5)
    url = (
                'https://api.vk.com/method/friends.get?'
                f'user_ids={user_id}&'
                f'access_token={access_token}'
                '&v=5.131'
            )
    response = requests.get(url)
    friends = response.json().get('response')['count']
    # получаем кол-во групп
    time.sleep(5)
    url = (
                'https://api.vk.com/method/groups.get?'
                f'user_ids={user_id}&'
                f'access_token={access_token}'
                '&v=5.131'
            )
    response = requests.get(url)
    groups = response.json().get('response')['count']
    # сохраняем объект в бд
    product = Product.objects.create(
        seller=request.user,
        price=price,
        category=Category.objects.get(slug='vk'),
        country=country,
        name=name,
        login=login,
        password=password,
        token=access_token,
        description=description,
        slug=slug,
        available=True,
        message_to_customer=mes_to_customer
    )
    # присваиваем параметры для данного типа аккаунта
    sex_param = SexParam.objects.get_or_create(
        product=product,
        value=sex
    )
    age_param = PSIFParamsForProducts.objects.get_or_create(
        product=product,
        name='age',
        value=age
    )
    subs_param = PIFParamsForProducts.objects.get_or_create(
        product=product,
        name='subs',
        value=followers
    )
    groups_param = PSIFParamsForProducts.objects.get_or_create(
        product=product,
        name='groups',
        value=groups
    )
    friends_param = PSIFParamsForProducts.objects.get_or_create(
        product=product,
        name='friends',
        value=friends
    )
    return


def index(request):
    data = {'title': 'connect-squad'}
    return render(request, 'inpage/index.html', context=data)


@login_required
def report(request):
    data = {'title': 'report'}
    return render(request, 'info/report.html', context=data)


def contacts(request):
    data = {'title': 'contacts'}
    return render(request, 'info/contacts.html', context=data)


def user_agreements(request):
    data = {'title': 'rules'}
    return render(request, 'info/user-agreements.html', context=data)


def generate_unique_identifier():
    unique_id = str(uuid.uuid4()).replace('-', '')[:6]  # Генерация уникального идентификатора из 6 символов
    return unique_id


def error_404_view(request, exception=None):
    return render(request, 'error/404.html', status=404)


def error_view(request, exception=None):
    return render(request, 'error/500.html', status=500)


@login_required
def massupload_inst(request):
    return render(
        request,
        'upload/accounts/instagram/massuploadinstagram.html'
    )


@login_required
def massupload_ok(request):
    return render(
        request,
        'upload/accounts/ok/massuploadok.html',
    )


@login_required
def massupload_whatsapp(request):
    return render(
        request,
        'upload/accounts/whatsapp/massuploadwhatsapp.html',
    )


@login_required
def massupload_vk(request):
    if request.method == 'POST':
        input_data = request.POST.get('upload-vk-form-accs_list').split(':')
        access_tokens = [input_data[x] for x in range(2, len(input_data), 2)]
        logins = [input_data[x] for x in range(0, len(input_data), 2)]
        passwords = [input_data[x] for x in range(1, len(input_data), 2)]
        s = request.POST
        for acc_id in range(len(access_tokens)):
            check = vk_account_checker(access_tokens[acc_id])
            if check['status']:
                vk_upload_method(
                    request,
                    logins[acc_id],
                    passwords[acc_id],
                    access_tokens[acc_id],
                    check['id']
                )
        else:
            return redirect('edit')
    return render(
        request,
        'upload/accounts/vk/massuploadvk.html')  # либо обратно на страницу загрузки, либо в лк.


@login_required
def massupload_tg(request):
    if request.method == 'POST':
        product_name = request.POST.get('upload-telegram-form-name-ru')
        product_price = request.POST.get('upload-telegram-form-price')
        account_session = request.FILES.get('upload-telegram-form-accounts-session')
        description = request.POST.get('upload-telegram-form')
        print(product_name)
        print(description)
        print(product_price)
        print(account_session)

        url = 'http://127.0.0.1:8000/check-accounts/'  # ?
        files = {'session_file': account_session}
        response = requests.post(url, files=files)
        response_data = response.json()
        result = response_data['answer']

        slug = slugify(product_name)  # Преобразование имени в slug-формат

        category = Category.objects.get(name='Telegram')

        # Проверьте уникальность slug и добавьте уникальный идентификатор при необходимости
        if Product.objects.filter(slug=slug).exists():
            # Генерация уникального идентификатора
            unique_identifier = generate_unique_identifier()  # Ваша логика генерации уникального идентификатора
            # Создание уникального slug с использованием идентификатора
            slug = f"{slug}-{unique_identifier}"
        user = request.user
        product = Product(
            user=user,
            name=product_name,
            slug=slug,
            category=category,
            price=product_price,
            description=description,
            stock=len(result)
        )
        product.save()

        for account_path in result:
            if account_path is None:
                continue
            account = AccountGroup(product=product, torrent_file=account_path)
            account.save()

    data = {'title': 'loading'}
    return render(
        request,
        'upload/accounts/telegram/massuploadtelegram.html',
        context=data
    )


def upload_tg(request):
    return render(
        request,
        'sale/accounts/telegram/saletelegram.html'
    )


def upload_vk(request, login=None, password=None, access_token=None):
    if request.method == 'POST':
        if not any(login, password, access_token):
            login = ''
            password = ''
            access_token = ''
        check = vk_account_checker(access_token)
        if check['status']:
            vk_upload_method(
                request,
                login,
                password,
                access_token,
                check['id']
            )
        return redirect('edit')
    return render(
        request,
        'sale/accounts/vk/salevk.html'
    )


def upload_ok(request):
    return render(
        request,
        'sale/accounts/ok/saleok.html'
    )


def upload_whatsapp(request):
    return render(
        request,
        'sale/accounts/whatsapp/salewhatsapp.html'
    )


def upload_inst(request):
    return render(
        request,
        'sale/accounts/instagram/saleinstagram.html'
    )


class ZipFileView(APIView):
    def get_api_credentials(self, session_file):
        json_file = session_file.replace('.session', '.json')
        try:
            with open(json_file, 'r') as f:
                credentials = json.load(f)
                return credentials['app_id'], credentials['app_hash']
        except Exception:
            api_id = random.randint(10000, 999999)
            api_hash = ''.join(random.choices('0123456789abcdef', k=32))
            credentials = {'api_id': api_id, 'api_hash': api_hash}
            with open(json_file, 'w') as f:
                json.dump(credentials, f)
            return api_id, api_hash

    async def check_session_file(self, session_file):
        try:
            return f"{session_file}"  # ?
            api_id, api_hash = self.get_api_credentials(session_file)
            client = TelegramClient(session_file, api_id, api_hash)
            await client.connect()

            if await client.is_user_authorized():
                await client.disconnect()
                return f"{session_file}"
            else:
                await client.disconnect()
        except Exception:
            pass

    async def handle_session_files(self, session_files):
        tasks = [self.check_session_file(session_file)
                 for session_file in session_files]
        return await asyncio.gather(*tasks)

    def post(self, request):
        serializer = ZipFileSerializer(data=request.data)

        if serializer.is_valid():
            session_file = serializer.validated_data['session_file']

            unique_folder = f"tmp/{str(uuid.uuid4())}"
            os.mkdir(unique_folder)

            with zipfile.ZipFile(session_file, 'r') as zip_ref:
                zip_ref.extractall(unique_folder)

            session_files = [
                os.path.abspath(os.path.join(unique_folder, file_name))
                for file_name in os.listdir(unique_folder)
                if os.path.isfile(
                    os.path.join(unique_folder, file_name)
                ) and file_name.endswith('.session')
            ]

            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                result = loop.run_until_complete(
                    self.handle_session_files(session_files)
                )
            finally:
                loop.close()

            return Response({'answer': result})
        else:
            return Response(serializer.errors, status=400)
