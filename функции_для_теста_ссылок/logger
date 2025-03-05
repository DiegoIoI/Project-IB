import logging
import os

log_dir = "logs"

if not os.path.exists(log_dir):
    os.makedirs(log_dir)

log_file = os.path.join(log_dir, "logs.txt")

logging.basicConfig(
    filename=log_file,
    filemode='a',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),  # Запись в файл
        logging.StreamHandler()         # Вывод в консоль
    ]
)

def log_check(domain, result, message):
    try:
        logging.info(f'Checked domain: {domain}, Result: {result}, Message: {message}')
    except Exception as e:
        logging.error(f"Ошибка при записи в лог: {str(e)}")
