import requests
import sqlite3

# connect DB
con = sqlite3.connect("program.db")
cur = con.cursor()

""" Create database and table if not exists
    asks the user for a command
    apply filters, parse API
    filters and write the result to the local database
    if the user enters "program list", we show the last 5 actions
"""

class BoredAPIWrapper:
    def __init__(self, name, type, participants, price_min, price_max, accessibility_min, accessibility_max):
        self.name = name
        self.type = type
        self.participants = participants
        
        self.price_min  = price_min
        self.price_max = price_max

        self.accessibility_min = accessibility_min
        self.accessibility_max = accessibility_max

        self.result_response = None

    
    def dataBase(self, user_filters):

        # Create TABLES
        cur.execute("""CREATE TABLE IF NOT EXISTS commands(
            filters TEXT,
            result TEXT
        )""")

        # checking duplicate
        cur.execute("SELECT * FROM commands WHERE filters = ?", (user_filters,))
        filters = cur.fetchone()
        con.commit()

        if not filters:

            # save if not duplicate
            cur.execute("INSERT INTO commands (filters, result) VALUES (?, ?);", (user_filters, str(self.result_response)))
            con.commit()


    def parse(self):
        response = requests.get(
            f"https://www.boredapi.com/api/activity?type={self.type}&participants={self.participants}&minprice={self.price_min}&maxprice={self.price_max}&minaccessibility={self.accessibility_min}&maxaccessibility={self.accessibility_max}"
        )

        if response.status_code == 200:    
            self.result_response = response.json()
            print(self.result_response)
        else:
            print(response.status_code)


# type filters
user_filters = input("Input filters: ").split()

if user_filters[1] == "new":

    dict_filters = {}

    parameters = user_filters[0::2]
    values = user_filters[1::2]

    # add dict 
    for i in range(len(parameters)):
        parameter = parameters[i]
        value = values[i]

        dict_filters[parameter.replace("-", "")] = value


    values = list(dict_filters.values())
    method = BoredAPIWrapper(*values)

    method.parse()
    method.dataBase(" ".join(user_filters[2:]))


elif user_filters[1] == "list":
    # get last 5 commands from tables
    cur.execute("SELECT * FROM commands ORDER BY ROWID DESC LIMIT 5")
    last_five_filters = cur.fetchall()
    
    # result
    for row in last_five_filters:
        print(row)
    
    con.commit()
else:
    print("Error command")