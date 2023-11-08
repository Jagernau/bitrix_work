from data_entry import (
        merge_glonasssoft_data, 
        merge_fort_data, 
        merge_wialon_host_data, 
        merge_wialon_local_data, 
        merge_scout_data,
        merge_era_data,
        get_postgre_clients,
        generate_glonass_client,
        generate_fort_companys,
        generate_wialon_host_users,
        generate_wialon_local_users,
        get_onec_clients,
        )

from database.crud import (
        add_objects,
        add_one_object,
        delete_one_object,
        update_one_object,
        add_clients_postgre,
        add_sys_mon_clients,
        add_one_sys_mon_client,
        update_one_sys_mon_client,
        delete_one_sys_mon_client,
        add_all_clients_oneC,
        add_one_oneC_clients,
        delete_one_oneC_client,
        update_one_oneC_client,
        )
import schedule
import time
import logging

import socket

computer_name = str(socket.gethostname())

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
        glonasssoft_data = merge_glonasssoft_data()
        #add_objects(glonasssoft_data)
        add_one_object(glonasssoft_data)
        delete_one_object(glonasssoft_data)
        update_one_object(glonasssoft_data)
        logger.info("Глонасссофт успешно обновлен")

    except Exception as e:
        logger.error(f"В обновлении Глонасссофтов возникла ошибка: {e}")


    try:
        fort_data = merge_fort_data()
        #add_objects(fort_data)
        add_one_object(fort_data)
        delete_one_object(fort_data)
        update_one_object(fort_data)
        logger.info("ФОРТ успешно обновлен")
    except Exception as e:
        logger.error(f"В обновлении ФОРТ возникла ошибка: {e}")

    try:
        wialon_host_data = merge_wialon_host_data()
        #add_objects(wialon_host_data)
        add_one_object(wialon_host_data)
        delete_one_object(wialon_host_data)
        update_one_object(wialon_host_data)
        logger.info("Вайлон хост успешно обновлен")
    except Exception as e:
        logger.error(f"В обновлении Вайлон хоста возникла ошибка: {e}")

    try:
        wialon_local_data = merge_wialon_local_data()
        #add_objects(wialon_local_data)
        add_one_object(wialon_local_data)
        delete_one_object(wialon_local_data)
        update_one_object(wialon_local_data)
        logger.info("Вайлон локаль успешно обновлен")
    except Exception as e:
        logger.error(f"В обновлении Вайлон локаль возникла ошибка: {e}")

    try:
        scout_data = merge_scout_data()
        #add_objects(scout_data)
        add_one_object(scout_data)
        delete_one_object(scout_data)
        update_one_object(scout_data)
        logger.info("Скаут успешно обновлен")
    except Exception as e:
        logger.error(f"В обновлении Скаута возникла ошибка: {e}")

    try:
        era_data = merge_era_data()
        #add_objects(era_data)
        add_one_object(era_data)
        delete_one_object(era_data)
        update_one_object(era_data)
        logger.info("Эра успешно обновлен")
    except Exception as e:
        logger.error(f"В обновлении Эра возникла ошибка: {e}")

    try:
        glonass_clients = generate_glonass_client()
        #add_sys_mon_clients(glonass_clients)
        add_one_sys_mon_client(glonass_clients)
        delete_one_sys_mon_client(glonass_clients)
        update_one_sys_mon_client(glonass_clients)
        logger.info("Хозяева Глонасс успешно обновлены")
    except Exception as e:
        logger.error(f"В обновлении Хозяев Глонасс возникла ошибка: {e}")

    try:
        fort_clients = generate_fort_companys()
        #add_sys_mon_clients(fort_clients)
        add_one_sys_mon_client(fort_clients)
        delete_one_sys_mon_client(fort_clients)
        update_one_sys_mon_client(fort_clients)
        logger.info("Хозяева ФОРТ успешно обновлены")
    except Exception as e:
        logger.error(f"В обновлении Хозяев ФОРТ возникла ошибка: {e}")

    try:
        wialon_host_users = generate_wialon_host_users()
        #add_sys_mon_clients(wialon_host_users)
        add_one_sys_mon_client(wialon_host_users)
        delete_one_sys_mon_client(wialon_host_users)
        update_one_sys_mon_client(wialon_host_users)
        logger.info("Хозяева Вайлон хост успешно обновлены")
    except Exception as e:
        logger.error(f"В обновлении Хозяев Вайлон хост возникла ошибка: {e}")

    try:
        wialon_local_users = generate_wialon_local_users()
        #add_sys_mon_clients(wialon_local_users)
        add_one_sys_mon_client(wialon_local_users)
        delete_one_sys_mon_client(wialon_local_users)
        update_one_sys_mon_client(wialon_local_users)
        logger.info("Хозяева Вайлон локаль успешно обновлены")
    except Exception as e:
        logger.error(f"В обновлении Хозяев Вайлон локаль возникла ошибка: {e}")


        if computer_name != "max-SWH":

            try:
                clients_oneC = get_onec_clients()
                # add_all_clients_oneC(clients_oneC)
                add_one_oneC_clients(clients_oneC)
                # delete_one_oneC_client(clients_oneC)
                update_one_oneC_client(clients_oneC)
                logger.info("Клиенты OneC успешно обновлены")
            except Exception as e:
                logger.error(f"В обновлении клиентов OneC возникла ошибка: {e}")


  


if __name__ == '__main__':

    # start_time = time.time()
    # job()
    # end_time = time.time()
    # execution_time = end_time - start_time
    # print(f"Execution time: {execution_time} seconds")

    schedule.every().day.at("03:20").do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)
