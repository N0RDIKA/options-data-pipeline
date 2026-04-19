import json
import os
from datetime import datetime
import peremen

def calculate_option_metrics(item, spot_price):
    """Вычисляет все показатели для одного опциона с правильными формулами."""
    try:
        # Парсим основные параметры
        strike = float(item["strike"])
        bid = float(item["bid"])
        ask = float(item["ask"])
        last = float(item["last"])
        
        # Определяем тип опциона (Call/Put)
        is_call = 'C' in item["contractID"]
        item["Тип"] = "CALL" if is_call else "PUT"

        item["name"] = ''.join([c for c in item["contractID"] if c.isalpha() and not c == 'C' and not c == 'P']).split('2')[0]
        
        # Расчет средней цены опциона
        option_price = (bid + ask) / 2
        item["PriceOpt"] = round(option_price, 2)
        
        # 1. Расчет внутренней стоимости
        intrinsic = max(0.0, spot_price - strike) if is_call else max(0.0, strike - spot_price)
        item["Вн.ст"] = round(intrinsic, 2)
        
        # Проверка на аномалии
        if intrinsic > option_price:
            print(f"Предупреждение: Вн.ст ({intrinsic}) > цены опциона ({option_price}) для {item['contractID']}")
        
        # 2. Расчет временной стоимости
        time_value = max(0.0, option_price - intrinsic)
        item["Вр.Ст.$"] = round(time_value, 2)
        
        # 3. Процент временной стоимости
        time_value_percent = (time_value / option_price * 100) if option_price > 0 else 0.0
        item["Вр.Ст.%"] = round(time_value_percent, 2)
        
        # 4. Корректный расчет дельты (нормализованный)
        if is_call:
            delta = (spot_price - strike) / spot_price  # Нормализованная дельта для CALL
        else:
            delta = (strike - spot_price) / spot_price  # Нормализованная дельта для PUT
        item["delta"] = round(delta, 4)
        
        # 5. Расчет дней до экспирации
        expiration_date = datetime.strptime(item["expiration"], "%Y-%m-%d")
        current_date = datetime.strptime(item["date"], "%Y-%m-%d")
        item["Экспирация"] = (expiration_date - current_date).days
        
        # 6. Дополнительные проверки
        if item["Вн.ст"] < 0 or item["Вр.Ст.$"] < 0:
            print(f"Ошибка: Отрицательные значения для {item['contractID']}")
            
        return item
        
    except Exception as e:
        print(f"Ошибка обработки опциона {item.get('contractID', 'UNKNOWN')}: {str(e)}")
        return None

def process_symbol_data(symbol, filename_suffix, data_dir):
    input_filename = f"{symbol}_filtered_{filename_suffix}_diapozon.json"
    output_filename = f"{symbol}_with_indicators_{filename_suffix}.json"
    
    input_path = os.path.join(data_dir, input_filename)
    output_path = os.path.join(data_dir, output_filename)
    
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if not isinstance(data.get("data"), list):
            raise ValueError("Данные должны быть в формате списка")
        
        # Получаем цену акции из первого элемента
        spot_price = float(data["data"][0]["05. price"])
        
        # Обрабатываем каждый опцион
        data["data"] = [calculate_option_metrics(item, spot_price) for item in data["data"]]
        data["data"] = [item for item in data["data"] if item is not None]  # Удаляем None
        
        # Сохраняем результат
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
            
        return True
    
    except Exception as e:
        print(f"Ошибка обработки {symbol}: {str(e)}")
        return False

def main():
    data_dir = r"C:\Users\User\Documents\papkagit\parserWork\ii\data"
    filename_suffix = "latest"  # Фиксированный суффикс

    for symbol in peremen.symbols:
        if process_symbol_data(symbol, filename_suffix, data_dir):
            print(f"Успешно обработан: {symbol}")
        else:
            print(f"Ошибка обработки: {symbol}")

if __name__ == "__main__":
    main()
