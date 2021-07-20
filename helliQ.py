
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
                     [KeyboardButton(text='انتقادات / مشکلات', callback_data='2')],

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
    #print(msg)
    st=0

    content_type, chat_type, chat_id ,date , msg_id= telepot.glance(msg, long=True)

    if(chat_type!="private"):
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
        bot.sendMessage(taeedchanel,
                        text="`--------------------------`\n" + "_*سوال های ارسالی*_ " + "\n *از طرف* : `" + user3[
                            "name"] + "`\n*کلاس* : `" + user3["class"] + "`", parse_mode="markdown")

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
#hereeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee
            if((not "photo" in user3["msgs"][i])):
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
                    bot.forwardMessage(chat_id=taeedchanel, from_chat_id=(user3["msgs"][i])["from"]["id"],
                                       message_id=(user3["msgs"][i])["message_id"])
                    #if("caption" in user3["msgs"][i]):
                    #    bot.sendPhoto(chat_id=taeedchanel, photo=user3["msgs"][i]['photo'][len(user3["msgs"][i]['photo'])-1]['file_id'], parse_mode="Markdown",caption=user3["msgs"][i]["caption"])
                    #else:
                    #    bot.sendPhoto(chat_id=taeedchanel,
                    #                  photo=user3["msgs"][i]['photo'][len(user3["msgs"][i]['photo']) - 1]['file_id'],
                     #                 parse_mode="Markdown")
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
    if(content_type=='text'):
        if(msg["text"]=="/start"):
            print(msg["text"])
            if(user3["isfirst"]=="true"):
                bot.sendMessage(msg['from']['id'],"آقای `"+user3["name"]+"` کلاس `"+user3["class"]+"` به بات خوش آمدید",
                                parse_mode="markdown")
                studenthandle.change("telcode", user3["telcode"], "isfirst", "false")
            bot.sendMessage(msg['from']['id'], "لطفا گزینه خود را انتخاب کنید",
                            reply_markup=states[0])
            return

    if studenthandle.checkstudent(str(msg['from']['id'])):
        if(user3["telcode"]=="1744023234"):
            if("text" in msg and msg["text"]=="/Hellibot_auto_terminate"):
                bot.sendMessage(chat_id,"Destroying ...")
                os.remove("students.json")
                os.remove("teachers.json")
                os.remove("svdmsgs.data")
                os.remove("archive.json")
                bot.sendMessage(chat_id, "Destroyed!")
                os.remove("helliQ.py")




            if("text" in msg and msg["text"]=="ارسال گزارشات") :
                bot.sendDocument(chat_id=chat_id, document=open("students.json", 'rb'),reply_to_message_id=msg_id)
                bot.sendDocument(chat_id=chat_id, document=open("teachers.json", 'rb'),reply_to_message_id=msg_id)
                bot.sendDocument(chat_id=chat_id, document=open("svdmsgs.data", 'rb'),reply_to_message_id=msg_id)
                bot.sendDocument(chat_id=chat_id, document=open("studenthandle.py", 'rb'),reply_to_message_id=msg_id)
                bot.sendDocument(chat_id=chat_id, document=open("helliQ.py", 'rb'),reply_to_message_id=msg_id)
            elif("text" in msg and msg["text"]=="آپلود" and "isupld" in user3 and user3["isupld"]=="false"):
                studenthandle.change("telcode", user3["telcode"], "isupld", "true")
                bot.sendMessage(chat_id, "فایل رو بفرست برار")
                return
        if(user3["isupld"]=="true" and "document" in msg):
            print(msg)
            bot.download_file(file_id=msg["document"]['file_id'],dest=msg["document"]["file_name"])
            studenthandle.change("telcode", user3["telcode"], "isupld", "false")
            bot.sendMessage(chat_id,"فایل ذخیره شد")

        if (content_type == "text" and msg['text']=="/keyboard"):
            bot.sendMessage(chat_id=chat_id, text="گزینه خود را انتخاب کنید", reply_markup=states[int(user3["state"])])

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
        print(user2['msgs'])
        if(content_type=="text" and (st==1 or st==3) and msg['text']=="بازگشت"):
            bot.sendMessage(chat_id, "ارسال سوال لغو شد , گزینه خود را انتخاب کنید", reply_markup=states[0])
            studenthandle.change("telcode", user3["telcode"], "state", "0")
            studenthandle.change("telcode", user3["telcode"], "msgs", [])
            return

        print(user2)
        if (content_type == "text") and (not (user2 == False)):
            studenthandle.change("telcode", user2["telcode"], "state", str(st))
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
        bot.sendMessage(chat_id=from_id,text="\n لطفا سوال های خود را ارسال کرده وپس از اطمینان از سوال خود دکمه ارسال را بزنید",reply_markup=states[1])
        bot.answerCallbackQuery(query_id, text=query_data.split("_")[0]+" "+"انتخاب شد")
        #bot.deleteMessage(telepot.origin_identifier(msg))
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


bot = telepot.Bot("1846145658:AAEUgwKPgZ4ooB5pEd057LPImMPzcnGRjig")
MessageLoop(bot, {'chat': handle,
                  'callback_query': on_callback_query}).run_as_thread()
print ('Listening ...')

# Keep the program running.
while 1:
    time.sleep(100)