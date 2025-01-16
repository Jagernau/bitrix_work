import multiprocessing
import time
import logging
from datetime import datetime
from data_entry import (
    merge_glonasssoft_data, 
    merge_fort_data, 
    merge_wialon_host_data, 
    merge_wialon_local_data, 
    merge_scout_data,
    merge_era_data,
)
from database.crud import (
    add_one_object,
    delete_one_object,
    update_one_object,
)
import schedule
import time

# Настройка логгера
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('16_thread_log.txt')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - [%(threadName)s] - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def monitor_system(fetch_data_func, system_name):
    """Функция для мониторинга одной системы в отдельном потоке."""
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


if __name__ == '__main__':

    def job():
        monitoring_functions = [
            (merge_glonasssoft_data, "Glonass"),
            (merge_fort_data, "Fort"),
            (merge_wialon_host_data, "Wialon Host"),
            (merge_wialon_local_data, "Wialon Local"),
            (merge_scout_data, "Scout"),
            (merge_era_data, "ERA"),
        ]

        processes = []

        # Запуск потоков для каждой системы
        for func, name in monitoring_functions:
            process = multiprocessing.Process(target=monitor_system, args=(func, name))
            process.start()
            processes.append(process)

        # Ожидание завершения всех потоков
        for process in processes:
            process.join()

        logger.info("Все системы завершили работу.")

    schedule.every().day.at("19:40").do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)

    # job()
