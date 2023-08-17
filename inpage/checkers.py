import os
import time
from random import randint
import json
import requests

from dotenv import load_dotenv
from django.core.exceptions import ObjectDoesNotExist
from django.template.defaultfilters import slugify

from shop.models import Game, GameOnSteam, Product


load_dotenv()


def discord_account_checker(auth_code: str) -> bool:
    """Чекер аккаунтов дискорд.

    Для данного чекера было создано кастомное приложение,
    чтобы получить client_id для взаимодействия с апи. Значение
    находится в .env и может быть свободно заменено.
    Функция принимает код аутентицикации пользователя и возвращает
    ответ с ссылкой переадресации, если профиль пользователя существует.
    """
    url = (
        "https://discord.com/api/v9/oauth2/authorize?"
        "response_type=code&"
        "scope=email&"
        f"client_id={os.getenv('DISCORD_CLIENT_ID')}"
    )
    payload = json.dumps({"permissions": "0", "authorize": True})
    headers = {
        "User-Agent": (
            "Mozilla/5.0"
            "(Windows NT 10.0; Win64; x64; rv:103.0)"
            "Gecko/20100101 Firefox/103.0"
        ),
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Content-Type": "application/json",
        "Authorization": auth_code,
        "X-Super-Properties": (
            "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRmlyZWZveCIsImRldml"
            "jZSI6IiIsInN5c3RlbV9sb2NhbGUiOiJlbi1VUyIsImJyb3dzZXJfdXN"
            "lcl9hZ2VudCI6Ik1vemlsbGEvNS4wIChXaW5kb3dzIE5UIDEwLjA7IF"
            "dpbjY0OyB4NjQ7IHJ2OjEwMy4wKSBHZWNrby8yMDEwMDEwMSBGaXJlZ"
            "m94LzEwMy4wIiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTAzLjAiLCJvc192"
            "ZXJzaW9uIjoiMTAiLCJyZWZlcnJlciI6IiIsInJlZmVycmluZ19kb21"
            "haW4iOiIiLCJyZWZlcnJlcl9jdXJyZW50IjoiIiwicmVmZXJyaW5nX2"
            "RvbWFpbl9jdXJyZW50IjoiIiwicmVsZWFzZV9jaGFubmVsIjoic3RhY"
            "mxlIiwiY2xpZW50X2J1aWxkX251bWJlciI6MTQxMjY5LCJjbGllbnRf"
            "ZXZlbnRfc291cmNlIjpudWxsfQ=="
        ),
        "X-Discord-Locale": "en-US",
        "X-Debug-Options": "bugReporterEnabled",
        "Alt-Used": "discord.com",
        "Cookie": (
            "__dcfduid=7dc5606419a411ed9b1fee90ba2eef9f;"
            "__sdcfduid=7dc5606419a411ed9b1fee90ba2eef9f"
            "20120e864cf33496bedf659a7820954f7611454b15423f7553e3e85c08756a75"
        ),
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    return ('location' in response.json())


def vk_account_checker(access_code: str) -> bool:
    """Чекер аккаунтов вк.

    Делает запрос к апи передавая access_code пользователя,
    возвращая ответ, в случае, если аккаунт реальный.
    https://dev.vk.com/method/account.getProfileInfo
    """
    url = (
        'https://api.vk.com/method/account.getProfileInfo?'
        f'access_token={access_code}'
        '&v=5.131'
    )
    response = requests.post(url).json()
    return {
        'status': 'response' in response,
        'id': response['response']['id']
    }


def checker_twitter(user_id) -> bool:
    """Чекер для твиттера.

    Делает простой запрос на страницу личного кабинет по
    айди пользователя.
    """
    time.sleep(randint(1, 10))
    response = requests.get(url=f'https://twitter.com/{user_id}')
    return response.status_code == 200


def checker_twitch(login) -> bool:
    """Функция чекер твич аккаунтов.

    работает через официальное апи твитч.
    Нужно лишь узнать свой client_id и токен
    авторизации:
    https://dev.twitch.tv/docs/authentication/#app-access-tokens
    Client-Id/Идентификатор клиента Twitch API можно найти в
    панели управления своим расширением в лк dev.twitch.tv:
    https://dev.twitch.tv/console/extensions/
    Возвращает True, если пользователь найден, если нет - False.
    """
    response = requests.get(
        url=f'https://api.twitch.tv/helix/users?login={login}',
        headers={
            'Authorization': os.getenv('TWITCH_AUTH_TOKEN'),
            'Client-Id': os.getenv('TWITCH_CLIENT_ID')
        }
    )
    return response.json()['data'] != []


def checker_steam(link_steam_id) -> bool:
    """Чекер для стима.

    Отправляет запрос на апи стима, для работы необходим токен и
    slug пользователя.
    https://steamcommunity.com/dev/apikey
    """
    # находим steam id64
    steam_id = get_steam_id(link_steam_id)
    if steam_id is not None:
        response = requests.get(
            url=(
                f'http://api.steampowered.com/ISteamUser/GetPlayerSummaries'
                f'/v0002/?key={os.getenv("STEAM_TOKEN")}&steamids={steam_id}')
            )
        return response.status_code == 200
    else:
        return False


def get_steam_id(link_steam_id):
    get_steam_id = (
        'http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/'
        f'?key={os.getenv("STEAM_TOKEN")}&'
        f'vanityurl={link_steam_id}'
    )
    steam_id = requests.get(get_steam_id).json()['response'].get('steamid')
    return steam_id


def steam_games_set(link_steam_id, product_id) -> dict:
    """Метод проверяющий аккаунт стим на наличие игр в нем.

    Принимает steam id из ссфлки на профиль и возвращает
    список игр и другие необходимые параметры.
    """
    url = (
        'https://api.steampowered.com/IPlayerService/GetOwnedGames'
        f'/v1/?key={os.getenv("STEAM_TOKEN")}&'
        f'steamid={link_steam_id}&'
        'include_appinfo=True&'
        'include_played_free_games=False&'
        'include_extended_appinfo=True'
    )
    games = {}
    response = requests.get(url)
    games.update({'games': response.json()['response']['games']})
    for game in games:
        try:
            game_instance = Game.objects.get(name=game['name'])
        except ObjectDoesNotExist:
            game_instance = Game.objects.get_or_create(
                name=game['name'],
                slug=slugify(game['name'])
            )
        try:
            GameOnSteam.objects.get_or_create(
                acc=Product.objects.get(id=product_id),
                game=game_instance,
                balance=0,
                block=False
            )
            return True
        except Exception:
            return False


def checker_facebook():
    return
