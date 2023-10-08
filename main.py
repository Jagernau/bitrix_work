from data_entry import (
        merge_glonasssoft_data, 
        merge_fort_data, 
        merge_wialon_host_data, 
        merge_wialon_local_data, 
        merge_scout_data,
        merge_era_data
        )
from database.crud import (
        add_objects,
        add_one_object,
        delete_one_object,
        update_one_object,

        )
import schedule
import time


def job():
    add_objects(merge_glonasssoft_data())
    add_objects(merge_fort_data())
    add_objects(merge_wialon_host_data())
    add_objects(merge_wialon_local_data())
    add_objects(merge_scout_data())
    add_objects(merge_era_data())
    #add_one_object(merge_glonasssoft_data())
    #update_one_object(merge_glonasssoft_data())


if __name__ == '__main__':
    start_time = time.time()
    job()
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution time: {execution_time} seconds")
