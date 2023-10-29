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

import socket

computer_name = str(socket.gethostname())


def glonass_object_data():
    glonasssoft_data = merge_glonasssoft_data()
    #add_objects(glonasssoft_data)
    add_one_object(glonasssoft_data)
    delete_one_object(glonasssoft_data)
    update_one_object(glonasssoft_data)

def fort_object_data():
    fort_data = merge_fort_data()
    #add_objects(fort_data)
    add_one_object(fort_data)
    delete_one_object(fort_data)
    update_one_object(fort_data)

def whost_object_data():
    wialon_host_data = merge_wialon_host_data()
    #add_objects(wialon_host_data)
    add_one_object(wialon_host_data)
    delete_one_object(wialon_host_data)
    update_one_object(wialon_host_data)

def wlocal_object_data():
    wialon_local_data = merge_wialon_local_data()
    #add_objects(wialon_local_data)
    add_one_object(wialon_local_data)
    delete_one_object(wialon_local_data)
    update_one_object(wialon_local_data)

def scout_object_data():
    scout_data = merge_scout_data()
    #add_objects(scout_data)
    add_one_object(scout_data)
    delete_one_object(scout_data)
    update_one_object(scout_data)

def era_object_data():
    era_data = merge_era_data()
    #add_objects(era_data)
    add_one_object(era_data)
    delete_one_object(era_data)
    update_one_object(era_data)

def glonass_clients_data():
    glonass_clients = generate_glonass_client()
    #add_sys_mon_clients(glonass_clients)
    add_one_sys_mon_client(glonass_clients)
    delete_one_sys_mon_client(glonass_clients)
    update_one_sys_mon_client(glonass_clients)

def fort_clients_data():
    fort_clients = generate_fort_companys()
    #add_sys_mon_clients(fort_clients)
    add_one_sys_mon_client(fort_clients)
    delete_one_sys_mon_client(fort_clients)
    update_one_sys_mon_client(fort_clients)

def wialon_host_users_data():
    wialon_host_users = generate_wialon_host_users()
    #add_sys_mon_clients(wialon_host_users)
    add_one_sys_mon_client(wialon_host_users)
    delete_one_sys_mon_client(wialon_host_users)
    update_one_sys_mon_client(wialon_host_users)

def wialon_local_users_data():
    wialon_local_users = generate_wialon_local_users()
    #add_sys_mon_clients(wialon_local_users)
    add_one_sys_mon_client(wialon_local_users)
    delete_one_sys_mon_client(wialon_local_users)
    update_one_sys_mon_client(wialon_local_users)


def onec_clients_data():
    if computer_name != "max-SWH":
        clients_oneC = get_onec_clients()
        # add_all_clients_oneC(clients_oneC)
        add_one_oneC_clients(clients_oneC)
        # delete_one_oneC_client(clients_oneC)
        update_one_oneC_client(clients_oneC)
    else:
        print("Невозможно добавить клиентов на компьютере max-SWH")
 

def execute_functions(functions):
    if not functions:
        return 

    try:
        current_function = functions[0]
        current_function()
        print(f"**********Выполнена функция {current_function.__name__}")
    except:
        print(f"Ошибка в функции {functions[0].__name__}")
        execute_functions(functions[1:])
    else:
        execute_functions(functions[1:])
            
            

def job():
    functions = [
        glonass_object_data,
        fort_object_data,
        whost_object_data,
        wlocal_object_data,
        scout_object_data,
        era_object_data,
        glonass_clients_data,
        fort_clients_data,
        wialon_host_users_data,
        wialon_local_users_data,
        onec_clients_data
    ]
    execute_functions(functions)
        

   


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
