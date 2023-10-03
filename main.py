from data_entry import merge_glonasssoft_data, merge_fort_data, merge_wialon_host_data, merge_wialon_local_data, merge_scout_data
from database.crud import add_objects, add_one_object
import schedule

def job():
    # add_objects(merge_glonasssoft_data())
    # add_objects(merge_fort_data())
    # add_objects(merge_wialon_host_data())
    # add_objects(merge_wialon_local_data())
    add_objects(merge_scout_data())


if __name__ == '__main__':
    job()
