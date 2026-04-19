import json
import os
from datetime import datetime, timedelta
import peremen

def merge_options_and_global(symbol, date_str, data_dir, output_filename="merged_data"):
    """Объединяет данные из файлов опционов и глобальных котировок."""

    options_filename = f"{symbol}_options_latest.json"
    global_filename = f"{symbol}_price.json"
    merged_filename = f"{symbol}_{output_filename}_{date_str}.json"
    options_filepath = os.path.join(data_dir, options_filename)
    global_filepath = os.path.join(data_dir, global_filename)
    output_filepath = os.path.join(data_dir, merged_filename)

    try:
        with open(options_filepath, 'r') as f:
            options_data = json.load(f)

        with open(global_filepath, 'r') as f:
            global_data = json.load(f)

        global_price = global_data.get("Global Quote", {}).get("05. price")

        if isinstance(options_data.get("data"), list) and global_price is not None:
            for item in options_data["data"]: # Исправлено имя переменной
                item["05. price"] = global_price

        os.makedirs(os.path.dirname(output_filepath), exist_ok=True)
        with open(output_filepath, 'w') as f:
            json.dump(options_data, f, indent=4)

        print(f"Данные объединены и сохранены в {output_filepath}")
        return True

    except FileNotFoundError:
        print(f"Ошибка: Один из файлов не найден ({options_filepath} или {global_filepath})")
        return False
    except json.JSONDecodeError:
        print(f"Ошибка: Неверный формат JSON в одном из файлов.")
        return False
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return False


def main():
    data_dir = r"C:\Users\User\Documents\papkagit\parserWork\ii\data"
    
    if isinstance(peremen.date, str): # Проверяем тип date
        date_str = peremen.date
    elif isinstance(peremen.date, datetime):
        date_str = peremen.date.strftime("%Y-%m-%d")
    else:
        date_str = "latest"


    for symbol in peremen.symbols:
        if merge_options_and_global(symbol, date_str, data_dir):
            print(f"Объединение данных для {symbol} на дату {date_str} выполнено успешно.")
        else:
            print(f"Ошибка при объединении данных для {symbol} на дату {date_str}.")

if __name__ == "__main__":
    main()
