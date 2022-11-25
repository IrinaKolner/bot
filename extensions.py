# здесь есть пара вопросов

import requests
import json
from config import exchanges


class ApiException(Exception):
    pass


class Converter:
    @staticmethod
    def get_price(base, sym, amount):
        try:
            base_key = exchanges[base.lower()]
        except KeyError:
            raise ApiException(f'Валюта {base} не найдена!') 
        try:
            sym_key = exchanges[sym.lower()]
        except KeyError:
            raise ApiException(f'Валюта {sym} не найдена')

        if base_key == sym_key:
            raise ApiException(f'Невозможно перевести одинаковые валюты{base}')

        try:
            amount = float(amount.replace(',', '.'))
        except ValueError:
            raise ApiException(f'Не удалось обработать количество {amount}')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={base_key}&tsyms={sym_key}')
        resp = json.loads(r.content)
        # new_price = resp['rates'][sym_key] * float(amount) <- строка из вебинара, там все работало, а у меня выдает ошибку
        new_price = resp[sym_key] * float(amount) # убрала["rates"] - теперь все работает
        return round(new_price, 2)

