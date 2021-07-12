
import time
import telepot
from telepot.loop import MessageLoop
import os.path
import codecs
import studenthandle
from studenthandle import *


def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(msg)
    if checkstudent(str(msg['from']['id'])):
        print(1)
        if (content_type=="text" and msg['text']=="/start"):
            user = searchs("telcode",str(msg['from']['id']))
            if(not (user==False)):
                bot.sendMessage(msg['from']['id'],"آقای " + user['name']+ " به بات خوش آمدید", parse_mode="Markdown")
    else:
        bot.sendMessage(msg['from']['id'], "شما مجاز به استفاده از بات نیستید", parse_mode="Markdown")
    if content_type == 'text':
        print("11")
        #bot.sendMessage(msg['from']['id'], msg['text'], parse_mode="Markdown")
    elif content_type == 'audio':
        txt = msg['caption']
        print(txt)
        print("ok")
        bot.sendAudio(msg['from']['id'], msg['audio']['file_id'],"asd", performer="matin", parse_mode="Markdown")
        print("yes")
    
#telepot.api.set_proxy("",  basic_auth=())

bot = telepot.Bot("1749966129:AAE8qFyu9T-cchkzM1rv4EzhNHBJFKH1mVA")
MessageLoop(bot, handle).run_as_thread()
print ('Listening ...')

# Keep the program running.
while 1:
    time.sleep(10)
