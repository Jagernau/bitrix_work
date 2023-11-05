from Levenshtein import ratio
import database.models as models
from database.database import Database
import re


def clear_func(value: str):
    value = value.replace("(ЭДО сс)", " ").replace("(СС)", " ").replace("(физ.лицо)", " ").replace("роуминг", " ").replace("фирма", " ")
    value = value.replace("  ", " ")
    value = re.sub(r'\W+', '', value)
    return value.lower().replace("ип", "").replace("эдо", "").replace("ооо", "").replace("тензор", "")

def bool_ratio(value1: str, value2: str):
    if ratio(value1, value2) > 0.95:
        return True
    
# def fisic_clients_clear(value: str):
#         value = clear_func(value)
#         split_value = value.split()
#         if len(split_value) > 2:
#                 return f"{split_value[0]} {split_value[1][0]} {split_value[2][0]}"
#         
#         


def join_user_client():
    session = Database().session
    users = session.query(models.LoginUser).filter(models.LoginUser.contragent_id == None).all()
    clients = session.query(models.Contragent.ca_id, models.Contragent.ca_name, models.Contragent.ca_shortname).all()
    session.close()
    for user in users:
        for client in clients:
           if bool_ratio(clear_func(str(user.client_name)), clear_func(str(client.ca_name))) or bool_ratio(clear_func(str(user.client_name)), clear_func(str(client.ca_shortname))):
# #            if bool_ratio(fisic_clients_clear(str(user.client_name)), fisic_clients_clear(str(client.ca_name))) or bool_ratio(fisic_clients_clear(str(user.client_name)), fisic_clients_clear(str(client.ca_shortname))):
                print(user.client_name, client.ca_name)
    #             session.query(models.LoginUser).filter(models.LoginUser.id == user.id).update({
    #                 "contragent_id": client.ca_id
    #             })
    # session.commit()
    # session.close()
# #
join_user_client()

# def first_clean():
#     """
#     Первое 100% совпадение
#     """
#     session = Database().session
#     users = session.query(models.LoginUser).all()
#     clients = session.query(models.Contragent).all()
#     session.close()
#     for user in users:
#         for client in clients:
#             if user.client_name == client.ca_name:
#                 session.query(models.LoginUser).filter(models.LoginUser.id == user.id).update({
#                     "contragent_id": client.ca_id
#                 })
#     session.commit()
#     session.close()
#
#
# def get_residual_counter_id():
#     session = Database().session
#     users = session.query(models.LoginUser).filter(models.LoginUser.contragent_id == None).all()
#     session.close()
#     results = ""
#     for user in users:
#         results += f"{user.client_name}---{user.login}" + "\n"
#     return results
# #
# print(get_residual_counter_id())
# with open("residual.txt", "w", encoding="utf-8") as f:
#     f.write(get_residual_counter_id())


#
# def second_clean():
#     session = Database().session
#     users = session.query(models.LoginUser).filter(models.LoginUser.contragent_id == None).all()
#     clients = session.query(models.Contragent).all()
#     session.close()
#     for user in users:
#         for client in clients:
#             if ratio(str(client.ca_name), str(user.client_name)) > 0.93:
#                 print(user.client_name, client.ca_name)
#                 session.query(models.LoginUser).filter(models.LoginUser.id == user.id).update({
#                     "contragent_id": client.ca_id
#                 })
#     session.commit()
#     session.close()
#
# second_clean()

#
# def third_clean():
#     session = Database().session
#     users = session.query(models.LoginUser).filter(models.LoginUser.contragent_id == None).all()
#     clients = session.query(models.Contragent).all()
#     session.close()
#
#     for user in users:
#         for client in clients:
#             split_name = str(user.client_name).split(" ")
#             if split_name[0] in client.ca_name:
#                 if len(split_name) > 1:
#                     if split_name[1] in client.ca_name:
#                         if ratio(str(client.ca_name), str(user.client_name)) > 0.75:
#                             print(user.client_name, client.ca_name)
#                             session.query(models.LoginUser).filter(models.LoginUser.id == user.id).update({
#                                 "contragent_id": client.ca_id
#                             })
#     session.commit()
#     session.close()
# #
# third_clean()

