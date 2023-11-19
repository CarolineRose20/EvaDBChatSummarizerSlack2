from gpt4all import GPT4All
import os


llm = GPT4All(os.environ.get('GPT4ALL_PATH'))


# Summarize a Single Message
def singleMessage(message):
    SingleMessageChat = f"""
Given:
{message}

Give a 1-3 sentense summary of the message. Use only the information above and do not come up with anything new
"""
    res = llm.generate(SingleMessageChat)
    return res

# Summarize Multiple Messages
def multipleMessages(messages):
    MultipleMessagesChat = f"""
Seeing the following conversation or message:
{messages}
Give a 2-3 sentense summary of what was talked about.
"""
    t = llm.generate(MultipleMessagesChat)
    return t

# Parse the given message for how many messages are generated and by who
def parseMessage(message):
    print("Test")
    MessageParssing = f"""
Do not make up any information only use the example formats.

Example Formats:
User: Can you give me a summary of the last 4 messages in chat please?
AI: general,3

User: Can you summerize the last post by @cmosier6
AI: cmosier6,1

User: Can you summerize the last 3 messages from @test12
AI: test12,3

User: Can you give me a summary of the last 5 messages in chat please?
AI: general,5

User: {message}
"""
    res = llm.generate(MessageParssing)
    list = res.split(' ')
    return list[1]

# singleMessage("Say HI")

