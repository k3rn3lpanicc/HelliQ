
import time
import telepot
from telepot.loop import MessageLoop
import os.path
import codecs
import studenthandle
from studenthandle import *
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from telepot.namedtuple import KeyboardButton , ReplyKeyboardMarkup

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(msg)
    if checkstudent(str(msg['from']['id'])):
        print(1)
        if (content_type=="text"):
            user = searchs("telcode",str(msg['from']['id']))
            if(not (user==False)):
                if(user['isfirst']=='false'):
                    bot.sendMessage(msg['from']['id'],"آقای " + user['name']+ " به بات خوش آمدید", parse_mode="Markdown")
                    change("telcode", str(msg['from']['id']), "isfirst", "true")
            else:
                print('salam')
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
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="طرح سوال")],
            [KeyboardButton(text="انتقادات")]
        ],resize_keyboard=True
    )
    bot.sendMessage(msg['from']['id'], "گزینه خود را انتخاب کنید", parse_mode="Markdown",reply_markup = keyboard)


#telepot.api.set_proxy("",  basic_auth=())
def on_callback_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    print('Callback Query:', query_id, from_id, query_data)
    bot.answerCallbackQuery(query_id, text='Button has been pressed')

bot = telepot.Bot("1749966129:AAE8qFyu9T-cchkzM1rv4EzhNHBJFKH1mVA")
MessageLoop(bot, {'chat': handle,
                  'callback_query': on_callback_query}).run_as_thread()
print ('Listening ...')

# Keep the program running.
while 1:
    time.sleep(10)
