import json
import os
import csv
from datetime import datetime, timedelta
import peremen

def process_and_round_data(symbol, date_str, data_dir, price_key="05. price", strike_key="strike", last_key="last", input_filename="with_indicators_latest", output_filename="rounded_data"):
    """Обрабатывает и округляет данные из файла."""

    if date_str == "latest":
        date_for_filename = datetime.now().strftime("%Y-%m-%d") # Текущая дата для имени файла
        input_filename_with_date = f"{symbol}_{input_filename}.json"
        output_filename_with_date = f"{symbol}_{output_filename}_{date_for_filename}" # Убрали расширение, так как будем использовать для JSON и CSV
    else:
        input_filename_with_date = f"{symbol}_{input_filename}_{date_str}.json"
        output_filename_with_date = f"{symbol}_{output_filename}_{date_str}"

    filepath = os.path.join(data_dir, input_filename_with_date)
    output_json_filepath = os.path.join(data_dir, f"{output_filename_with_date}.json")
    output_csv_filepath = os.path.join(data_dir, f"{output_filename_with_date}.csv")

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

            if not isinstance(data.get("data"), list):
                raise TypeError("'data' не является списком.")

            rounded_data = {"data": []}

            for item in data["data"]:
                new_item = {}
                for key, value in item.items():
                    if isinstance(value, (int, float)):
                        if key in ["delta", "Вн.Ст.", "Вр.Ст.$", "Вр.Ст.%"]:
                            new_item[key] = str(round(value, 2)).replace('.', ',') # Округление и замена
                        else:
                            new_item[key] = str(value).replace('.', ',')# Замена без округления

                    elif isinstance(value, str):
                        new_item[key] = value.replace('.', ',') # Замена в строках
                    else:
                        new_item[key] = value

                rename_map = {
                    strike_key: "PriceSt",
                    last_key: "PriceOpt",
                    price_key: "PS",
                    
                }
                for old_key, new_key in rename_map.items():
                    if old_key in new_item:
                        new_item[new_key] = new_item.pop(old_key)

                rounded_data["data"].append(new_item)

        # Сохранение в JSON
        with open(output_json_filepath, 'w', encoding='utf-8') as outfile:
            json.dump(rounded_data, outfile, indent=4, ensure_ascii=False)

        # Сохранение в CSV
        if rounded_data["data"]:
            # Получаем все возможные заголовки из всех записей
            fieldnames = set()
            for item in rounded_data["data"]:
                fieldnames.update(item.keys())
            
            with open(output_csv_filepath, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=sorted(fieldnames))
                writer.writeheader()
                writer.writerows(rounded_data["data"])

        print(f"Округленные данные сохранены в JSON: {output_json_filepath}")
        print(f"Округленные данные сохранены в CSV: {output_csv_filepath}")
        return True

    except (FileNotFoundError, json.JSONDecodeError, TypeError) as e:
        print(f"Ошибка: {e}")
        return False


def main():
    data_dir = r"C:\Users\User\Documents\papkagit\parserWork\ii\data"

    if isinstance(peremen.date, str):
        date_str = peremen.date
    elif isinstance(peremen.date, datetime):
        date_str = peremen.date.strftime("%Y-%m-%d")
    else:
        date_str = "latest"

    for symbol in peremen.symbols:
        if process_and_round_data(symbol, date_str, data_dir):
            print(f"Обработка и округление данных для {symbol} на дату {date_str} завершены успешно.")
        else:
            print(f"Ошибка при обработке данных для {symbol} на дату {date_str}.")


if __name__ == "__main__":
    main()
