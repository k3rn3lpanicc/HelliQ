
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
    a=False
    #print(msg)
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="طرح سوال")], [KeyboardButton(text="انتقادات")]],
        resize_keyboard=True)


    if checkstudent(str(msg['from']['id'])):
        if (content_type=="text"):
            user2 = searchs("telcode",str(msg['from']['id']))
            print(user2)
            if(not (user2==False)):
                if(user2['isfirst']=='false'):
                    bot.sendMessage(msg['from']['id'],"آقای " + user2['name']+ " دانش آموز کلاس " +user2['class']+ " به بات خوش آمدید", parse_mode="Markdown",reply_markup=keyboard)

                    change("telcode", str(msg['from']['id']), "isfirst", "true")
                else:
                    if (content_type == "text" and msg['text'] == 'طرح سوال'):
                        print(1)
                        user = searchs("telcode", str(msg['from']['id']))
                        #print(user)
                        matn="لطفا درس خود را انتخاب کنید"
                        paye = user['class'].split('/')[0]
                        reshte=user['class'].split('/')[1]
                        if (str(paye) == "11"):
                            keyboard2 = InlineKeyboardMarkup(inline_keyboard=[
                                [InlineKeyboardButton(text='ریاضی صفر', callback_data='2')],
                                [InlineKeyboardButton(text='ریاضی صفر', callback_data='3')],
                                [InlineKeyboardButton(text='ریاضی صفر', callback_data='4')],
                                [InlineKeyboardButton(text='ریاضی صفر', callback_data='5')],
                                [InlineKeyboardButton(text='ریاضی صفر', callback_data='6')],
                                [InlineKeyboardButton(text='ریاضی صفر', callback_data='7')],
                                [InlineKeyboardButton(text='ریاضی صفر', callback_data='8')],
                            ])
                            bot.sendMessage(msg['from']['id'], matn, parse_mode="Markdown", reply_markup=keyboard2)
                        if (str(paye)=="12"):
                            if(int(reshte)<=6):
                                keyboard2 = InlineKeyboardMarkup(inline_keyboard=[
                                    [InlineKeyboardButton(text='فارسی', callback_data='فارسی')],
                                    [InlineKeyboardButton(text='عربی', callback_data='عربی')],
                                    [InlineKeyboardButton(text='دینی', callback_data='4')],
                                    [InlineKeyboardButton(text='زبان', callback_data='5')],
                                    [InlineKeyboardButton(text='حسابان', callback_data='6')],
                                    [InlineKeyboardButton(text='هندسه', callback_data='7')],
                                    [InlineKeyboardButton(text='گسسته', callback_data='8')],
                                    [InlineKeyboardButton(text='فیزیک', callback_data='8')],
                                    [InlineKeyboardButton(text='شیمی', callback_data='8')],

                                ])
                                bot.sendMessage(msg['from']['id'], matn, parse_mode="Markdown", reply_markup=keyboard2)
                            else:
                                keyboard2 = InlineKeyboardMarkup(inline_keyboard=[
                                    [InlineKeyboardButton(text='فارسی', callback_data='2')],
                                    [InlineKeyboardButton(text='عربی', callback_data='3')],
                                    [InlineKeyboardButton(text='دینی', callback_data='4')],
                                    [InlineKeyboardButton(text='زبان', callback_data='5')],
                                    [InlineKeyboardButton(text='زمین شناسی', callback_data='6')],
                                    [InlineKeyboardButton(text='ریاضی', callback_data='8')],
                                    [InlineKeyboardButton(text='زیست', callback_data='8')],
                                    [InlineKeyboardButton(text='فیزیک', callback_data='8')],
                                    [InlineKeyboardButton(text='شیمی', callback_data='8')],

                                ])
                                bot.sendMessage(msg['from']['id'], matn, parse_mode="Markdown", reply_markup=keyboard2)


    else:
        bot.sendMessage(msg['from']['id'], "شما مجاز به استفاده از بات نیستید", parse_mode="Markdown")







def on_callback_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    print('Callback Query:', query_id, from_id, query_data)
    bot.answerCallbackQuery(query_id, text='Button has been pressed')

bot = telepot.Bot("1860330944:AAGXJUANMwuBDfMsFXxg2siViWt_ardlrEo")
MessageLoop(bot, {'chat': handle,
                  'callback_query': on_callback_query}).run_as_thread()
print ('Listening ...')

# Keep the program running.
while 1:
    time.sleep(10)
