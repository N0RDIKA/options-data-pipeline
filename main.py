import subprocess


def run_scripts_sequentially(scripts):
    """Запускает скрипты последовательно, проверяя результат каждого."""
    for script in scripts:
        try:
            # Указываем явно python.exe, если нужно
            # process = subprocess.run([r"C:\Users\User\AppData\Local\Programs\Python\Python311\python.exe", script], check=True) 
            process = subprocess.run(["python", script], check=True) # Или просто python, если он в PATH
            print(f"Скрипт {script} выполнен успешно.")
        except subprocess.CalledProcessError as e:
            print(f"Ошибка при выполнении скрипта {script}: {e}")
            return False # Прерываем выполнение, если скрипт завершился с ошибкой
        except FileNotFoundError:
            print(f"Ошибка: скрипт {script} не найден. Проверьте путь.")
            return False
    return True



scripts_to_run = [
    "zagruzkaglobal.py",
    "zagruzkahistori.py",
    "obedinenie.py",
    "diapozon.py",
    "rachet_pokazateli.py",
    "oformlenie.py",
    "format_csv.py"
]

if run_scripts_sequentially(scripts_to_run):
    print("Все скрипты выполнены успешно.")
