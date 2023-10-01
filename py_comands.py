import sys
from parser import classes
from  configurations import config
import time
import os
from data_entry import (
        merge_glonasssoft_data, 
        merge_fort_data, 
        merge_wialon_host_data,
        merge_wialon_local_data, 
        )


if sys.argv[1] == 'get_json':
    if sys.argv[2] == 'glonass':
        glonasssoft = classes.Glonasssoft(str(config.GLONASS_LOGIN), str(config.GLONASS_PASSWORD))
        token = str(glonasssoft.token)
        if sys.argv[3] == 'objects':
            time.sleep(1)
            print(glonasssoft.get_glonasssoft_vehicles(token=token))
        if sys.argv[3] == 'agents':
            time.sleep(1)
            print(glonasssoft.get_glonasssoft_agents(token=token))
        if sys.argv[3] == 'users':
            time.sleep(1)
            print(glonasssoft.get_glonasssoft_users(token=token))
        if sys.argv[3] == 'merge':
            time.sleep(1)
            print(merge_glonasssoft_data())

    if sys.argv[2] == 'fort':
        fort = classes.Fort(str(config.FORT_LOGIN), str(config.FORT_PASSWORD))
        token = str(fort.token)
        if sys.argv[3] == 'objects':
            time.sleep(1)
            print(fort.get_fort_objects(token=token))
        if sys.argv[3] == 'companies':
            time.sleep(1)
            print(fort.get_fort_companies(token=token))
        if sys.argv[3] == 'groups_companies':
            time.sleep(1)
            print(fort.get_fort_objectgroup(token=token))
        if sys.argv[3] == 'groups_users':
            time.sleep(1)
            print(fort.get_fort_group_users(token=token))
        if sys.argv[3] == 'users':
            time.sleep(1)
            print(fort.get_fort_users(token=token))
        if sys.argv[3] == 'merge':
            time.sleep(1)
            print(merge_fort_data())

    if sys.argv[2] == 'whost':        
        wialon_data = classes.get_wialin_host_units_users(str(config.WIALON_HOST_TOKEN))
        if sys.argv[3] == 'units':
            time.sleep(1)
            print(wialon_data[0])
        if sys.argv[3] == 'users':
            time.sleep(1)
            print(wialon_data[1])
        if sys.argv[3] == 'merge':
            time.sleep(1)
            print(merge_wialon_host_data())

    if sys.argv[2] == 'wlocal':
        wialon_data = classes.get_wialin_local_units_users(str(config.WIALON_LOCAL_TOKEN))
        if sys.argv[3] == 'units':
            time.sleep(1)
            print(wialon_data[0])
        if sys.argv[3] == 'users':
            time.sleep(1)
            print(wialon_data[1])
        if sys.argv[3] == 'merge':
            time.sleep(1)
            print(merge_wialon_local_data())

    if sys.argv[2] == 'scout':
        time.sleep(1)
        scout = classes.Scout(str(config.SCOUT_LOGIN), str(config.SCOUT_PASSWORD))
        time.sleep(1)
        token = str(scout.token)
        if sys.argv[3] == "units":
            time.sleep(1)
            print(scout.get_scout_units(token=token))
