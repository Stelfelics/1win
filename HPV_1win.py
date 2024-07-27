from requests import post, get
from urllib.parse import unquote, parse_qs
from colorama import Fore
from datetime import datetime, timedelta
from threading import Thread, Lock
from typing import Literal
from random import randint
from os import system as sys
from platform import system as s_name
from time import sleep
from itertools import cycle
from re import search, sub
from json import loads

from Core.Tools.HPV_Getting_File_Paths import HPV_Get_Accounts
from Core.Tools.HPV_Proxy import HPV_Proxy_Checker
from Core.Tools.HPV_User_Agent import HPV_User_Agent

from Core.Config.HPV_Config import *







class HPV_1win:
    '''
    AutoBot Ferma /// HPV
    ---------------------
    [1] - `Выполнение заданий связанные с подписками`
    
    [2] - `Сбор монет за рефералов`
    
    [3] - `Получение ежедневной награды`
    
    [4] - `Улучшение бустов`
    
    [5] - `Апгрейд всех карточек до максимально возможно уровня`
    
    [6] - `1 час беспрерывного тапания`
    
    [7] - `Ожидание от 1 до 3 часов`
    
    [8] - `Повторение действий через 1-3 часа`
    '''



    def __init__(self, Name: str, URL: str, Proxy: dict = None) -> None:
        INFO = self.URL_Clean(URL)
        self.Name = Name                     # Ник аккаунта
        self.TG_ID = INFO['ID']              # ID аккаунта
        self.URL = INFO['URL']               # Уникальная ссылка для авторизации в mini app
        self.Domain = INFO['Domain']         # Домен игры
        self.Proxy = Proxy                   # Прокси (при наличии)
        self.UA = HPV_User_Agent()           # Генерация уникального User Agent
        self.Token = self.Authentication()   # Токен аккаунта



    def URL_Clean(self, URL: str) -> dict:
        '''Очистка уникальной ссылки от лишних элементов'''

        try:
            ID = str(loads(unquote(unquote(unquote(URL.split('tgWebAppData=')[1].split('&tgWebAppVersion')[0]))).split('&')[1].split('user=')[1])['id'])
        except:
            ID = ''

        try:
            _URL = {KEY: VALUE[0] for KEY, VALUE in parse_qs(unquote(unquote(unquote(URL.split('#tgWebAppData=')[1].split('&tgWebAppVersion')[0])))).items()}
        except:
            _URL = ''

        return {'ID': ID, 'URL': _URL, 'Domain': 'https://crypto-clicker-backend-go-prod.100hp.app/'}



    def Current_Time(self) -> str:
        '''Текущее время'''

        return Fore.BLUE + f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'



    def Logging(self, Type: Literal['Success', 'Warning', 'Error'], Name: str, Smile: str, Text: str) -> None:
        '''Логирование'''

        with Console_Lock:
            COLOR = Fore.GREEN if Type == 'Success' else Fore.YELLOW if Type == 'Warning' else Fore.RED # Цвет текста
            DIVIDER = Fore.BLACK + ' | '   # Разделитель

            Time = self.Current_Time()     # Текущее время
            Name = Fore.MAGENTA + Name     # Ник аккаунта
            Smile = COLOR + str(Smile)     # Смайлик
            Text = COLOR + Text            # Текст лога

            print(Time + DIVIDER + Smile + DIVIDER + Text + DIVIDER + Name)



    def Authentication(self) -> str:
        '''Аутентификация аккаунта'''

        URL = self.Domain + 'game/start'
        Headers = {'accept': 'application/json, text/plain, */*', 'accept-language': 'ru,en;q=0.9,uz;q=0.8', 'content-type': 'multipart/form-data; boundary=----WebKitFormBoundarya2JfBapJZfGJnj9A', 'origin': 'https://cryptocklicker-frontend-rnd-prod.100hp.app', 'priority': 'u=1, i', 'referer': 'https://cryptocklicker-frontend-rnd-prod.100hp.app/', 'sec-fetch-dest': 'empty', 'sec-fetch-mode': 'cors', 'sec-fetch-site': 'same-site', 'user-agent': self.UA}

        try:
            Token = post(URL, headers=Headers, params=self.URL, proxies=self.Proxy).json()['token']
            self.Logging('Success', self.Name, '🟢', 'Инициализация успешна!')
            return Token
        except:
            self.Logging('Error', self.Name, '🔴', 'Ошибка инициализации!')
            return ''



    def ReAuthentication(self) -> None:
        '''Повторная аутентификация аккаунта'''

        self.Token = self.Authentication()



    def Get_Info(self) -> dict:
        '''Получение информации о балансе, прибыли в час и силе клика'''

        URL = self.Domain + 'user/balance'
        Headers = {'accept': '*/*', 'accept-language': 'ru,en;q=0.9,uz;q=0.8', 'authorization': f'Bearer {self.Token}', 'origin': 'https://cryptocklicker-frontend-rnd-prod.100hp.app', 'priority': 'u=1, i', 'referer': 'https://cryptocklicker-frontend-rnd-prod.100hp.app/', 'sec-fetch-dest': 'empty', 'sec-fetch-mode': 'cors', 'sec-fetch-site': 'same-site', 'user-agent': self.UA, 'x-user-id': self.TG_ID}

        try:
            HPV = get(URL, headers=Headers, proxies=self.Proxy).json()

            Balance = HPV['coinsBalance'] # Баланс
            Hour_Profit = HPV['miningPerHour'] # Прибыль в час
            Click_Power = HPV['coinsPerClick'] # Сила клика

            return {'Balance': f'{Balance:,}', 'Hour_Profit': f'{Hour_Profit:,}', 'Click_Power': f'{Click_Power:,}'}
        except:
            return None



    def Run_Tasks(self) -> None:
        '''Выполнение заданий связанные с подписками'''

        URL = self.Domain + 'tasks/subscription'
        Headers = {'accept': '*/*', 'accept-language': 'ru,en;q=0.9,uz;q=0.8', 'authorization': f'Bearer {self.Token}', 'origin': 'https://cryptocklicker-frontend-rnd-prod.100hp.app', 'priority': 'u=1, i', 'referer': 'https://cryptocklicker-frontend-rnd-prod.100hp.app/', 'sec-fetch-dest': 'empty', 'sec-fetch-mode': 'cors', 'sec-fetch-site': 'same-site', 'user-agent': self.UA, 'x-user-id': self.TG_ID}

        try:
            HPV = post(URL, headers=Headers, proxies=self.Proxy).json()

            if HPV['isCollected']:
                self.Logging('Success', self.Name, '⚡️', f'Задание с Telegram выполнено! +{HPV["money"]:,}')
                sleep(randint(33, 103)) # Промежуточное ожидание
        except:
            pass



    def Referal_Claim(self) -> dict:
        '''Сбор монет за рефералов'''

        URL = self.Domain + 'friends/collect'
        Headers = {'accept': '*/*', 'accept-language': 'ru,en;q=0.9,uz;q=0.8', 'authorization': f'Bearer {self.Token}', 'origin': 'https://cryptocklicker-frontend-rnd-prod.100hp.app', 'priority': 'u=1, i', 'referer': 'https://cryptocklicker-frontend-rnd-prod.100hp.app/', 'sec-fetch-dest': 'empty', 'sec-fetch-mode': 'cors', 'sec-fetch-site': 'same-site', 'user-agent': self.UA, 'x-user-id': self.TG_ID}

        try:
            HPV = post(URL, headers=Headers, proxies=self.Proxy).json()['coinsCollected']

            return {'Status': True, 'Collected': f'{HPV:,}'} if HPV > 0 else {'Status': False}
        except:
            return {'Status': False}



    def Daily_Reward(self) -> dict:
        '''Получение ежедневной награды'''

        URL = self.Domain + 'tasks/everydayreward'
        Headers = {'accept': '*/*', 'accept-language': 'ru,en;q=0.9,uz;q=0.8', 'authorization': f'Bearer {self.Token}', 'origin': 'https://cryptocklicker-frontend-rnd-prod.100hp.app', 'priority': 'u=1, i', 'referer': 'https://cryptocklicker-frontend-rnd-prod.100hp.app/', 'sec-fetch-dest': 'empty', 'sec-fetch-mode': 'cors', 'sec-fetch-site': 'same-site', 'user-agent': self.UA, 'x-user-id': self.TG_ID}

        try:
            HPV = post(URL, headers=Headers, proxies=self.Proxy).json()['collectedCoins']

            Reward = {'1': 1_000, '2': 1_500, '3': 2_000, '4': 3_000, '5': 4_000, '6': 5_000, '7': 6_000, '8': 7_000, '9': 8_000, '10': 10_000, '11': 13_000, '12': 16_000, '13': 20_000, '14': 25_000, '15': 30_000, '16': 40_000, '17': 50_000, '18': 70_000, '19': 90_000, '20': 100_000, '21': 125_000, '22': 150_000, '23': 200_000, '24': 300_000}

            def Day(Coins):
                ALL = 0
                for _Day, _Reward in Reward.items():
                    ALL += _Reward
                    if ALL == Coins:
                        return _Day

            return {'Status': True, 'Collected': f'{Reward[Day(HPV)]:,}'}
        except:
            return {'Status': False}



    def Get_Cards(self) -> list:
        '''Список всех кард'''

        URL = 'https://cryptocklicker-frontend-rnd-prod.100hp.app/assets/clicker-config-v-3-BmW6CR9W.js'

        try:
            HPV = get(URL, proxies=self.Proxy).text.split('const e=[')[1].split('],i=[{id:')[0].split('{id:"')[1:]

            def Clean(ID: str) -> str:
                return sub(r'\d', '', ID) if search(r'\d', ID) else ID

            CARDS = []
            for Card in HPV:
                Card = Clean(Card.split('",name:"')[0])
                if Card not in CARDS:
                    CARDS.append(Card)

            return CARDS
        except:
            return []



    def Get_Card_ID(self, ID: str) -> dict:
        '''Получение ID карточек'''

        URL = self.Domain + 'minings'
        Headers = {'accept': '*/*', 'accept-language': 'ru,en;q=0.9,uz;q=0.8', 'authorization': f'Bearer {self.Token}', 'origin': 'https://cryptocklicker-frontend-rnd-prod.100hp.app', 'priority': 'u=1, i', 'referer': 'https://cryptocklicker-frontend-rnd-prod.100hp.app/', 'sec-fetch-dest': 'empty', 'sec-fetch-mode': 'cors', 'sec-fetch-site': 'same-site', 'user-agent': self.UA, 'x-user-id': self.TG_ID}

        try:
            HPV = get(URL, headers=Headers, proxies=self.Proxy).json()

            for CARD in HPV:
                if ID in CARD['id']:
                    return {'Status': True, 'Current': CARD['level'], 'New': f'{ID}{CARD["level"] + 1}'}

            return {'Status': True, 'Current': 0, 'New': f'{ID}1'}
        except:
            return {'Status': False}



    def Upgrade_Card(self, ID: str) -> bool:
        '''Апгрейд карточек'''

        URL = self.Domain + 'minings'
        Headers = {'accept': '*/*', 'accept-language': 'ru,en;q=0.9,uz;q=0.8', 'authorization': f'Bearer {self.Token}', 'origin': 'https://cryptocklicker-frontend-rnd-prod.100hp.app', 'priority': 'u=1, i', 'referer': 'https://cryptocklicker-frontend-rnd-prod.100hp.app/', 'sec-fetch-dest': 'empty', 'sec-fetch-mode': 'cors', 'sec-fetch-site': 'same-site', 'user-agent': self.UA, 'x-user-id': self.TG_ID}
        Json = {'id': ID}

        try:
            post(URL, headers=Headers, json=Json, proxies=self.Proxy).json()['totalProfit']
            return True
        except:
            return False



    def Click(self) -> None:
        '''Совершение тапов'''

        URL = self.Domain + 'tap'
        Headers = {'accept': '*/*', 'accept-language': 'ru,en;q=0.9,uz;q=0.8', 'authorization': f'Bearer {self.Token}', 'origin': 'https://cryptocklicker-frontend-rnd-prod.100hp.app', 'priority': 'u=1, i', 'referer': 'https://cryptocklicker-frontend-rnd-prod.100hp.app/', 'sec-fetch-dest': 'empty', 'sec-fetch-mode': 'cors', 'sec-fetch-site': 'same-site', 'user-agent': self.UA, 'x-user-id': self.TG_ID}
        Json = {'tapsCount': randint(COINS[0], COINS[1])}

        try:
            post(URL, headers=Headers, json=Json, proxies=self.Proxy)
            self.Logging('Success', self.Name, '🟢', 'Тап совершён!')
        except:
            self.Logging('Error', self.Name, '🔴', 'Не удалось тапнуть!')



    def Get_Boosts(self) -> list:
        '''Получение списка доступных бустов'''

        URL = self.Domain + 'energy/improvements'
        Headers = {'accept': '*/*', 'accept-language': 'ru,en;q=0.9,uz;q=0.8', 'authorization': f'Bearer {self.Token}', 'origin': 'https://cryptocklicker-frontend-rnd-prod.100hp.app', 'priority': 'u=1, i', 'referer': 'https://cryptocklicker-frontend-rnd-prod.100hp.app/', 'sec-fetch-dest': 'empty', 'sec-fetch-mode': 'cors', 'sec-fetch-site': 'same-site', 'user-agent': self.UA, 'x-user-id': self.TG_ID}

        try:
            return [{'ID': Card['id'], 'LVL': Card['level']} for Card in get(URL, headers=Headers, proxies=self.Proxy).json()]
        except:
            return []



    def Update_Boosts(self, ID: str) -> bool:
        '''апдейт буста'''

        URL = self.Domain + 'energy/improvements'
        Headers = {'accept': '*/*', 'accept-language': 'ru,en;q=0.9,uz;q=0.8', 'authorization': f'Bearer {self.Token}', 'content-type': 'application/json', 'origin': 'https://cryptocklicker-frontend-rnd-prod.100hp.app', 'priority': 'u=1, i', 'referer': 'https://cryptocklicker-frontend-rnd-prod.100hp.app/', 'sec-fetch-dest': 'empty', 'sec-fetch-mode': 'cors', 'sec-fetch-site': 'same-site', 'user-agent': self.UA, 'x-user-id': self.TG_ID}
        Json = {'id': ID}

        try:
            post(URL, headers=Headers, json=Json, proxies=self.Proxy).json()['NextLevel']
            return True
        except:
            return False



    def Run(self) -> None:
        '''Активация бота'''

        while True:
            try:
                if self.Token: # Если аутентификация успешна
                    self.Logging('Success', self.Name, '💰', f'Баланс: {self.Get_Info()["Balance"]} /// Прибыль в час: {self.Get_Info()["Hour_Profit"]} /// Сила клика: {self.Get_Info()["Click_Power"]}')
                    self.Run_Tasks() # Выполнение заданий связанные с подписками


                    # Сбор монет за рефералов
                    Referal_Claim = self.Referal_Claim()
                    if Referal_Claim['Status']:
                        self.Logging('Success', self.Name, '🟢', f'Монеты за рефералов собраны! +{Referal_Claim["Collected"]}')
                        sleep(randint(33, 103)) # Промежуточное ожидание


                    # Получение ежедневной награды
                    Daily_Reward = self.Daily_Reward()
                    if Daily_Reward['Status']:
                        self.Logging('Success', self.Name, '🟢', f'Ежедневная награда получена! +{Daily_Reward["Collected"]}')
                        sleep(randint(33, 103)) # Промежуточное ожидание


                    # Улучшение бустов
                    for Boost in self.Get_Boosts():
                        # Улучшение `Запас энергии` буста (максимальная ёмкость энергии)
                        if 'energylimit' in Boost['ID'] and Boost['LVL'] < MAX_ENERGY_LIMIT:
                            if self.Update_Boosts(Boost['ID']):
                                self.Logging('Success', self.Name, '⚡️', 'Буст `Запас энергии` улучшен!')
                                sleep(randint(33, 103)) # Промежуточное ожидание

                        # Улучшение `Восстановление энергии` буста (скорость восстановления энергии)
                        if 'energyregen' in Boost['ID'] and Boost['LVL'] < MAX_ENERGY_REGEN:
                            if self.Update_Boosts(Boost['ID']):
                                self.Logging('Success', self.Name, '⚡️', 'Буст `Восстановление энергии` улучшен!')
                                sleep(randint(33, 103)) # Промежуточное ожидание


                    # Апгрейд всех карточек до максимально возможно уровня
                    Updates = {}
                    CARDS = self.Get_Cards()
                    while True:
                        # Остановка цикла, если все карточки улучшены (или нет) до максимально возможно уровня
                        if all(Updates) and len(Updates) == len(CARDS): break

                        for CARD in CARDS:
                            CARD_ID = self.Get_Card_ID(CARD) 
                            if CARD_ID['Current'] < MAX_LVL:
                                if self.Upgrade_Card(CARD_ID['New']):
                                    self.Logging('Success', self.Name, '🟢', f'Апгрейд {CARD} успешен! Новый уровень: {CARD_ID["New"][-1]}')
                                    sleep(randint(33, 103)) # Промежуточное ожидание
                                else:
                                    Updates[CARD] = True
                            else:
                                Updates[CARD] = True


                    sleep(randint(33, 103)) # Промежуточное ожидание


                    # 1 час беспрерывного тапания
                    for _ in range(randint(550, 650)):
                        self.Click()
                        sleep(randint(4, 8)) # Промежуточное ожидание


                    Waiting = randint(4_000, 11_000) # Значение времени в секундах для ожидания
                    Waiting_STR = (datetime.now() + timedelta(seconds=Waiting)).strftime('%Y-%m-%d %H:%M:%S') # Значение времени в читаемом виде

                    self.Logging('Success', self.Name, '💰', f'Баланс: {self.Get_Info()["Balance"]} /// Прибыль в час: {self.Get_Info()["Hour_Profit"]} /// Сила клика: {self.Get_Info()["Click_Power"]}')
                    self.Logging('Warning', self.Name, '⏳', f'Следующий сбор наград: {Waiting_STR}!')

                    sleep(Waiting) # Ожидание от 1 до 3 часов
                    self.ReAuthentication() # Повторная аутентификация аккаунта

                else: # Если аутентификация не успешна
                    sleep(randint(33, 66)) # Ожидание от 33 до 66 секунд
                    self.ReAuthentication() # Повторная аутентификация аккаунта
            except:
                pass







if __name__ == '__main__':
    sys('cls') if s_name() == 'Windows' else sys('clear')

    Console_Lock = Lock()
    Proxy = HPV_Proxy_Checker()

    def Start_Thread(Account, URL, Proxy = None):
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
    except:
        print(Fore.RED + '\n\tОшибка чтения `HPV_Account.json`, ссылки указаны некорректно!')


