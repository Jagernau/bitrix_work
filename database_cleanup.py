from Levenshtein import ratio
import database.models as models
from database.database import Database

def first_clean():
    """
    Первое 100% совпадение
    """
    session = Database().session
    users = session.query(models.LoginUser).all()
    clients = session.query(models.Contragent).all()
    session.close()
    for user in users:
        for client in clients:
            if user.client_name == client.ca_name:
                session.query(models.LoginUser).filter(models.LoginUser.id == user.id).update({
                    "contragent_id": client.ca_id
                })
    session.commit()
    session.close()

#first_clean()


def get_residual_counter_id():
    session = Database().session
    users = session.query(models.LoginUser).filter(models.LoginUser.contragent_id == None).all()
    session.close()
    return len(users)

def second_clean():
    session = Database().session
    users = session.query(models.LoginUser).filter(models.LoginUser.contragent_id == None).all()
    clients = session.query(models.Contragent).all()
    session.close()
    for user in users:
        for client in clients:
            if ratio(str(client.ca_name), str(user.client_name)) > 0.92:
                session.query(models.LoginUser).filter(models.LoginUser.id == user.id).update({
                    "contragent_id": client.ca_id
                })
    session.commit()
    session.close()


def third_clean():
    session = Database().session
    users = session.query(models.LoginUser).filter(models.LoginUser.contragent_id == None).all()
    clients = session.query(models.Contragent).all()
    session.close()

    for user in users:
        for client in clients:
            split_name = str(user.client_name).split(" ")
            if split_name[0] in client.ca_name:
                if len(split_name) > 1:
                    if split_name[1] in client.ca_name:
                        if ratio(str(client.ca_name), str(user.client_name)) > 0.7:
                            session.query(models.LoginUser).filter(models.LoginUser.id == user.id).update({
                                "contragent_id": client.ca_id
                            })
    session.commit()
    session.close()



def fourth_clean():
    session = Database().session
    users = session.query(models.LoginUser).filter(models.LoginUser.contragent_id == None).all()
    clients = session.query(models.Contragent).all()
    session.close()
    for user in users:
        for client in clients:
            if ratio(
                    str(client.ca_name.replace("ООО", "").replace("ЭДО", "").replace("ИП", "")), 
                    str(user.client_name.replace("ООО", "").replace("ЭДО", "").replace("ИП", ""))) > 0.9:
                session.query(models.LoginUser).filter(models.LoginUser.id == user.id).update({
                    "contragent_id": client.ca_id
                })
    session.commit()
    session.close()



def fifth_clean():
    session = Database().session
    users = session.query(models.LoginUser).filter(models.LoginUser.contragent_id == None).all()
    clients = session.query(models.Contragent).all()
    session.close()
    
    for user in users:
        for client in clients:
            if ratio(
                    str(client.ca_name.replace("ООО", "").replace("ЭДО", "").replace("ИП", "")), 
                    str(user.client_name.replace("ООО", "").replace("ЭДО", "").replace("ИП", ""))) > 0.8:
                split_client = client.ca_name.split(" ")
                split_user = user.client_name.split(" ")
                if split_client[0] in split_user:
                    if len(split_client) > 1:
                        if split_client[1] in split_user:
                            session.query(models.LoginUser).filter(models.LoginUser.id == user.id).update({
                                "contragent_id": client.ca_id
                            })
    session.commit()
    session.close()




def six_clean():
    session = Database().session
    users = session.query(models.LoginUser).filter(models.LoginUser.contragent_id == None).all()
    clients = session.query(models.Contragent).all()
    session.close()
    
    for user in users:
        for client in clients:
            if ratio(
                    str(client.ca_name.replace("ООО", "").replace("ЭДО", "").replace("ИП", "").replace(")", "").replace("(", "")), 
                    str(user.client_name.replace("ООО", "").replace("ЭДО", "").replace("ИП", "").replace(")","").replace("(",""))) > 0.75:
                split_client = client.ca_name.split(" ")
                split_user = user.client_name.split(" ")
                if split_client[0] in split_user:
                    if len(split_client) > 1:
                        if split_client[1] in split_user:
                            session.query(models.LoginUser).filter(models.LoginUser.id == user.id).update({
                                "contragent_id": client.ca_id
                            })
    session.commit()
    session.close()



def seven_clean():
    session = Database().session
    users = session.query(models.LoginUser).filter(models.LoginUser.contragent_id == None).all()
    clients = session.query(models.Contragent).all()
    session.close()
#    result = ""
    for user in users:
        for client in clients:
            if ratio(
                    str(client.ca_name.replace("ООО", "").replace("ЭДО", "").replace("ИП", "").replace(")", "").replace("(", "")).lower(), 
                    str(user.client_name.replace("ООО", "").replace("ЭДО", "").replace("ИП", "").replace(")", "").replace("(", "")).lower()) > 0.82:
                            session.query(models.LoginUser).filter(models.LoginUser.id == user.id).update({
                                "contragent_id": client.ca_id
                            })
    session.commit()
    session.close()

print(get_residual_counter_id())


#                             result += f'\n{user.login} {user.client_name} {client.ca_name} {ratio(str(client.ca_name.replace("ООО", "").replace("ЭДО", "").replace("ИП", "").replace(")", "").replace("(", "")).lower(), str(user.client_name.replace("ООО", "").replace("ЭДО", "").replace("ИП", "").replace(")", "").replace("(", "")).lower())}\n'
#     return result
#
# with open("seven_clean_82.txt", "w") as f:
#      f.write(seven_clean())
