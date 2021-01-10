import json
import requests
from config import keys


class ExchangeException(Exception):
    pass


class Exchange:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        if quote == base:
            raise ExchangeException(f'Одинаковые валюты, нечего конвертировать, потому что {base} = {quote}.')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ExchangeException(f'Не смог найти валюту {quote}. Могу работать только с теми, что в /values')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ExchangeException(f'Не смог найти валюту {base}. Могу работать только с теми, что в /values')

        try:
            amount = float(amount)
        except ValueError:
            raise ExchangeException(f'Не смог обработать количество {amount}. Используйте числа с "."')

        r = requests.get(f'https://api.exchangeratesapi.io/latest?base={quote_ticker}&symbols={base_ticker}')
        total_base = json.loads(r.content)["rates"][keys[base]]
        total_base1 = total_base * amount
        total_base2 = round(total_base * amount,2)

        total_text = f'{amount} {quote_ticker} = {total_base2} {base_ticker} ({total_base1})'
        return total_text
