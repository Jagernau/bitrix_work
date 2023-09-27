def get_status(status: str):
    if "_новт" in status.lower():
        return int(1)
    elif "_тест" in status.lower():
        return int(2)
    elif "_ппрог" in status.lower():
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
    return user_list


def get_fort_company(obj_group_id:int, companies: list, grops_companies):
    for group_company in grops_companies:
        if group_company["id"] == obj_group_id and group_company["companyId"] != 0:
            for company in companies:
                if company["id"] == group_company["companyId"]:
                    return company["name"]

        if group_company["id"] == obj_group_id and group_company["companyId"] == 0:
            parent = group_company["parentGroupId"]
            for group_company in grops_companies:
                if group_company["id"] == parent:
                    for company in companies:
                        if company["id"] == group_company["companyId"]:
                            return company["name"]
    

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


