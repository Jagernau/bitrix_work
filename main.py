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
        )

from database.crud import (
        add_objects,
        add_one_object,
        delete_one_object,
        update_one_object,
        add_clients_postgre,
        add_sys_mon_clients,
        add_one_sys_mon_client,
        )
import schedule
import time


def job():
    # add_objects(merge_glonasssoft_data())
    # add_objects(merge_fort_data())
    # add_objects(merge_wialon_host_data())
    # add_objects(merge_wialon_local_data())
    # add_objects(merge_scout_data())
    # add_objects(merge_era_data())

    glonasssoft_data = merge_glonasssoft_data()
    fort_data = merge_fort_data()
    wialon_host_data = merge_wialon_host_data()
    wialon_local_data = merge_wialon_local_data()
    scout_data = merge_scout_data()
    era_data = merge_era_data()


    add_one_object(glonasssoft_data)
    add_one_object(fort_data)
    add_one_object(wialon_host_data)
    add_one_object(wialon_local_data)
    add_one_object(scout_data)
    add_one_object(era_data)

    delete_one_object(glonasssoft_data)
    delete_one_object(fort_data)
    delete_one_object(wialon_host_data)
    delete_one_object(wialon_local_data)
    delete_one_object(scout_data)
    delete_one_object(era_data)

    update_one_object(glonasssoft_data)
    update_one_object(fort_data)
    update_one_object(wialon_host_data)
    update_one_object(wialon_local_data)
    update_one_object(scout_data)
    update_one_object(era_data)

    #update_one_object(merge_wialon_host_data())
    # add_clients_postgre(get_postgre_clients())
    #add_sys_mon_clients(generate_glonass_client())
    #add_one_sys_mon_client(generate_glonass_client())
    #add_sys_mon_clients(generate_fort_companys())

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
