from flask import Flask, request
from slack_bolt.adapter.flask import SlackRequestHandler

import EvaDB
import ChatBot
from slack_sdk import WebClient 
import ssl
import certifi
import os

SLACK_TOKEN = os.environ.get('SLACK_BOT_TOKEN')
ssl_context = ssl.create_default_context(cafile=certifi.where())
client = WebClient(token=SLACK_TOKEN, ssl=ssl_context)

working = 0

app = Flask(__name__)

# This is the app route that will decode the request from Slack
# There are three distinct things we are looking for
# 1) A message is added to the slack channel
# 2) A message is deleted from the slack channel
# 3) The slack bot is asked to summarize something
@app.route("/slack", methods=["POST"])
def slack_events():
    # print(request.get_json())
    # Get the data from the request
    r = request.get_json()
    global working

    # This is to check varification when setting up events in slack
    # It will send the required challenge back to slack and verify the server
    if (r.get("challenge") != None):
        return r.get("challenge")
    
    # Get the event data
    event = r.get("event")

    # Check if you are tagging the bot
    if (event != None and event.get("type") == "app_mention"):
        if (working == 0):
            working = 1
            try:
                print("Getting Summary")

                # Remove Message from Message Table
                ts = float(r.get("event").get('ts').strip(' "'))
                user = r.get("event").get('user')
                EvaDB.removeMessage(ts, user)

                el = event.get("blocks")[0].get("elements")[0].get("elements")
                # Check if the request is for general messages or a reset
                if (len(el) == 2):
                    num = el[1].get("text")
                    if (num == " reset"):
                        print("Test")
                        EvaDB.reset()
                        working = 0
                        return "Sucsess"
                    messages = EvaDB.getGeneralMessages(num[1])
                    response = client.chat_postMessage(
    				    channel="testingbot",
    				    text="I am woking on the summary. It may take a few minutes for GPT4ALL to give a response.")
                    text  = ""
                    if (int(num[1]) > 1):
                        text = ChatBot.multipleMessages(messages)
                    else:
                        text = ChatBot.singleMessage(messages)
                    response = client.chat_postMessage(
                        channel="testingbot",
                        text="Summary: " + text)
                    print("Summary Done")
                #Check if the request is for a spesific user
                elif (len(el) == 4):
                    userid = el[2].get("user_id")
                    num = el[3].get("text")
                    messages = EvaDB.getSingleUser(num[1], userid)
                    response = client.chat_postMessage(
                        channel="testingbot",
                        text="I am woking on the summary. It may take a few minutes for GPT4ALL to give a response.")
                    text  = ""
                    if (int(num[1]) > 1):
                        text = ChatBot.multipleMessages(messages)
                    else:
                        text = ChatBot.singleMessage(messages)
                    response = client.chat_postMessage(
                        channel="testingbot",
                        text="Summary: " + text)
                    print("Summary Done")
                else:
                    text = """Somthing in the formatting was wrong. Try again with the correct formatting.
                    For getting a simgle users message use @BotName @User (num of responses wanted)
                    For getting the last x messages in chat use @BotName (num of responses wanted)"""
                    response = client.chat_postMessage(
                        channel="testingbot",
                        text="Error: " + text)
                working = 0
            except Exception as e:
                print(e)
                text = """Somthing in the formatting was wrong. Try again with the correct formatting.
                    For getting a simgle users message use @BotName @User (num of responses wanted)
                    For getting the last x messages in chat use @BotName (num of responses wanted)"""
                response = client.chat_postMessage(
                    channel="testingbot",
                    text="Error: " + text)
                working = 0
                return "Sucsess"
        else:
            response = client.chat_postMessage(
    				channel="testingbot",
    				text="Sorry I am still working on the previous request")

    
    # Check if you are deleting a message to the message table
    elif (event != None and event.get("type") == "message" and event.get("subtype") == "message_deleted"):
        try:
            print("Message Deleted")
            ts = float(r.get("event").get("previous_message").get('ts').strip(' "'))
            user = r.get("event").get("previous_message").get('user')
            EvaDB.removeMessage(ts, user)
        except Exception as e:
            print(e)

    # Check if a message has been edited 
    elif (event != None and event.get("type") == "message" and event.get("subtype") == "message_changed"):
        try:
            print("Message Edited")
            ts = float(r.get("event").get("previous_message").get("ts").strip(' "'))
            user = r.get("event").get("previous_message").get("user")
            mes = r.get("event").get("message").get("text")
            phrase = ""
            phrase = phrase + mes
            mes = phrase.replace("'", "" )
            EvaDB.removeMessage(ts, user)
            EvaDB.addMessage(ts, user, mes)
            # EvaDB.updateMessage(ts, user, mes)
        except Exception as e:
            print(e)

    # Check if you are adding a message to the message table
    elif (event != None and event.get("type") == "message" and event.get("subtype") == None):
        print("Message Added")
        try:
            ts = float(r.get("event").get("ts").strip(' "'))
            user = r.get("event").get("user")
            mes = r.get("event").get("text")
            phrase = ""
            phrase = phrase + mes
            mes = phrase.replace("'", "" )
            if (user != EvaDB.BOT_ID):
                EvaDB.addMessage(ts, user, mes)
        except Exception as e:
            print(e)

    return "Sucsess"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)