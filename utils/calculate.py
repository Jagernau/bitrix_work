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

def get_user(vehicle_owner_id: str, users: list):
    for user in users:
        if user["agentGuid"] == vehicle_owner_id:
            return user["name"]
