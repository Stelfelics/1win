import json
import urllib

from requests import post, get
from urllib.parse import unquote
from colorama import Fore
from datetime import datetime, timedelta
from threading import Thread, Lock
from typing import Literal
from random import randint
from time import sleep
from itertools import cycle

from Core.Tools.HPV_Getting_File_Paths import HPV_Get_Accounts
from Core.Tools.HPV_Proxy import HPV_Proxy_Checker
from Core.Tools.HPV_User_Agent import HPV_User_Agent

from Core.Config.HPV_Config import *

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Accept-Language': 'ru,en;q=0.9',
    'Content-Length': '44',
    'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundaryOzAYnWTxCoBURBph',
    'Dnt': '1',
    'Origin': 'https://cryptocklicker-frontend-rnd-prod.100hp.app',
    'Priority': 'u=1, i',
    'Referer': 'https://cryptocklicker-frontend-rnd-prod.100hp.app/',
    'Sec-Ch-Ua-Mobile': '?1',
    'Sec-Ch-Ua-Platform': '"Android"',
    'Sec-Ch-Ua': '"Not/A)Brand";v="8", "Chromium";v="126", "YaBrowser";v="24.7", "Yowser";v="2.5"',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': HPV_User_Agent()
}


def Logging(Type: Literal['Success', 'Warning', 'Error'], argName: str, argSmile: str, argText: str) -> None:
    current_time = Fore.BLUE + f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'

    with Console_Lock:
        color = Fore.GREEN if Type == 'Success' else Fore.YELLOW if Type == 'Warning' else Fore.RED  # Цвет текста
        divider = Fore.BLACK + ' | '  # Разделитель

        name = Fore.MAGENTA + argName  # Ник аккаунта
        smile = color + str(argSmile)  # Смайлик
        text = color + argText  # Текст лога

        print(current_time + divider + smile + divider + text + divider + name)


