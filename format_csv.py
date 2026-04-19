import json
import csv
import os
import peremen
from datetime import datetime

def json_to_csv(symbol, date_str, data_dir, input_filename="rounded_data", output_filename="csv_data"):
    """Конвертирует JSON файл в CSV."""
    
    # Формируем пути к файлам
    input_filename_with_date = f"{symbol}_{input_filename}_{date_str}.json"
    output_filename_with_date = f"{symbol}_{output_filename}_{date_str}.csv"
    
    input_path = os.path.join(data_dir, input_filename_with_date)
    output_path = os.path.join(data_dir, output_filename_with_date)

    try:
        # Проверяем существование файла
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Файл {input_path} не найден")

        # Читаем JSON
        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Проверяем структуру данных
        if not isinstance(data.get("data"), list):
            raise ValueError("Некорректный формат данных: ожидается список в поле 'data'")

        if len(data["data"]) == 0:
            print(f"Предупреждение: файл {input_path} не содержит данных")
            return False

        # Определяем заголовки CSV
        headers = data["data"][0].keys()

        # Записываем в CSV
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(data["data"])

        print(f"Данные сохранены в CSV: {output_path}")
        return True

    except Exception as e:
        print(f"Ошибка обработки {symbol}: {str(e)}")
        return False

def main():
    data_dir = r"C:\Users\User\Documents\papkagit\parserWork\ii\data"

    # Определяем дату (используем текущую дату, если не задана)
    if isinstance(peremen.date, str):
        date_str = peremen.date
    elif isinstance(peremen.date, datetime):
        date_str = peremen.date.strftime("%Y-%m-%d")
    else:
        date_str = datetime.now().strftime("%Y-%m-%d")

    # Обрабатываем все символы
    for symbol in peremen.symbols:
        print(f"\nОбработка {symbol}...")
        if json_to_csv(symbol, date_str, data_dir):
            print(f"Успешно конвертирован: {symbol}")
        else:
            print(f"Ошибка конвертации: {symbol}")

if __name__ == "__main__":
    main()
