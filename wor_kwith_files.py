import pandas as pd


def get_tele2_data():
    # read xlsx file
    df = pd.read_excel('tele2.xlsx')

    # data to list
    data = df.values.tolist()

    return data


def decorator_status(arg:str):
    "return active numbers"
    def wrapper(func) -> list:
        data = func()
        data_list = []
        for i in data:
            if i[3] == arg:
                data_list.append(str(i[2]))
        return data_list
    return wrapper

