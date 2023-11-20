
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

# get num messgaes from a spesific user
def getSingleUser(num, user, channel):
    cursor.query("DROP DATABASE if exists slackTest;").execute()

    cursor.query("""CREATE DATABASE slackTest WITH ENGINE = 'slack', PARAMETERS = {
        "token": "xoxb-5954206853489-5964598795008-q50q9gWVAQDPvhRXju1e2DIB",
        "channel": "C05U262RF4H"};""").execute()
    
    res = cursor.query(f"Select text, user from slackTest.{channel} where user = \"{user}\" LIMIT {num};").execute()
    
    users = res.column_as_numpy_array("user")
    mes = res.column_as_numpy_array("text")


    Messagelist = ""

    for m in range(len(mes)-1, -1 , -1):
        x = f"{users[m]}: {mes[m]}"
        Messagelist = Messagelist + x + "\n"

    return Messagelist
    

# get num messgaes from a spesific user
def getGeneralMessages(num, channel):
    cursor.query("DROP DATABASE if exists slackTest;").execute()

    cursor.query("""CREATE DATABASE slackTest WITH ENGINE = 'slack', PARAMETERS = {
        "token": "xoxb-5954206853489-5964598795008-q50q9gWVAQDPvhRXju1e2DIB",
        "channel": "C05U262RF4H"};""").execute()
    
    res = cursor.query(f"Select text, user  from slackTest.{channel} LIMIT {num};").execute()

    users = res.column_as_numpy_array("user")
    mes = res.column_as_numpy_array("text")


    Messagelist = ""

    for m in range(len(mes)-1, -1 , -1):
        x = f"{users[m]}: {mes[m]}"
        Messagelist = Messagelist + x + "\n"

    return Messagelist