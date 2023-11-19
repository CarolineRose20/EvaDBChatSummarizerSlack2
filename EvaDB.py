
import os
from slack_sdk import WebClient 
import ssl
import certifi
import evadb

SLACK_TOKEN = os.environ.get('SLACK_BOT_TOKEN')
CHANNEL_ID = "C05TGT8N1DL" #<<<<< CHANGE THIS TO THE CHANNEL YOU WANT THE BOT TO EXSIST ON
BOT_ID = "U05UCHLPD08" #<<<<< CHANAGE THIS TO YOUR BOT ID

# Setting up EvaDB and Slack API so we can see channel history
cursor = evadb.connect().cursor()
ssl_context = ssl.create_default_context(cafile=certifi.where())
client = WebClient(token=SLACK_TOKEN, ssl=ssl_context)

# This will run when the server starts and will initialize and fill in the table we will need

# If the user table does not exsist add it
try:
    test = cursor.query("Select * from UserTable").execute()
except:
    # Table Does no exsist so initialize it
    cursor.query("DROP TABLE IF EXISTS UserTable;").execute()
    cursor.query(f"CREATE TABLE UserTable (id TEXT(100), username TEXT(1000));").execute()

    result = client.users_list()

    for user in result['members']:
        cursor.query(f"""
            INSERT INTO UserTable (id, username)
            VALUES ('{user['id']}', '{user['name']}');
        """).execute()

# If the message table does not exsist add it
try:
    test = cursor.query("Select * from MessageTable").execute()
except:
    # Table Does not exsist so initialize it
    res = client.conversations_history(channel=CHANNEL_ID)
    cursor.query("DROP TABLE IF EXISTS MessageTable;").execute()
    cursor.query(f"CREATE TABLE MessageTable (timestamp FLOAT(12,7), user TEXT(1000), message TEXT(1000));").execute()

    for message in res['messages']:
        if (message['type'] == 'message' and message.get('subtype') == None):
            result = float(message['ts'].strip(' "'))
            mes = message['text']
            phrase = ""
            phrase = phrase + mes
            mes = phrase.replace("'", "" )
            if (message['user'] != BOT_ID):
                cursor.query(f"""
                INSERT INTO MessageTable (timestamp, user, message)
                VALUES ({result}, "{message['user']}", '{mes}');
                """).execute()


# get num messgaes from a spesific user
def getSingleUser(num, user):
    test = cursor.query(f"Select message, T1.username from MessageTable Inner Join (Select * from UserTest where id='{user}') as T1 on user = T1.id order by timestamp desc limit {num};").execute()

    users = test.column_as_numpy_array("T1.username")
    mes = test.column_as_numpy_array("Inner.message")


    Messagelist = ""

    for m in range(len(mes)-1, -1 , -1):
        x = f"{users[m]}: {mes[m]}"
        Messagelist = Messagelist + x + "\n"

    return Messagelist

# get num messgaes from a spesific user
def getGeneralMessages(num):
    test = cursor.query(f"SELECT message, username FROM MessageTable Inner Join UserTable on user = id order by timestamp desc limit 5;").execute()

    users = test.column_as_numpy_array("usertable.username")
    mes = test.column_as_numpy_array("Inner.message")


    Messagelist = ""

    for m in range(len(mes)-1, -1 , -1):
        x = f"{users[m]}: {mes[m]}"
        Messagelist = Messagelist + x + "\n"

    return Messagelist

# Add a new message to Message Table
def addMessage(ts, user, mes):
    cursor.query(f"""
            INSERT INTO MessageTable (timestamp, user, message)
            VALUES ({ts}, '{user}', '{mes}');
            """).execute()
    q = cursor.query("Select * from MessageTable order by timestamp desc").execute()

# Edit an existing message in the Table
def updateMessage(ts, user, mes):
    cursor.query(f""" Update MessageTable set message = '{mes}' where user = '{user}' AND timestamp = {ts} """)
    q = cursor.query("Select * from MessageTable order by timestamp desc").execute()

# Delete a messgage from Message Table
def removeMessage(ts, user):
    cursor.query(f"""Delete from MessageTable where user = '{user}' AND timestamp = {ts}""").execute()
    q = cursor.query("Select * from MessageTable order by timestamp desc").execute()

# Reset the user and message tables
def reset():
    cursor.query("DROP TABLE IF EXISTS UserTable;").execute()
    cursor.query(f"CREATE TABLE UserTable (id TEXT(100), username TEXT(1000));").execute()

    result = client.users_list()

    for user in result['members']:
        cursor.query(f"""
            INSERT INTO UserTable (id, username)
            VALUES ('{user['id']}', '{user['name']}');
        """).execute()

    res = client.conversations_history(channel=CHANNEL_ID)
    cursor.query("DROP TABLE IF EXISTS MessageTable;").execute()
    cursor.query(f"CREATE TABLE MessageTable (timestamp FLOAT(12,7), user TEXT(1000), message TEXT(1000));").execute()

    for message in res['messages']:
        if (message['type'] == 'message' and message.get('subtype') == None):
            result = float(message['ts'].strip(' "'))
            mes = message['text']
            phrase = ""
            phrase = phrase + mes
            mes = phrase.replace("'", "" )
            if (message['user'] != BOT_ID):
                cursor.query(f"""
                INSERT INTO MessageTable (timestamp, user, message)
                VALUES ({result}, "{message['user']}", '{mes}');
                """).execute()

    q = cursor.query("Select * from MessageTable").execute()
    print(q)
