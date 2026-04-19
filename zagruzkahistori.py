import json
import os
import requests
from peremen import symbols, api_key
import time

def fetch_global_quote(symbol, api_key):
    """Получает данные о глобальных котировках акций и возвращает только цену."""
    url = 'https://www.alphavantage.co/query'
    params = {
        'function': 'GLOBAL_QUOTE',
        'symbol': symbol,
        'apikey': api_key,
        'datatype': 'json'
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        if "Global Quote" not in data or "05. price" not in data["Global Quote"]:
            print(f"Ошибка: Неполные данные для {symbol}")
            return None

        # Возвращаем данные в требуемой структуре
        result = {
            "Global Quote": {
                "05. price": data["Global Quote"]["05. price"]
            }
        }

        filename = f"{symbol}_price.json"
        filepath = os.path.join("data", filename)
        os.makedirs("data", exist_ok=True)
        
        with open(filepath, 'w') as f:
            json.dump(result, f, indent=4)
            
        print(f"Данные сохранены в {filepath}")
        return filepath

    except requests.exceptions.RequestException as e:
        print(f"Ошибка запроса для {symbol}: {e}")
        return None
    except Exception as e:
        print(f"Неизвестная ошибка для {symbol}: {e}")
        return None

def main():
    if not isinstance(symbols, list):
        print("Ошибка: symbols должен быть списком. Проверьте файл peremen.py")
        return

    for symbol in symbols:
        filepath = fetch_global_quote(symbol, api_key)
        if not filepath:
            print(f"Не удалось получить данные для {symbol}")
        time.sleep(12)  # Соблюдаем лимиты API (5 запросов в минуту)

if __name__ == "__main__":
    main()
