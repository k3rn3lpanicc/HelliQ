
import time
import telepot
from telepot.loop import MessageLoop
import os.path
import codecs
import studenthandle
from studenthandle import *
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from telepot.namedtuple import KeyboardButton , ReplyKeyboardMarkup
import pickle





states=[ReplyKeyboardMarkup(keyboard=[
                     [KeyboardButton(text='طرح سوال', callback_data='1')],
                     [KeyboardButton(text='انتقادات', callback_data='2')],

                 ], resize_keyboard=True)
    ,
        ReplyKeyboardMarkup(keyboard=[
            [KeyboardButton(text='ارسال', callback_data='1')],
            [KeyboardButton(text='بازگشت', callback_data='1')],
        ], resize_keyboard=True)
,
ReplyKeyboardMarkup(keyboard=[
            [KeyboardButton(text='بله', callback_data='1')],
            [KeyboardButton(text='خیر', callback_data='1')],
        ], resize_keyboard=True)
    ]

def handle(msg):
    st=0

    content_type, chat_type, chat_id ,date , msg_id= telepot.glance(msg, long=True)
    #print(content_type,chat_type,chat_id,date,msg_id)
    print(msg)
    #if (st == 0):
    #    bot.deleteMessage(msg_identifier=telepot.message_identifier(msg))
    f = open("teachers.json", "r", encoding='utf-8')
    tdata = json.loads(f.read())
    f.close()
    print(chat_type)
    if(chat_type=="channel"):
        keyboards2 = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="yes",callback_data="sss")],[InlineKeyboardButton(text="no",callback_data="sss")]
        ])
        bot.sendMessage("-1001538222324", "asddsa",reply_markup=keyboards2)
        return

    user3 = studenthandle.searchs("telcode", str(msg['from']['id']))
    if (not (user3 == False)):
        st = int(user3["state"])

    if(st==3 and msg['text']=="بله"):
        bot.deleteMessage(telepot.message_identifier(msg))
        st = 0
        # Sending to channel
        studenthandle.change("telcode", user3["telcode"], "state", "0")
        bot.sendMessage(chat_id=chat_id,
                        text="سوال شما ارسال شد" + "\n" + "میتوانید موضوع بعدی را انتخاب کنید",
                        reply_markup=states[0])
        for i in range(len(user3["msgs"])):
            bot.forwardMessage(chat_id=user3["toid"], from_chat_id=(user3["msgs"][i])[0],
                               message_id=(user3["msgs"][i])[1])
            # bot.sendMessage(chat_id=user3["toid"],text=telepot.message_identifier(user3["msgs"][i])["text"])

        studenthandle.change("telcode", user3["telcode"], "msgs", [])
        studenthandle.change("telcode", user3["telcode"], "toid", "")
        return
    if(st==3 and msg['text']=="خیر"):
        bot.deleteMessage(telepot.message_identifier(msg))
        bot.sendMessage(chat_id,"میتوانید سوال های فرستاده شده خود را ویرایش کنید و پس از اتمام ارسال کنید",reply_markup=states[1])
        studenthandle.change("telcode", user3["telcode"], "state", "1")
        return
    if(content_type=='text' and msg['text']=="/start"):
        bot.sendMessage(msg['from']['id'],"به بات خوش آمدید",reply_markup=states[0])
        return

    if studenthandle.checkstudent(str(msg['from']['id'])):
        if ((st == 1 or st==3) and content_type == "text" and msg['text'] == "ارسال"):
            bot.deleteMessage(telepot.message_identifier(msg))
            bot.sendMessage(chat_id,"آیا از فرستادن این سوال ها اطمینان دارید ؟",reply_markup=states[2])
            st=3
            studenthandle.change("telcode", user3["telcode"], "state", "3")
            return
        user2 = studenthandle.searchs("telcode", str(msg['from']['id']))
        if (int(user2["state"]) == 1 and (not "edit_date" in msg)):
            user2["msgs"].append(telepot.message_identifier(msg))
        studenthandle.change("name", user2["name"], "msgs", user2["msgs"])
        if((st==1 or st==3) and msg['text']=="بازگشت"):
            bot.sendMessage(chat_id, "ارسال سوال لغو شد , گزینه خود را انتخاب کنید", reply_markup=states[0])
            studenthandle.change("telcode", user3["telcode"], "state", "0")
            studenthandle.change("telcode", user3["telcode"], "msgs", [])
            return

        print(user2)
        if (content_type=="text"):
            if(not (user2==False)):
                studenthandle.change("telcode", user2["telcode"], "state", str(st))
                if(user2['isfirst']=='true'):
                    bot.sendMessage(msg['from']['id'],"آقای " + user2['name']+ " دانش آموز کلاس " +user2['class']+ " به بات خوش آمدید", parse_mode="Markdown",reply_markup=states[st])
                    studenthandle.change("telcode", str(msg['from']['id']), "isfirst", "false")
                else:
                    if (content_type == "text" and msg['text'] == 'طرح سوال'):
                        #print(1)
                        user = studenthandle.searchs("telcode", str(msg['from']['id']))
                        #print(user)
                        matn="لطفا درس خود را انتخاب کنید"
                        paye = user['class'].split('/')[0]

                        reshte=user['class'].split('/')[1]
                        keyboard2 = InlineKeyboardMarkup(inline_keyboard=[
                        ])
                        for i in range(len(tdata)):
                            for j in range(len(tdata[i]["class"])):
                                if(tdata[i]["class"][j][0]==user2["class"]):
                                    if not str(tdata[i]["class"][j][1])=="":
                                        keyboard2.inline_keyboard.append([InlineKeyboardButton(text=str(tdata[i]["dars"]+" _ "+"آقای "+tdata[i]["name"]), callback_data=tdata[i]["dars"]+"_"+str(tdata[i]["class"][j][1]))])

                        bot.sendMessage(msg['from']['id'], matn, parse_mode="Markdown", reply_markup=keyboard2)
    else:
        bot.sendMessage(msg['from']['id'], "شما مجاز به استفاده از بات نیستید", parse_mode="Markdown")







def on_callback_query(msg):
    global st
    st = 1
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    a,b=telepot.origin_identifier(msg)
    user2 = studenthandle.searchs("telcode", str(from_id))
    studenthandle.change("telcode", user2["telcode"], "msgs", [])
    studenthandle.change("telcode", user2["telcode"], "toid", query_data.split("_")[1])
    studenthandle.change("telcode", user2["telcode"], "state", "1")
    print('Callback Query:', query_id, from_id, query_data)
    bot.editMessageText(msg_identifier=telepot.origin_identifier(msg),text="درس "+query_data.split("_")[0]+" انتخاب شد",parse_mode="Markdown")
    bot.sendMessage(chat_id=from_id,text="\n لطفا سوال خود را ارسال کرده وپس از اطمینان از سوال خود دکمه ارسال را بزنید",reply_markup=states[1])
    bot.answerCallbackQuery(query_id, text='Button has been pressed')

bot = telepot.Bot("1846145658:AAEdDoGYlURjcMT9yZywmZIgaXJzt12R8QU")
MessageLoop(bot, {'chat': handle,
                  'callback_query': on_callback_query}).run_as_thread()
print ('Listening ...')

# Keep the program running.
while 1:

    time.sleep(10)
