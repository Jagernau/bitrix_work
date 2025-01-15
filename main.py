from data_entry import (
        get_onec_clients,
        get_onec_contracts,
        get_onec_contacts
        )

from database.crud import (
        add_one_oneC_contracts,
        add_one_oneC_clients,
        update_one_oneC_client,
        add_one_oneC_contracts,
        update_one_oneC_contracts,
        add_one_oneC_contacts,
        update_one_oneC_contacts
        )

import schedule
import time
import logging

#Логгер

# Создание и настройка логгера
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Создание обработчика для записи в файл
file_handler = logging.FileHandler('log.txt')
file_handler.setLevel(logging.INFO)

# Создание форматировщика
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Добавление обработчика к логгеру
logger.addHandler(file_handler)



def job():

        try:
            logger.info("Клиенты 1С начало получения")
            clients_oneC = get_onec_clients()
            logger.info("Клиенты 1С конец получения")

            logger.info("Клиенты 1С начал добавлять")
            add_one_oneC_clients(clients_oneC)
            logger.info("Клиенты 1С окончил добавлять")

            logger.info("Клиенты 1С начали обновляться")
            update_one_oneC_client(clients_oneC)
            logger.info("Клиенты 1С закончили обновляться")

            logger.info("Клиенты OneC успешно обновлены")
        except Exception as e:
            logger.error(f"В обновлении клиентов OneC возникла ошибка: {e}")


        try:

            logger.info("Договоры 1С начало получения")
            contracts_oneC = get_onec_contracts()
            logger.info("Договоры 1С конец получения")

            logger.info("Договоры 1С начал добавлять")
            add_one_oneC_contracts(contracts_oneC)
            logger.info("Договоры 1С окончил добавлять")

            logger.info("Договоры 1С начали обновляться")
            update_one_oneC_contracts(contracts_oneC)
            logger.info("Договоры 1С закончили обновляться")

            logger.info("Договоры OneC успешно обновлены")
        except Exception as e:
            logger.error(f"В обновлении Договоры OneC возникла ошибка: {e}")


        try:

            logger.info("Контакты 1С начало получения")
            contacts_oneC = get_onec_contacts()
            logger.info("Контакты 1С конец получения")
            
            logger.info("Контакты 1С начал добавлять")
            add_one_oneC_contacts(contacts_oneC)
            logger.info("Контакты 1С окончил добавлять")

            logger.info("Контакты 1С начали обновляться")
            update_one_oneC_contacts(contacts_oneC)
            logger.info("Контакты 1С закончили обновляться")

            logger.info("Контакты OneC успешно обновлены")
        except Exception as e:
            logger.error(f"В обновлении Контактов OneC возникла ошибка: {e}")

if __name__ == '__main__':

    # start_time = time.time()
    # print(start_time)
    # job()
    # end_time = time.time()
    # print(end_time)
    # execution_time = end_time - start_time
    # print(f"Execution time: {execution_time} seconds")

    schedule.every().day.at("17:40").do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)
