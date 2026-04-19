import json
import os
import requests
from concurrent.futures import ThreadPoolExecutor
from typing import List, Optional, Dict
from peremen import api_key, symbols  # Теперь импортируем и symbols
import time

# Константы
API_URL = "https://www.alphavantage.co/query"
DATA_DIR = "data"
KEYS_TO_KEEP = ["contractID", "strike", "last", "bid", "ask", "date", "expiration"]
MAX_ITEMS = 150
REQUEST_DELAY = 12  # Задержка между запросами для соблюдения лимитов API

def fetch_single_symbol(symbol: str, api_key: str, date: Optional[str] = None) -> Optional[str]:
    """Загружает данные для одного тикера."""
    params = {
        "function": "HISTORICAL_OPTIONS",
        "symbol": symbol,
        "apikey": api_key,
    }
    if date:
        params["date"] = date

    try:
        response = requests.get(API_URL, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()

        if "Error Message" in data:
            print(f"[{symbol}] Ошибка API: {data['Error Message']}")
            return None

        filename = f"{symbol}_options_{date or 'latest'}.json"
        filepath = os.path.join(DATA_DIR, filename)
        
        with open(filepath, "w") as f:
            json.dump(data, f, indent=4)
        
        return filepath

    except requests.exceptions.RequestException as e:
        print(f"[{symbol}] Ошибка запроса: {str(e)[:100]}...")
    except Exception as e:
        print(f"[{symbol}] Неизвестная ошибка: {str(e)[:100]}...")
    return None

def fetch_options_data(symbols: List[str], api_key: str, date: Optional[str] = None) -> List[str]:
    """Основная функция загрузки данных."""
    os.makedirs(DATA_DIR, exist_ok=True)
    saved_files = []
    
    for symbol in symbols:
        filepath = fetch_single_symbol(symbol, api_key, date)
        if filepath:
            saved_files.append(filepath)
        time.sleep(REQUEST_DELAY)  # Соблюдаем лимиты API
    
    print(f"\nУспешно загружено {len(saved_files)}/{len(symbols)} тикеров")
    return saved_files

def filter_option(option: Dict) -> Dict:
    """Фильтрация данных опциона."""
    return {key: option[key] for key in KEYS_TO_KEEP if key in option}

def filter_and_truncate_options_data(filepaths: List[str]) -> None:
    """Фильтрация и сохранение данных."""
    for filepath in filepaths:
        try:
            with open(filepath, "r") as f:
                data = json.load(f)
            
            if isinstance(data.get("data"), list):
                data["data"] = [
                    filter_option(opt) 
                    for opt in data["data"] 
                    if "C" in opt.get("contractID", "")
                ][:MAX_ITEMS]
                
                for key in ["endpoint", "message"]:
                    data.pop(key, None)
                
                with open(filepath, "w") as f:
                    json.dump(data, f, indent=4)
                    
        except Exception as e:
            print(f"Ошибка обработки {filepath}: {str(e)[:100]}...")

if __name__ == "__main__":
    # Теперь symbols берется из peremen.py
    date = None  # Или конкретная дата "2024-03-01"
    
    files = fetch_options_data(symbols, api_key, date)
    if files:
        filter_and_truncate_options_data(files)