#
#
# def fourth_clean():
#     session = Database().session
#     users = session.query(models.LoginUser).filter(models.LoginUser.contragent_id == None).all()
#     clients = session.query(models.Contragent).all()
#     session.close()
#     for user in users:
#         for client in clients:
#             if ratio(
#                     str(client.ca_name.replace("ООО", "").replace("ЭДО", "").replace("ИП", "")), 
#                     str(user.client_name.replace("ООО", "").replace("ЭДО", "").replace("ИП", ""))) > 0.9:
#                 print(user.client_name, client.ca_name)
#                 session.query(models.LoginUser).filter(models.LoginUser.id == user.id).update({
#                     "contragent_id": client.ca_id
#                 })
#     session.commit()
#     session.close()
# #
# fourth_clean()
#
# def fifth_clean():
#     session = Database().session
#     users = session.query(models.LoginUser).filter(models.LoginUser.contragent_id == None).all()
#     clients = session.query(models.Contragent).all()
#     session.close()
#     
#     for user in users:
#         for client in clients:
#             if ratio(
#                     str(client.ca_name.replace("ООО", "").replace("ЭДО", "").replace("ИП", "")), 
#                     str(user.client_name.replace("ООО", "").replace("ЭДО", "").replace("ИП", ""))) > 0.8:
#                 split_client = client.ca_name.split(" ")
#                 split_user = user.client_name.split(" ")
#                 if split_client[0] in split_user:
#                     if len(split_client) > 1:
#                         if split_client[1] in split_user:
#                             print(user.client_name, client.ca_name)
#                             session.query(models.LoginUser).filter(models.LoginUser.id == user.id).update({
#                                 "contragent_id": client.ca_id
#                             })
#     session.commit()
#     session.close()
# fifth_clean()

