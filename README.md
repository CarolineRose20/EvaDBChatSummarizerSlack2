# EvaDB Slack Bot 2 Using EvaDBs Slack as a Data Source
A Slack App that summarizes a single message or a group of messages on a single channel using EvaDB and GPT4ALL

# Installation Guide
## Step 1) Create a Slack App
You will need a Slack token for your bot to connect the code to the bot and a channel to connect the bot to. As of right now the bot only works on a singular channel.
## Step 2) Install and set up NGROK
You will need to use NGROK to connect the Flask server to Slack once it is installed open the application and use the command: ngrok http 8080
This will create a link that you will then put in the Event Subscriptions URL link inside your Slack application.
## Step 3) Final Steps
Install the required packages to be able to run everything. After this is done there are two lines of code you will need to edit so the app works for your server.
You must edit the CHANNEL_ID and BOT_ID variables in the EvaDB.py they are towards the top. CHANNEL_ID is the channel ID for the channel the bot will live in.
BOT_ID is the ID for the bot. This lets the application bypass the bot when saving messages so they do not crowd the Message Table
## STEP 4) Start the Flask Server
Run flask_server.py to start the flask server and now it should be able to see your Slack Channel.

# How to Use
## General Messages
If you just want the bot to summarize the last x messages in the chat you have to write the command as @bot_name channel_name x
EX. I want to grab the last 5 messages from the chat (this excludes any bot messages): @Bot general 5

## Messages from a Specific User
If you just want the bot to summarize the last x messages sent by a specific user in the chat you have to write the command as @bot_name channel_name @user x
EX. I want to grab the last message from a user @cm: @Bot general @cm 1
