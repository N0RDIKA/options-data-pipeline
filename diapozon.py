import json
import os
import peremen
from datetime import datetime, timedelta
def filter_by_strike_price(symbol, date_str, data_dir, price_key="05. price", strike_key="strike", input_filename="merged_data", threshold_percent=40, output_filename="filtered"):
    """Фильтрует данные по strike."""

    input_filename_with_date = f"{symbol}_{input_filename}_{date_str}.json"
    output_filename_with_date = f"{symbol}_{output_filename}_{date_str}_diapozon.json"

    filepath = os.path.join(data_dir, input_filename_with_date)
    output_filepath = os.path.join(data_dir, output_filename_with_date)
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Извлекаем цену из "Global Quote" или первого элемента "data"
        price_str = data.get("Global Quote", {}).get(price_key)
        if price_str is None and data.get("data") and isinstance(data["data"], list) and data["data"][0].get(price_key):
            price_str = data["data"][0].get(price_key)

        if price_str is None or not price_str:
            raise ValueError(f"Ключ '{price_key}' не найден или имеет пустое значение.")

        price = float(price_str)
        threshold = price * (threshold_percent / 100)
        lower_bound = price - threshold
        upper_bound = price + threshold

        filtered_data = {"data": []}

        if isinstance(data.get("data"), list):
            for item in data["data"]:
                strike_str = item.get(strike_key)
                if strike_str is None or not strike_str: # Проверка на None/пустую строку для strike
                    print(f"Пропущена запись с отсутствующим или пустым значением '{strike_key}': {item}")
                    continue

                try:
                    strike = float(strike_str)
                    if lower_bound <= strike <= upper_bound:
                        filtered_data["data"].append(item)
                except (TypeError, ValueError):
                    print(f"Пропущена запись с некорректным значением '{strike_key}': {item}")

   


        os.makedirs(os.path.dirname(output_filepath), exist_ok=True)
        with open(output_filepath, 'w', encoding='utf-8') as f:
            json.dump(filtered_data, f, indent=4)

        print(f"Фильтрованные данные сохранены в {output_filepath}")
        return True

    except (FileNotFoundError, json.JSONDecodeError, ValueError) as e:
        print(f"Ошибка: {e}")
        return False
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return False

def main():
    data_dir = r"C:\Users\User\Documents\papkagit\parserWork\ii\data"

    if isinstance(peremen.date, str):
        date_str = peremen.date
    elif isinstance(peremen.date, datetime):
        date_str = peremen.date.strftime("%Y-%m-%d")
    else:
        date_str = "latest"


    for symbol in peremen.symbols: # Цикл по всем акциям
        if filter_by_strike_price(symbol, date_str, data_dir):
            print(f"Фильтрация для {symbol} на дату {date_str} выполнена успешно.")
        else:
            print(f"Ошибка при фильтрации данных для {symbol} на дату {date_str}.")


if __name__ == "__main__":
    main()