#
# def six_clean():
#     session = Database().session
#     users = session.query(models.LoginUser).filter(models.LoginUser.contragent_id == None).all()
#     clients = session.query(models.Contragent).all()
#     session.close()
#     
#     for user in users:
#         for client in clients:
#             if ratio(
#                     str(client.ca_name.replace("ООО", "").replace("ЭДО", "").replace("ИП", "").replace(")", "").replace("(", "")), 
#                     str(user.client_name.replace("ООО", "").replace("ЭДО", "").replace("ИП", "").replace(")","").replace("(",""))) > 0.75:
#                 split_client = client.ca_name.split(" ")
#                 split_user = user.client_name.split(" ")
#                 if split_client[0] in split_user:
#                     if len(split_client) > 1:
#                         if split_client[1] in split_user:
#                             print(user.client_name, client.ca_name)
#                             session.query(models.LoginUser).filter(models.LoginUser.id == user.id).update({
#                                 "contragent_id": client.ca_id
#                             })
#     session.commit()
#     session.close()
# six_clean()
#
#
# def seven_clean():
#     session = Database().session
#     users = session.query(models.LoginUser).filter(models.LoginUser.contragent_id == None).all()
#     clients = session.query(models.Contragent).all()
#     session.close()
#     for user in users:
#         for client in clients:
#             if ratio(
#                     str(client.ca_name.replace("ООО", "").replace("ЭДО", "").replace("ИП", "").replace(")", "").replace("(", "")).lower(), 
#                     str(user.client_name.replace("ООО", "").replace("ЭДО", "").replace("ИП", "").replace(")", "").replace("(", "")).lower()) > 0.82:
#                             print(user.client_name, client.ca_name)
#                             session.query(models.LoginUser).filter(models.LoginUser.id == user.id).update({
#                                 "contragent_id": client.ca_id
#                             })
#     session.commit()
#     session.close()
#
# seven_clean()
#
# def sim_firs_clean():
#     session = Database().session
#     sims = session.query(models.SimCard).filter(models.SimCard.contragent_id == None).all()
#     clients = session.query(models.Contragent).all()
#     session.close()
#     for sim in sims:
#         for client in clients:
#             if sim.client_name == client.ca_name:
#                 session.query(models.SimCard).filter(models.SimCard.sim_id == sim.sim_id).update({
#                     "contragent_id": client.ca_id
#                 })
#     session.commit()
#     session.close()
#
# def sim_residual_counter_id():
#     session = Database().session
#     sims = session.query(models.SimCard).filter(models.SimCard.contragent_id == None).all()
#     session.close()
#     return len(sims)
#
#
# def sim_second_clean():
#     session = Database().session
#     sims = session.query(models.SimCard).filter(models.SimCard.contragent_id == None).all()
#     clients = session.query(models.Contragent).all()
#     session.close()
#     for sim in sims:
#         for client in clients:
#             if ratio(str(client.ca_name), str(sim.client_name)) > 0.92:
#                 session.query(models.SimCard).filter(models.SimCard.sim_id == sim.sim_id).update({
#                     "contragent_id": client.ca_id
#                 })
#     session.commit()
#     session.close()
#
#
# def sim_third_clean():
#     session = Database().session
#     sims = session.query(models.SimCard).filter(models.SimCard.contragent_id == None).all()
#     clients = session.query(models.Contragent).all()
#     session.close()
#
#     for sim in sims:
#         for client in clients:
#             split_name = str(sim.client_name).split(" ")
#             if split_name[0] in client.ca_name:
#                 if len(split_name) > 1:
#                     if split_name[1] in client.ca_name:
#                         if ratio(str(client.ca_name), str(sim.client_name)) > 0.7:
#                             session.query(models.SimCard).filter(models.SimCard.sim_id == sim.sim_id).update({
#                                 "contragent_id": client.ca_id
#                             })
#     session.commit()
#     session.close()
#
#
#
# def sim_fourth_clean():
#     session = Database().session
#     sims = session.query(models.SimCard).filter(models.SimCard.contragent_id == None).all()
#     clients = session.query(models.Contragent).all()
#     session.close()
#     for sim in sims:
#         for client in clients:
#             if ratio(
#                     str(str(client.ca_name).replace("ООО", "").replace("ЭДО", "").replace("ИП", "")), 
#                     str(str(sim.client_name).replace("ООО", "").replace("ЭДО", "").replace("ИП", ""))) > 0.9:
#                 session.query(models.SimCard).filter(models.SimCard.sim_id == sim.sim_id).update({
#                     "contragent_id": client.ca_id
#                 })
#     session.commit()
#     session.close()
#
#
# def sim_fifth_clean():
#     session = Database().session
#     sims = session.query(models.SimCard).filter(models.SimCard.contragent_id == None).all()
#     clients = session.query(models.Contragent).all()
#     session.close()
#     
#     for sim in sims:
#         for client in clients:
#             if ratio(
#                     str(str(client.ca_name).replace("ООО", "").replace("ЭДО", "").replace("ИП", "")), 
#                     str(str(sim.client_name).replace("ООО", "").replace("ЭДО", "").replace("ИП", ""))) > 0.8:
#                 split_client = client.ca_name.split(" ")
#                 split_sim = sim.client_name.split(" ")
#                 if split_client[0] in split_sim:
#                     if len(split_client) > 1:
#                         if split_client[1] in split_sim:
#                             session.query(models.SimCard).filter(models.SimCard.sim_id == sim.sim_id).update({
#                                 "contragent_id": client.ca_id
#                             })
#     session.commit()
#     session.close()
#
#
# def sim_seven_clean():
#     session = Database().session
#     sims = session.query(models.SimCard).filter(models.SimCard.contragent_id == None).all()
#     clients = session.query(models.Contragent).all()
#     session.close()
#     for sim in sims:
#         for client in clients:
#             if ratio(
#                     str(str(client.ca_name).replace("ООО", "").replace("ЭДО", "").replace("ИП", "").replace(")", "").replace("(", "")).lower(), 
#                     str(str(sim.client_name).replace("ООО", "").replace("ЭДО", "").replace("ИП", "").replace(")", "").replace("(", "")).lower()) > 0.82:
#                             session.query(models.SimCard).filter(models.SimCard.sim_id == sim.sim_id).update({
#                                 "contragent_id": client.ca_id
#                             })
#     session.commit()
#     session.close()
#
#
#
# print(sim_residual_counter_id())
# sim_seven_clean()
# print(sim_residual_counter_id())
#
#