class HPV_1win:
    """
    AutoBot Ferma /// HPV
    ---------------------
    [1] - Выполнение заданий связанные с подписками

    [2] - Сбор монет за рефералов

    [3] - Получение ежедневной награды

    [4] - Улучшение бустов

    [5] - Апгрейд всех карточек до максимально возможно уровня

    [6] - 1 час беспрерывного тапания

    [7] - Ожидание от 1 до 3 часов

    [8] - Повторение действий через 1-3 часа
    """

    def __init__(self, Name: str, URL: str, Proxy: dict = None) -> None:
        INFO = self.URL_Clean(URL)
        self.Name = Name  # Ник аккаунта
        self.id = INFO['id']  # ID аккаунта
        self.tg_web_data = INFO['tg_web_data']  # Уникальная ссылка для авторизации в mini app
        self.Domain = 'https://crypto-clicker-backend-go-prod.100hp.app'  # Домен игры
        self.Proxy = Proxy  # Прокси (при наличии)
        self.UA = HPV_User_Agent()  # Генерация уникального User Agent
        self.Token = self.Authentication()  # Токен аккаунта

    def URL_Clean(self, url: str) -> dict:

        """Очистка уникальной ссылки от лишних элементов"""

        try:

            # === получить уникальную строку
            tg_web_data = unquote(
                string=unquote(
                    string=url.split('tgWebAppData=', maxsplit=1)[1].split('&tgWebAppVersion', maxsplit=1)[0]))

            # === получить id из уникальной строки
            user_param = urllib.parse.parse_qs(tg_web_data).get('user', [None])[0]
            user_data = json.loads(urllib.parse.unquote(user_param))

            return {'id': user_data.get('id'), 'tg_web_data': tg_web_data}
        except Exception as error:
            Logging('Error', self.Name, '🔴', f'Ошибка разбора ссылки: {error}')
            return {'id': '', 'tg_web_data': ''}

    def Authentication(self) -> str:
        """Аутентификация аккаунта"""

        url = f'{self.Domain}/game/start?{self.tg_web_data}'
        headers['X-User-Id'] = str(self.id)

        try:
            Token = post(url, headers=headers, json=self.tg_web_data, proxies=self.Proxy).json()['token']
            Logging('Success', self.Name, '🟢', 'Инициализация успешна!')

            headers['Authorization'] = f'Bearer {Token}'

            return Token
        except Exception as error:
            Logging('Error', self.Name, '🔴', f'Ошибка инициализации: {error}')
            return ''

    def ReAuthentication(self) -> None:
        """Повторная аутентификация аккаунта"""

        self.Token = self.Authentication()

    def Get_Info(self) -> dict:
        """Получение информации о балансе, прибыли в час и силе клика"""

        url = f'{self.Domain}/user/balance'
        try:
            HPV = get(url, headers=headers, json=self.tg_web_data, proxies=self.Proxy).json()

            balance = HPV['coinsBalance']  # Баланс
            hourProfit = HPV['miningPerHour']  # Прибыль в час
            clickPower = HPV['coinsPerClick']  # Сила клика
            currentEnergy = HPV['currentEnergy']

            return {
                'Balance': f'{balance:,}', 'Hour_Profit': f'{hourProfit:,}',
                'Click_Power': f'{clickPower:,}', 'currentEnergy': f'{currentEnergy:,}'
            }
        except Exception as error:
            Logging('Error', self.Name, '🔴', f'Ошибка получения информации о балансе: {error}')

    def Referral_Claim(self) -> dict:
        """Сбор монет за рефералов"""

        url = f'{self.Domain}/friends/collect'
        try:
            HPV = post(url, headers=headers, json=self.tg_web_data, proxies=self.Proxy).json()
            money = HPV['coinsCollected']

            return {'status': True, 'collectedCoins': f'{money:,}'} if money > 0 else {'status': False}
        except Exception as error:
            Logging('Error', self.Name, '🔴', f'Ошибка сбора монет за реферала: {error}')
            return {'status': False, 'collectedCoins': 0}

    def Daily_Reward(self) -> dict:
        """Получение ежедневной награды"""

        url = f'{self.Domain}/tasks/everydayreward'

        try:
            HPV_get = get(url, headers=headers, json=self.tg_web_data, proxies=self.Proxy).json()
            for item in HPV_get['days']:
                if not item['isCollected']:
                    HPV_post = post(url, headers=headers, json=self.tg_web_data, proxies=self.Proxy).json()
                    return {
                        'status': True,
                        'collectedCoins': HPV_post["collectedCoins"],
                        'collectedDay': item['id'][3:]
                    }

            return {'status': True, 'collectedCoins': 0}
        except Exception as error:
            Logging('Error', self.Name, '🔴', f'Ошибка получения ежедневной награды: {error}')
            return {'status': False, 'collectedCoins': 0}

    def handle_req_energy_bonus(self, action: int) -> dict:
        url = f'{self.Domain}/energy/bonus'
        new_headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Accept-Language': 'ru,en;q=0.9',
            'Dnt': '1',
            'Origin': 'https://cryptocklicker-frontend-rnd-prod.100hp.app',
            'Priority': 'u=1, i',
            'Referer': 'https://cryptocklicker-frontend-rnd-prod.100hp.app/',
            'Sec-Ch-Ua-Mobile': '?1',
            'Sec-Ch-Ua-Platform': '"Android"',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': headers['User-Agent'],
            'Authorization': headers['Authorization'],
            'X-User-Id': headers['X-User-Id']
        }

        try:
            if action == 1:
                HPV_get = get(url, headers=new_headers, proxies=self.Proxy).json()
                return {
                    'remaining': HPV_get['remaining'],
                    'seconds_to_next_use': HPV_get['seconds_to_next_use']
                }
            elif action == 2:
                HPV_post = post(url, headers=new_headers, proxies=self.Proxy).json()
                return {
                    'remaining': HPV_post['remaining'],
                    'seconds_to_next_use': HPV_post['seconds_to_next_use']
                }

        except Exception as error:
            Logging('Error', self.Name, '🔴', f'Ошибка получения количества бонусной энергии: {error}')
            return {
                'remaining': -1,
                'seconds_to_next_use': -1
            }

    def handle_energy_bonus(self) -> dict:
        try:
            # Проверяем доступность энергии и время до следующего применения
            energy_status = self.handle_req_energy_bonus(action=1)

            remaining = energy_status['remaining']
            seconds_to_next_use = energy_status['seconds_to_next_use']

            if remaining > 0:
                if seconds_to_next_use == 0:
                    # Если энергия доступна и её можно применить
                    apply_status = self.handle_req_energy_bonus(action=2)
                    Logging('Success', self.Name, '🟢',
                            f'Доп. энергия активирована! Осталось: {apply_status["remaining"]} шт.')
                    return {'remaining': apply_status['remaining']}
                else:
                    # Если энергия доступна, но на восстановлении
                    # Logging('Warning', self.Name, '🟡',
                    #         f'Энергия есть, но на восстановлении. До применения осталось: {seconds_to_next_use} сек.')
                    return {'remaining': remaining, 'seconds_to_next_use': seconds_to_next_use}
            else:
                # Если энергии нет
                # Logging('Error', self.Name, '🔴',
                #         f'Энергия закончилась. До восстановления: {energy_status["remaining"]} сек.')
                return {'remaining': remaining, 'seconds_to_next_use': seconds_to_next_use}

        except Exception as error:
            Logging('Error', self.Name, '🔴', f'Ошибка применения бонусной энергии: {error}')
            return {'remaining': -1, 'seconds_to_next_use': -1}

    def Click(self) -> None:
        """Совершение тапов"""

        url = f'{self.Domain}/tap'
        Json = {'tapsCount': randint(29, 69)}
        try:

            new_headers = {
                'Accept': '*/*',
                'Accept-Encoding': 'gzip, deflate, br, zstd',
                'Accept-Language': 'ru,en;q=0.9',
                'Content-Length': '15',
                'Content-Type': 'application/json',
                'Dnt': '1',
                'Origin': 'https://cryptocklicker-frontend-rnd-prod.100hp.app',
                'Priority': 'u=1, i',
                'Referer': 'https://cryptocklicker-frontend-rnd-prod.100hp.app/',
                'Sec-Ch-Ua': '"Not/A)Brand";v="8", "Chromium";v="126", "YaBrowser";v="24.7", "Yowser";v="2.5"',
                'Sec-Ch-Ua-Mobile': '?1',
                'Sec-Ch-Ua-Platform': '"Android"',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-site',
                'User-Agent': headers['User-Agent'],
                'Authorization': headers['Authorization'],
                'X-User-Id': headers['X-User-Id']

            }

            post(url, headers=new_headers, json=Json, proxies=self.Proxy)
            Logging('Success', self.Name, '🟢', 'Тап совершён!')
        except Exception as error:
            Logging('Error', self.Name, '🔴', f'Не удалось тапнуть: {error}')

    def Run(self) -> None:
        """Активация бота"""

        while True:
            try:

                SLEEP_SEC = randint(21, 69)

                if self.Token:  # Если аутентификация успешна
                    # Сбор монет за рефералов
                    Referral_Claim = self.Referral_Claim()
                    if Referral_Claim['status']:
                        Logging('Success', self.Name, '🟢',
                                f'Монеты за рефералов собраны! +{Referral_Claim["collectedCoins"]}')
                        sleep(SLEEP_SEC)  # Промежуточное ожидание
                    else:
                        Logging('Error', self.Name, '🔴',
                                f'Монеты за рефералов были собраны ранее или рефералов нет!')
                        sleep(SLEEP_SEC)  # Промежуточное ожидание

                    daily_reward = self.Daily_Reward()
                    if daily_reward['status'] and daily_reward['collectedCoins']:
                        Logging('Success', self.Name, '🟢',
                                f'Ежедневная награда получена! За вход на {daily_reward["collectedDay"]}ый день +{daily_reward["collectedCoins"]} монет!')
                        sleep(SLEEP_SEC)  # Промежуточное ожидание
                    else:
                        Logging('Warning', self.Name, '🟡',
                                f'Ежедневная награда уже была получена!')
                        sleep(SLEEP_SEC)  # Промежуточное ожидание

                    # 1 час беспрерывного тапания
                    for _ in range(randint(550, 650)):
                        self.Click()

                        remain_energy = int(self.Get_Info()['currentEnergy'].replace(",", ""))
                        if remain_energy <= 50:
                            bonus_energy = self.handle_energy_bonus()
                            # if bonus_energy['remaining'] == 0 and  bonus_energy['seconds_to_next_use'] > 0:
                            #     print('Sleep 1-3 hours, remain energy 0')

                        sleep(randint(3, 6))  # Промежуточное ожидание

                    Waiting = randint(4_000, 11_000)  # Значение времени в секундах для ожидания
                    Waiting_STR = (datetime.now() + timedelta(seconds=Waiting)).strftime(
                        '%Y-%m-%d %H:%M:%S')  # Значение времени в читаемом виде

                    Logging('Success', self.Name, '💰',
                            f'Баланс: {self.Get_Info()["Balance"]} /// Прибыль в час: {self.Get_Info()["Hour_Profit"]} /// Сила клика: {self.Get_Info()["Click_Power"]}')
                    Logging('Warning', self.Name, '⏳', f'Следующий сбор наград: {Waiting_STR}!')

                    sleep(Waiting)  # Ожидание от 1 до 3 часов
                    self.ReAuthentication()  # Повторная аутентификация аккаунта

                else:  # Если аутентификация не успешна
                    sleep(randint(33, 66))  # Ожидание от 33 до 66 секунд
                    self.ReAuthentication()  # Повторная аутентификация аккаунта
            except Exception as error:
                Logging('Error', self.Name, '🔴', f'Неизвестная ошибка при активации бота: {error}')


if __name__ == '__main__':
    Console_Lock = Lock()
    Proxy = HPV_Proxy_Checker()


    def Start_Thread(Account, URL, Proxy=None):
        _1win = HPV_1win(Account, URL, Proxy)
        _1win.Run()


    if Proxy:
        DIVIDER = Fore.BLACK + ' | '
        Time = Fore.BLUE + f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
        Text = Fore.GREEN + f'Проверка прокси окончена! Работоспособные: {len(Proxy)}'
        print(Time + DIVIDER + '🌐' + DIVIDER + Text)
        sleep(5)

    try:
        for Account, URL in HPV_Get_Accounts().items():
            if Proxy:
                Proxy = cycle(Proxy)
                Thread(target=Start_Thread, args=(Account, URL, next(Proxy),)).start()
            else:
                Thread(target=Start_Thread, args=(Account, URL,)).start()
    except Exception as error:
        Logging('Error', 'BOT', '🔴', f'Неизвестная ошибка при старте потока: {error}')
