
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

def savedata(datas):
    with open('svdmsgs.data', 'wb') as filehandle:
        pickle.dump(datas, filehandle)
def loaddata():
    with open('svdmsgs.data', 'rb') as filehandle:
        variables = pickle.load(filehandle)
        return  variables


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
taeedchanel="-1001591586880"


def handle(msg):
    print(msg)
    st=0
    #print(msg)
    content_type, chat_type, chat_id ,date , msg_id= telepot.glance(msg, long=True)
    #print(content_type,chat_type,chat_id,date,msg_id)
    #print(msg)
    #if (st == 0):
    #    bot.deleteMessage(msg_identifier=telepot.message_identifier(msg))


    if(chat_type=="channel"):
        #keyboards2 = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="yes",callback_data="sss")],[InlineKeyboardButton(text="no",callback_data="sss")]
        #])
        #bot.sendMessage("-1001591586880", "asddsa",reply_markup=keyboards2)
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
        gpp=[]
        keyboards2 = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="yes",
                                                                                 callback_data=user3["name"] + "_" +
                                                                                               user3["telcode"] + "_" +
                                                                                               user3[
                                                                                                   "toid"] + "_" + "y")],
                                                           [InlineKeyboardButton(text="no",
                                                                                 callback_data=user3["name"] + "_" +
                                                                                               user3["telcode"] + "_" +
                                                                                               user3[
                                                                                                   "toid"] + "_" + "n")]
                                                           ])
        bot.sendMessage(taeedchanel, text="سوال های ارسالی " + "\n از طرف : " + user3["name"])
        f = open("teachers.json", "r", encoding='utf-8')
        tdata = json.loads(f.read())
        f.close()
        sk=""
        for w in range(len(tdata)):
            for j in range(len(tdata[w]["class"])):
                if(tdata[w]["class"][j][1]==user3["toid"]):
                    sk=tdata[w]["dars"]
        bot.sendMessage(taeedchanel, text="`ادمین ارسال`" + "\n" + "آیا پیام بالا ارسال شود؟"+"\n`------------------------------------`"+"\n"+"`فرستنده : `"+"`"+user3["name"]+"`\n`کلاس : "+user3["class"]+"`\n`درس : "+sk+"`", reply_markup=keyboards2,
                        parse_mode="Markdown")


        for i in range(len(user3["msgs"])):
            if("media_group_id" in user3["msgs"][i]):
                if(user3["msgs"][i]["media_group_id"] in gpp):
                    continue;
                else:
                    gpp.append(user3["msgs"][i]["media_group_id"])
            #print(gpp)
            #bot.sendMessage(chat_id=user3["toid"],text=(user3["msgs"][i])['text']+"\n از طرف : "+user3["name"])

            if("text" in user3["msgs"][i] and (not "photo" in user3["msgs"][i])):
                #bot.sendMessage(taeedchanel, text=(user3["msgs"][i])['text'], reply_markup=keyboards2)
                f=bot.forwardMessage(chat_id=taeedchanel, from_chat_id=(user3["msgs"][i])["from"]["id"],
                                   message_id=(user3["msgs"][i])["message_id"])
                bot.sendMessage(taeedchanel,
                                text="`ادمین ارسال`" + "\n" + "آیا پیام بالا ارسال شود؟" + "\n`------------------------------------`" + "\n" + "`فرستنده : `" + "`" +
                                     user3["name"] + "`\n`کلاس : " + user3["class"] + "`\n`درس : " + sk + "`",
                                reply_markup=keyboards2,
                                parse_mode="Markdown")

                #bot.editMessageReplyMarkup(telepot.message_identifier(f),reply_markup=keyboards2)
            #--------------------------------------------------------------
            elif("photo" in user3["msgs"][i]):
                md=[]
                lkk=[]
                for j in range(len(user3["msgs"])):
                    if ("media_group_id" in user3["msgs"][j] and "media_group_id" in user3["msgs"][i]):
                        if(user3["msgs"][j]["media_group_id"]==user3["msgs"][i]["media_group_id"]):
                            if("caption" in user3["msgs"][j]):
                                md.append({"type": "photo", "media": user3["msgs"][j]["photo"][len(user3["msgs"][j]["photo"])-1]["file_id"],
                                        "caption": user3["msgs"][j]["caption"]})
                            else:
                                md.append({"type": "photo",
                                           "media": user3["msgs"][j]["photo"][len(user3["msgs"][j]["photo"]) - 1][
                                               "file_id"]})
                #print(len(md))
                if(len(md)!=0):
                    bot.sendMediaGroup(chat_id=taeedchanel,media=md)
                    ll=loaddata()

                    keyboards3 = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="yes",
                                                                                             callback_data="!_" + user3[
                                                                                                 "telcode"] + "_" +
                                                                                                           user3[
                                                                                                               "toid"] + "_" + "y" + "_" + "_"+str(len(md)))],
                                                                       [InlineKeyboardButton(text="no",
                                                                                             callback_data="!_" + user3[
                                                                                                 "telcode"] + "_" +
                                                                                                           user3[
                                                                                                               "toid"] + "_" + "n" + "_" + "_"+str(len(md)))]
                                                                       ])

                    a=bot.sendMessage(taeedchanel, "عکس ها ارسالی " + "\n از طرف : " + user3["name"],
                                    reply_markup=keyboards3)
                    ll.append([md, a["message_id"]])
                    # print(a)
                    savedata(ll)
                    #print(ll)
                else :
                    if("caption" in user3["msgs"][i]):
                        bot.sendPhoto(chat_id=taeedchanel, photo=user3["msgs"][i]['photo'][len(user3["msgs"][i]['photo'])-1]['file_id'], parse_mode="Markdown",caption=user3["msgs"][i]["caption"])
                    else:
                        bot.sendPhoto(chat_id=taeedchanel,
                                      photo=user3["msgs"][i]['photo'][len(user3["msgs"][i]['photo']) - 1]['file_id'],
                                      parse_mode="Markdown")
                    bot.sendMessage(taeedchanel,
                                    text="`ادمین ارسال`" + "\n" + "آیا پیام بالا ارسال شود؟" + "\n`------------------------------------`" + "\n" + "`فرستنده : `" + "`" +
                                         user3["name"] + "`\n`کلاس : " + user3["class"] + "`\n`درس : " + sk + "`",
                                    reply_markup=keyboards2,
                                    parse_mode="Markdown")

                #print(len(lkk))



