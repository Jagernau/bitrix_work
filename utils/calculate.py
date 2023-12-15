
def get_status(status: str):
    if "_новт" in status.lower():
        return int(1)
    elif "тест" in status.lower():
        return int(2)
    elif "_ппро" in status.lower():
        return int(4)
    elif "_приост" in status.lower():
        return int(5)
    elif "_пере" in status.lower():
        return int(6)
    else:
        return int(3)

def get_glonas_user(vehicle_owner_id: str, users: list):
    for user in users:
        if user["agentGuid"] == vehicle_owner_id:
            return user["name"]



def get_fort_user(company_name: str, users: list, companies):
    user_list = []
    for company in companies:
        if company["name"] == company_name:
            for user in users:
                if user["companyId"] == company["id"]:
                    user_list.append(user["name"])
    if len(user_list) >= 1:                    
        return user_list[0]
    else:
        return "НЕ ЗАПОЛНЕНО"

def get_fort_user_by_id(company_id, users: list, company_group):
    user_dict = {
            f"{company_group}": None,
            0: None,
            1: None,
            2: None,
            3: None,
            4: None,
            5: None,
            6: None,
            7: None,
            8: None,
            9: None,
            10: None,
            }
    count = 0
    for user in users:
        if user["companyId"] == company_id and user["email"] == company_group:
            user_dict[f"{company_group}"] = user["name"]

        if user["companyId"] == company_id:
            user_dict[count] = user["name"]
            count += 1
                            
    if user_dict[f"{company_group}"] != None:
        return user_dict[f"{company_group}"]
    else:
        return user_dict[0]

        

def get_fort_company(obj_group_id:int, companies: list, grops_companies):
    for group_company in grops_companies:
        if group_company["id"] == obj_group_id and group_company["companyId"] != 0:
            for company in companies:
                if company["id"] == group_company["companyId"]:
                    return company["id"]

        if group_company["id"] == obj_group_id and group_company["companyId"] == 0:
            parent = group_company["parentGroupId"]
            for group_company in grops_companies:
                if group_company["id"] == parent:
                    for company in companies:
                        if company["id"] == group_company["companyId"]:
                            return company["id"]


def get_fort_company_group(obj_group_id:int, grops_companies):
    for group_company in grops_companies:
        if group_company["id"] == obj_group_id:
            return group_company["name"]






def get_wialon_imei(field: dict):
    if len(field) == 0:
        return None
    else:
        result = ""
        for key in field:
            if field[key]["n"] == "IMEI" or field[key]["n"] == "imei":
                result = field[key]["v"]
                break
            else:
                result = None
        return result

def get_wialon_agent(field: dict):
    if len(field) == 0:
        return None
    else:
        result = ""
        for key in field:
            if field[key]["n"] == "Подразделение":
                result = field[key]["v"]
                break
            elif field[key]["n"] == "клиент" or field[key]["n"] == "Клиент":
                result = field[key]["v"]
                break
            else:
                result = None
        return result


def get_wialon_user(vehicle_owner_id: str, users: list):
    for user in users:
        if user["id"] == vehicle_owner_id:
            return user["nm"]

def generate_scout_user(unit_id: str, users: list):
    user_list = []
    for user in users:
        if unit_id in user["UnitIds"]:
            user_list.append(user["GroupName"])

    return user_list


def generate_era_company(group_id: str, companies):
    for company in companies:
        if group_id in company.id:
            return company.title


def generate_era_user(group_id, users):
    for user in users:
        if user.parentGroupId == group_id:
            return user.login



def generate_client_from_user(user_sysmon, users_in_db):
    for i in users_in_db:
        if user_sysmon == i[1]:
            return i[2]

