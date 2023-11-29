from Levenshtein import ratio
import database.models as models
from database.database import Database
import re

from data_entry import with_token_comand_put_get_glonasssoft
from parser.classes import Glonasssoft
from configurations import config

def clear_func(value: str):
    if value == None:
        return ""
    value = value.replace("(ЭДО сс)", " ").replace("(СС)", " ").replace("(физ.лицо)", " ").replace("роуминг", " ").replace("фирма", " ")
    value = value.replace("  ", " ")
    value = re.sub(r'\W+', '', value)
    return value.lower().replace("ип", "").replace("эдо", "").replace("ооо", "").replace("тензор", "")

def bool_ratio(value1: str, value2: str):
    if ratio(value1, value2) > 0.90:
        return True
    


def join_user_client():
    session = Database().session
    users = session.query(models.LoginUser).filter(models.LoginUser.contragent_id == None).all()
    clients = session.query(models.Contragent.ca_id, models.Contragent.ca_name, models.Contragent.ca_shortname).all()
    session.close()
    for user in users:
        for client in clients:
           if bool_ratio(
                   clear_func(str(user.client_name)), 
                   clear_func(str(client.ca_name))) \
           or bool_ratio(
                   clear_func(str(user.client_name)), 
                   clear_func(str(client.ca_shortname))):
                session.query(models.LoginUser).filter(models.LoginUser.id == user.id).update({
                    "contragent_id": client.ca_id
                })
    session.commit()
    session.close()


def join_sim_from_comands_glonass_navtelecom():
    """
    Опрашивает терминалы navtelecom, которые в базе данных на глонассофт
    какие ICCID у терминала и записывает в таблицу симок imei по ICCID
    """
    glonass = Glonasssoft(str(config.GLONASS_LOGIN), str(config.GLONASS_PASSWORD))
    command_iccid = "*?ICCID"
    token_glonass = str(glonass.token)
    session = Database().session
    objects = session.query(models.CaObject.imei).filter(models.CaObject.imei != None, models.CaObject.sys_mon_id == 1).all()
    session.close()
    imei_set = set()
    for object in objects:
        pattern = r"86\d{13}"
        if re.search(pattern, str(object.imei)):
            imei_set.add(object.imei)
    list_imei = list(imei_set)
    data = with_token_comand_put_get_glonasssoft(
            token_glonass=token_glonass,
            command_glonass=command_iccid,
            imei_glonas="866192034294932",
            )
    return data


def join_devices_client():
    session = Database().session
    clients = session.query(models.Contragent.ca_id, models.Contragent.ca_name, models.Contragent.ca_shortname).all()
    devices = session.query(models.Device).filter(models.Device.contragent_id == None).all()
    session.close()
    for client in clients:
        for device in devices:
            if device.client_name == client.ca_name \
            or bool_ratio(
                    clear_func(str(device.client_name)),
                    clear_func(str(client.ca_name))) \
            or bool_ratio(
                    clear_func(str(device.client_name)),
                    clear_func(str(client.ca_shortname))):
                session.query(models.Device).filter(models.Device.device_id == device.device_id).update({
                    "contragent_id": client.ca_id
                })

join_devices_client()


# def get_residual_counter_id():
#     session = Database().session
#     users = session.query(models.LoginUser).filter(models.LoginUser.contragent_id == None).all()
#     session.close()
#     # results = ""
#     # for user in users:
#     #     results += f"{user.client_name}---{user.login}" + "\n"
#     return len(users)
# #
# print(get_residual_counter_id())
# # with open("residual.txt", "w", encoding="utf-8") as f:
# #     f.write(get_residual_counter_id())


# def fisic_clients_clear(value: str):
#         value = clear_func(value)
#         split_value = value.split()
#         if len(split_value) > 2:
#                 return f"{split_value[0]} {split_value[1][0]} {split_value[2][0]}"
#         
#         

# def sim_firs_clean():
#     session = Database().session
#     sims = session.query(models.SimCard).filter(models.SimCard.contragent_id == None, models.SimCard.client_name != None).all()
#     clients = session.query(models.Contragent).all()
#     # objects = session.query(
#     #         models.CaObject.contragent_id, 
#     #         models.CaObject.contragent_name
#     #         ).filter(
#     #             models.CaObject.contragent_id != None,
#     #             models.CaObject.contragent_name != None,
#     #             ).all()
#     session.close()
#     for sim in sims:
#         # for obj in objects:
#         #     if bool_ratio(
#         #             clear_func(sim.client_name), 
#         #             clear_func(obj.contragent_name))\
#         #     or bool_ratio(
#         #             clear_func(sim.client_name),
#         #             clear_func(obj.contragent_name)):
#         #         print(f"{sim.client_name}---{obj.contragent_name}")
#                 # session.query(models.SimCard).filter(models.SimCard.sim_id == sim.sim_id).update({
#                 #     "contragent_id": obj.contragent_id
#                 # })
#
#
#         for client in clients:
#             if bool_ratio(
#                     clear_func(sim.client_name), 
#                     clear_func(client.ca_name))\
#             or bool_ratio(
#                     clear_func(sim.client_name),
#                     clear_func(client.ca_shortname)):
#                 print(f"{sim.client_name}---{client.ca_name}")
#     #             session.query(models.SimCard).filter(models.SimCard.sim_id == sim.sim_id).update({
    #                 "contragent_id": client.ca_id
    #             })
    # session.commit()
    # session.close()



# def sim_residual_counter_id():
#     session = Database().session
#     sims = session.query(models.SimCard).filter(
#             models.SimCard.contragent_id == None,
#             #models.SimCard.client_name != None
#             ).all()
#     session.close()
#     return len(sims)
# #
# print(sim_residual_counter_id())