#----------------------------------------------------------------
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
            if(len(user3["msgs"])==0):
                bot.sendMessage(chat_id, "شما هنوز سوالی وارد نکرده اید", reply_markup=states[1])
                return
            bot.sendMessage(chat_id,"آیا از فرستادن این سوال ها اطمینان دارید ؟",reply_markup=states[2])
            st=3
            studenthandle.change("telcode", user3["telcode"], "state", "3")
            return
        user2 = studenthandle.searchs("telcode", str(msg['from']['id']))
        st=int(user2["state"])
        if (st == 1 and (not "edit_date" in msg)):
            user2["msgs"].append(msg)
            studenthandle.change("name", user2["name"], "msgs", user2["msgs"])
        #print(user2['msgs'])
        if(content_type=="text" and (st==1 or st==3) and msg['text']=="بازگشت"):
            bot.sendMessage(chat_id, "ارسال سوال لغو شد , گزینه خود را انتخاب کنید", reply_markup=states[0])
            studenthandle.change("telcode", user3["telcode"], "state", "0")
            studenthandle.change("telcode", user3["telcode"], "msgs", [])
            return

        #print(user2)
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
                        f = open("teachers.json", "r", encoding='utf-8')
                        tdata = json.loads(f.read())
                        f.close()
                        for i in range(len(tdata)):
                            for j in range(len(tdata[i]["class"])):
                                if(tdata[i]["class"][j][0]==user2["class"]):
                                    if not str(tdata[i]["class"][j][1])=="":
                                        keyboard2.inline_keyboard.append([InlineKeyboardButton(text=str(tdata[i]["dars"]+" _ "+"آقای "+tdata[i]["name"]), callback_data=tdata[i]["dars"]+"_"+str(tdata[i]["class"][j][1]))])

                        bot.sendMessage(msg['from']['id'], matn, parse_mode="Markdown", reply_markup=keyboard2)
    else:
        bot.sendMessage(msg['from']['id'], "شما مجاز به استفاده از بات نیستید", parse_mode="Markdown")







def on_callback_query(msg):
    st = 1
    global dlmsgs
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    kl=query_data.split("_")
    #print(telepot.origin_identifier(msg))
    if(len(kl)==2):
        user2 = studenthandle.searchs("telcode", str(from_id))
        studenthandle.change("telcode", user2["telcode"], "msgs", [])
        studenthandle.change("telcode", user2["telcode"], "toid", query_data.split("_")[1])
        studenthandle.change("telcode", user2["telcode"], "state", "1")
        print('Callback Query:', query_id, from_id, query_data)
        bot.editMessageText(msg_identifier=telepot.origin_identifier(msg),text="درس "+query_data.split("_")[0]+" انتخاب شد",parse_mode="Markdown")
        bot.sendMessage(chat_id=from_id,text="\n لطفا سوال خود را ارسال کرده وپس از اطمینان از سوال خود دکمه ارسال را بزنید",reply_markup=states[1])
        bot.answerCallbackQuery(query_id, text=query_data.split("_")[0]+" "+"انتخاب شد")
        bot.deleteMessage(telepot.origin_identifier(msg))
    elif (len(kl)==4):
        name,telcode,toid,yon=kl
        if(yon=="y"):
            # bot.forwardMessage(chat_id=user3["toid"], from_chat_id=(user3["msgs"][i])["from"]["id"],
            # message_id=(user3["msgs"][i])["message_id"])
            bot.forwardMessage(chat_id =toid,message_id=telepot.origin_identifier(msg)[1]-1,from_chat_id=telepot.origin_identifier(msg)[0])
        bot.deleteMessage(telepot.origin_identifier(msg))
        bot.deleteMessage((telepot.origin_identifier(msg)[0], telepot.origin_identifier(msg)[1] - 1))

    elif(len(kl)==6):
        name, telcode, toid, yon,chatid,numbs = kl
        numbs=int(numbs)
        if (yon == "y"):
            #bot.forwardMessage(chat_id=user3["toid"], from_chat_id=(user3["msgs"][i])["from"]["id"],
                #message_id=(user3["msgs"][i])["message_id"])


            if(numbs!=0):
                ll=loaddata()
                b=[]
                for i in range(len(ll)):
                    if(ll[i][1]==telepot.origin_identifier(msg)[1]):
                        bot.sendMediaGroup(chat_id=toid,media=ll[i][0])
                        continue
                    b.append(ll[i])
                savedata(b)
        bot.deleteMessage(telepot.origin_identifier(msg))
        if(numbs!=0):
            for i in range(1, numbs + 1):
                bot.deleteMessage((telepot.origin_identifier(msg)[0], telepot.origin_identifier(msg)[1] - i))
    dlmsgs=[]

botfatherapi = "API_KEY"
bot = telepot.Bot(botfatherapi)
MessageLoop(bot, {'chat': handle,
                  'callback_query': on_callback_query}).run_as_thread()
print ('Listening ...')

# Keep the program running.
while 1:
    time.sleep(100)
