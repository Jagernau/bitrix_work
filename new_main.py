import threading
import time
import logging
import socket
from datetime import datetime
from data_entry import (
    merge_glonasssoft_data, 
    merge_fort_data, 
    merge_wialon_host_data, 
    merge_wialon_local_data, 
    merge_scout_data,
    merge_era_data,
    get_onec_clients,
)
from database.crud import (
    add_one_object,
    delete_one_object,
    update_one_object,
    add_one_oneC_clients,
    update_one_oneC_client,
)

# Настройка логгера
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('new_log.txt')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

computer_name = str(socket.gethostname())

def monitor_system(fetch_data_func, system_name):
    """Функция для мониторинга одной системы в отдельном потоке."""
    while True:
        current_time = datetime.now()
        if 0 <= current_time.hour < 8:
            logger.info(f"{system_name} приостановлен с 00:00 до 08:00.")
            time.sleep(60)  # Проверка каждые 60 секунд
            continue

        try:
            logger.info(f"Начало получения данных из {system_name}")
            data = fetch_data_func()
            logger.info(f"Данные из {system_name} получены")

            logger.info(f"Начало добавления объектов {system_name}")
            add_one_object(data)
            logger.info(f"Объекты {system_name} добавлены")

            logger.info(f"Начало удаления объектов {system_name}")
            delete_one_object(data)
            logger.info(f"Объекты {system_name} удалены")

            logger.info(f"Начало обновления объектов {system_name}")
            update_one_object(data)
            logger.info(f"Объекты {system_name} обновлены")

            logger.info(f"{system_name} успешно обновлен")
        except Exception as e:
            logger.error(f"Ошибка в системе {system_name}: {e}")
        time.sleep(5)  # Задержка перед следующим циклом

def onec_monitoring():
    """Функция для мониторинга системы 1С."""
    while True:
        current_time = datetime.now()
        if 0 <= current_time.hour < 8:
            logger.info("1С приостановлен с 00:00 до 08:00.")
            time.sleep(60)  # Проверка каждые 60 секунд
            continue

        try:
            logger.info("Клиенты 1С: начало получения данных")
            clients_oneC = get_onec_clients()
            logger.info("Клиенты 1С: данные получены")

            logger.info("Клиенты 1С: добавление данных")
            add_one_oneC_clients(clients_oneC)
            logger.info("Клиенты 1С: данные добавлены")

            logger.info("Клиенты 1С: обновление данных")
            update_one_oneC_client(clients_oneC)
            logger.info("Клиенты 1С: данные обновлены")
        except Exception as e:
            logger.error(f"Ошибка в системе 1С: {e}")
        time.sleep(5)  # Задержка перед следующим циклом

if __name__ == '__main__':
    monitoring_functions = [
        (merge_glonasssoft_data, "Glonass"),
        (merge_fort_data, "Fort"),
        (merge_wialon_host_data, "Wialon Host"),
        (merge_wialon_local_data, "Wialon Local"),
        (merge_scout_data, "Scout"),
        (merge_era_data, "ERA"),
    ]

    threads = []

    # Запуск потоков для каждой системы
    for func, name in monitoring_functions:
        thread = threading.Thread(target=monitor_system, args=(func, name))
        thread.start()
        threads.append(thread)

    # Дополнительный поток для системы 1С, если требуется
    if computer_name != "max-SWH":
        onec_thread = threading.Thread(target=onec_monitoring)
        onec_thread.start()
        threads.append(onec_thread)

    # Ожидание завершения всех потоков
    for thread in threads:
        thread.join()

    logger.info("Все системы завершили работу.")
