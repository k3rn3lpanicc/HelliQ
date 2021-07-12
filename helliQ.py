
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
    if(not os.path.isfile('music\\'+str(chat_id)+'.txt')):
        asd=open('music\\'+str(chat_id)+'.txt',"w")
        if(content_type=='text'):
            if(msg['text']=='mydamnpass'):
                asd.write("admin:")
    text=''
    with codecs.open('music\\'+str(chat_id)+'.txt', 'r', encoding='utf8') as f:
        text = f.read()
    
    tt=text
    fir=''
    sec=''
    if(tt!=''):
        fir=tt.split(':')[0]
        sec=tt.split(':')[1]
    if sec=='':
        print("First set the text with /set [text] command")

    sec=''
    if content_type == 'text' and fir=='admin':
        bot.sendMessage(msg['from']['id'],msg['text'],parse_mode="Markdown")
    elif content_type == 'audio':
        #caption :
        txt=msg['caption']
        print(txt)
        # if not txt..endswith('')
        print("ok")
        bot.sendAudio(msg['from']['id'], msg['audio']['file_id'],"asd", performer="matin", parse_mode="Markdown")
        print("yes")
    
telepot.api.set_proxy("", basic_auth=())

bot = telepot.Bot("1749966129:AAE8qFyu9T-cchkzM1rv4EzhNHBJFKH1mVA")
MessageLoop(bot, handle).run_as_thread()
print ('Listening ...')

# Keep the program running.
while 1:
    time.sleep(10)
