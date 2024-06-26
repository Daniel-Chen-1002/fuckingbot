from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

import random
import time
import math

from firebase import firebase
url = 'https://fuck-ae07c-default-rtdb.firebaseio.com/'
fb = firebase.FirebaseApplication(url, None)

app = Flask(__name__)
line_bot_api = LineBotApi('nfX/V4p/OO1N9b85uLXlAwJjFCTFrZVns0ujsKwO9XAqDyDos0Ws/Z3zKIV3aG7SzPWOFXdVll9WEiROWsd/voQCYrhwpR65dHfu5Jb3OTLThMTiVxwopIKKRDD0kHy5Q+CXyTdzI8uxnDvlZfKSaAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('7c883d50fe75288c115e9a7e111b6012')
comp = {}
boost = {}
w = []
season = {}
team = {}
totalTeams=[]
seasontime=0
bank = {}
banktimer={}
mode = "echo"
toggle = {"Season":[], "Competition":[], "Debug":[]} #{mode:groupID} mode: Season, Competition, Debug
day = 0
get_day = False


@app.route('/callback', methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    app.logger.info('Request body: ' + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    except Exception as e:
        app.logger.exception('Error occurred: ' + str(e))
        abort(500)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    global comp
    global w
    global mode
    global toggle
    global season
    global team
    global boost
    global totalTeams
    global bank
    global banktimer
    global seasontime
    global day
    global get_day
    group = event.source.group_id
    user = event.source.user_id
    seasontime=fb.get(url+"seasontime/", None)
    def normal(user):
        try:
            team[user]
            return True
        except KeyError:
            return False
    try:
        name = line_bot_api.get_profile(event.source.user_id).display_name
    except LineBotApiError:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="Since like you didn't add the bot as friend, so https://lin.ee/5M1merW is the link to adding friend, please add it quickly."))
        name = user
    print(user)
    if event.message.text.split(" ")[0] == "!toggle":
        if user == "U4e5ae01224117b28f662c288775be0a7":
            for i in list(toggle.keys()):
                if str(group) in toggle[i]:
                    toggle[i].remove(str(group))
                    break
            toggle[event.message.text.split(" ")[1]].append(str(group))
            reply = [TextSendMessage(text="Successfully toggle to "+event.message.text.split(" ")[1]), TextSendMessage(text="group ID: "+str(group))]
            line_bot_api.reply_message(event.reply_token, reply)
        else:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="fuck you cheater"))
    if group in toggle["Competition"]:
        if event.message.text.split(" ")[0] == "!start":
            if event.message.text.split(" ")[1] == "comp":
                if user == "U4e5ae01224117b28f662c288775be0a7":
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text="keyword is:"+ event.message.text.split(" ")[2]+", please type as much keyword as possible"))
                    w.append(event.message.text.split(" ")[2])
        if event.message.text=="clear score":
            comp = {}
        if len(w)>0:
            if event.message.text == "fuck" or event.message.text == "Fuck":
                if random.randint(1, 100) == 50:
                    boost[name]==time.time()
                else:
                    try:
                        if time.time()-boost[name]<=3:
                            pass
                        else:
                            boost[name] = 0
                    except KeyError:
                        boost[name] = 0
                if time.time()-boost[name]<=3:
                    try:
                        comp[name] = comp[name] + 2
                    except KeyError:
                        comp[name] = 2
                else:
                    try:
                        comp[name] = comp[name] + 1
                    except KeyError:
                        comp[name] = 1
            if event.message.text == "condom" or event.message.text == "Condom":
                try:
                    if random.randint(1, len(comp)) == 1:
                        try:
                            comp[name] = comp[name] + (len(comp)-1)
                        except KeyError:
                            comp[name] = (len(comp))
                        other = list(comp.keys())
                        other.remove(name)
                        for ppl in other:
                            try:
                                comp[ppl] = comp[ppl] - 1
                            except KeyError:
                                comp[ppl] = -1
                        print("success")
                    else:
                        try:
                            comp[name] = comp[name] - 1
                        except KeyError:
                            comp[name] = (len(comp))
                        other = list(comp.keys())
                        other.remove(name)
                        for ppl in other:
                            try:
                                comp[ppl] = comp[ppl] + 1
                            except KeyError:
                                comp[ppl] = +1
                        print("fail")
                except ValueError:
                    try:
                        comp[name] = comp[name] - 15
                    except KeyError:
                        comp[name] = -15
                    print("fuck you cheater")
            if event.message.text == "Daniel" or event.message.text == "@陳雋翔 Daniel Chen" or event.message.text == "daniel" or event.message.text == "Fuck daniel" or event.message.text == "VBB":
                try:
                    comp[name] = comp[name] - 1
                except KeyError:
                    comp[name] = -1
        if event.message.text == "stop":
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=str(comp)))
            w.pop()
    if group in toggle["Season"]:
        if event.message.text.split(" ")[0] == "!join":
            if user == "U4e5ae01224117b28f662c288775be0a7":
                for i in event.message.mention.mentionees:
                    x = []
                    x.append(event.message.text.split(" ")[-1])
                    print(event.message.text.split(" "))
                    x.append(0)
                    x.append(0)
                    x.append(0)
                    x.append(0)
                    team[i.user_id] = x
                    if x[0] not in totalTeams:
                        totalTeams.append(x[0])
                season[event.message.text.split(" ")[-1]] = [100000, 0, 1]
                bank[event.message.text.split(" ")[-1]] = 0
                banktimer[event.message.text.split(" ")[-1]] = 0
                fb.put(url, data=season, name="season")
                fb.put(url, data=bank, name="bank")
                fb.put(url, data=banktimer, name="banktimer")
                fb.put(url, data=team, name="team")
                fb.put(url, data=totalTeams, name="totalTeams")
        if event.message.text == "stat" or event.message.text == "stats" or event.message.text == "Stat" or event.message.text == "Stats":
            season = fb.get(url+"season/", None)
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=str(season)))
        if event.message.text == "Bank" or event.message.text == "bank":
            bank = fb.get(url+"bank/", None)
            banktimer=fb.get(url+"banktimer/", None)
            for i in list(bank.keys()):
                hours = int((time.time()-banktimer[i])//3600)
                for j in range(hours):
                    bank[i] *= 1.005
                banktimer[i]+=(3600*hours)
            fb.put(url, data=bank, name="bank")
            fb.put(url, data=banktimer, name="banktimer")
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=str(bank)))
        if event.message.text == "end season" or event.message.text == "End season":
            if user == "U4e5ae01224117b28f662c288775be0a7":
                season = fb.get(url+"season/", None)
                bank = fb.get(url+"bank/", None)
                bkey = list(season.keys())
                out = {}
                for i in range(len(bkey)):
                    out[bkey[i]]=int(season[bkey[i]][0]+bank[bkey[i]])
        if event.message.text.split("n")[0] == "!start seaso":
            if user == "U4e5ae01224117b28f662c288775be0a7":
                get_day = True
                fb.put(url, data=day, name="day")
                day = int(event.message.text.split(" ")[-1])
                reply = []
                seasontime=time.time()
                fb.put(url, data=seasontime, name="seasontime")
                reply.append(TextSendMessage(text="Teams are devide as below:"))
                key = list(team.keys())
                for i in range(len(totalTeams)):
                    member = []
                    
                    for j in range(len(team)):
                        if team[key[j]][0] == totalTeams[i]:
                            try:
                                member.append(line_bot_api.get_profile(key[j]).display_name)
                            except LineBotApiError:
                                member.append(key[j])
                    reply.append(TextSendMessage(text=totalTeams[i]+" : "+str(member)))
                reply.append(TextSendMessage(text="Duration: "+str(day)+" days"))
                line_bot_api.reply_message(event.reply_token, reply)
            else:
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text="Fuck you bitch you fucking dare impersonate the head mod u idiot cerebral palsy down syndrome whore"))
        if event.message.text == "help" or event.message.text == "Help":
                reply=[TextSendMessage(text="Commands list:"), TextSendMessage(text="Main:\nfuck, bitch, viagra, report\nothers:\nstat, bank, deposit, help\nUse help [command] to get more info")]
                line_bot_api.reply_message(event.reply_token, reply)
        if event.message.text.split(" ")[0] == "help" or event.message.text.split(" ")[0] == "Help":
            topic = event.message.text.split(" ")[1]
            topicList={"fuck":"Fuck other team\nSteals points (0~20000)from other team ",
                       "bitch":"Hire a bitch to work for you\nprovides chance to block fucks from opponents\nSyntax: bitch",
                       "viagra":"Boost your dick that is used to fuck\nincrease fuck point multiplier\nSyntax: viagra",
                       "report":"Reports other player\n??"+"%"+" chance to success\nSuccess: banning opponent for 1 hour\nFail: banning yourself for 15 minutes\nSyntax: report [opponent]",
                       "stat":"Check the current point status of every team\nSyntax: stat",
                       "bank":"A place to store points, can only deposit\nPoints multiplies by 1.005 every hour\nSyntax: bank",
                       "deposit":"Deposits points into the bank\nSyntax: deposit [amount]"
                       }
            try:
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text=topicList[topic]))
            except KeyError:
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text="Are you typing with your dick? Type the correct command you need help with"))
        if event.message.text == "!continue season":
            if user == "U4e5ae01224117b28f662c288775be0a7":
                reply = []
                seasontime=fb.get(url+"seasontime/", None)
                reply.append(TextSendMessage(text="Season continued\nTeams are devide as below:"))
                season = fb.get(url+"season", None)
                team = fb.get(url+"team/", None)
                totalTeams = fb.get(url+"totalTeams/", None)
                key = list(team.keys())
                for i in range(len(totalTeams)):
                    member = []
                    
                    for j in range(len(team)):
                        if team[key[j]][0] == totalTeams[i]:
                            try:
                                member.append(line_bot_api.get_profile(key[j]).display_name)
                            except LineBotApiError:
                                member.append(key[j])
                    reply.append(TextSendMessage(text=totalTeams[i]+" : "+str(member)))
                line_bot_api.reply_message(event.reply_token, reply)
        if (time.time()-seasontime)<(day*60*60*24):
            print("length:"+str(day*60*60*24))
            print("Now:"+str(time.time()-seasontime))
            if event.message.text.split(" ")[0] == "deposit" or event.message.text.split(" ")[0] == "Deposit":
                bank = fb.get(url+"bank/", None)
                banktimer = fb.get(url+"banktimer/", None)
                season = fb.get(url+"season/", None)
                hours = int((time.time()-banktimer[team[user][0]])//3600)
                for i in range(hours):
                    bank[team[user][0]] *= 1.005
                banktimer[team[user][0]]+=(3600*hours)
                fb.put(url, data=bank, name="bank")
                fb.put(url, data=banktimer, name="banktimer")
                try:
                    if season[team[user][0]][0] - int(event.message.text.split(" ")[1])>=0:
                        season[team[user][0]][0] = season[team[user][0]][0] - int(event.message.text.split(" ")[1])
                        bank[team[user][0]]+=int(event.message.text.split(" ")[1])
                        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="Successfully deposit "+str(int(event.message.text.split(" ")[1]))+" points"))
                        banktimer[team[user][0]]=time.time()
                        fb.put(url, data=season, name="season")
                        fb.put(url, data=bank, name="bank")
                        fb.put(url, data=banktimer, name="banktimer")
                    else:
                        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="Hey yo idiot! You don't have enough points, go fuck someone then come back"))
                except ValueError:
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text="Fuck you!!! Are you Ethan? deposit a number!"))
                except KeyError:
                    if user!="U4e5ae01224117b28f662c288775be0a7":
                        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="you are not in this season, please sign up for the next season to join."))
            if event.message.text.split(" ")[0] == "report" or event.message.text.split(" ")[0] == "Report":
                season=fb.get(url+"season/", None)
                try:
                    if time.time()-team[user][4]>7200:
                        reply=[]
                        if random.randint(1, 2)==1:
                            team[event.message.mention.mentionees[0].user_id][1]=time.time()+3600
                            reply.append(TextSendMessage(text="You reported "+line_bot_api.get_profile(event.message.mention.mentionees[0].user_id).display_name+" to the Gender Equality Committee....."))
                            reply.append(TextSendMessage(text="Success! "+line_bot_api.get_profile(event.message.mention.mentionees[0].user_id).display_name+" is put into jail for 1 hours."))
                        else:
                            team[user][1]=time.time()-900
                            reply.append(TextSendMessage(text="You reported "+line_bot_api.get_profile(event.message.mention.mentionees[0].user_id).display_name+" to the Gender Equality Committee....."))
                            reply.append(TextSendMessage(text="Nope! Seems like "+line_bot_api.get_profile(user).display_name+" wants to fake a crime on "+line_bot_api.get_profile(event.message.mention.mentionees[0].user_id).display_name+" but got caught, so is banned for 15 minutes."))
                        team[user][4]==time.time()
                        fb.put(url, data=team, name="team")
                        line_bot_api.reply_message(event.reply_token, reply)
                    else:
                        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="The police is still fucking, wait for "+str(int((7200-(time.time()-team[user][1]))//60))+"M "+str(int((7200-(time.time()-team[user][1]))%60//1))+"S to report again."))
                except IndexError:
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text="you idiot! Report a person by pinging him/her (no her) like report @EthanB"))
                except KeyError:
                    if user not in team.keys():
                        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="you are not in this season, please sign up for the next season to join."))
                    else:
                        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="Stop right there. Is your brain dead or hand broken? REPORT THE RIGHT WAY!"))
            if event.message.text == "bitch" or event.message.text == "Bitch":
                season = fb.get(url+"season/", None)
                try:
                    if time.time()-team[user][1]>1800:
                        reply = []
                        b = season[team[user][0]][1]
                        b= int(b)
                        if random.random()<((-1)*(0.00000396)*(b-50)*(b-50)*(b-50)+(-1)*(0.0001)*(b-50)+0.5):
                            season[team[user][0]][1] = season[team[user][0]][1]+1
                            fb.put(url, data=season, name="season")
                            reply.append(TextSendMessage(text="Congrats, "+name+", you successfully hired a bitch for your team."))
                        else:
                            reply.append(TextSendMessage(text="Hahaha "+name+" the bitch doesn't like you!"))
                        line_bot_api.reply_message(event.reply_token, reply)
                    else:
                        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="Fuck you son of a bitch, why are you in such a hurry to throw your mother to the other team? You need to wait for "+str(int((1800-(time.time()-team[user][1]))//60))+"M "+str(int((1800-(time.time()-team[user][1]))%60//1))+"S to do so."))
                except KeyError:
                    if user not in team.keys():
                        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="you are not in this season, please sign up for the next season to join."))
                    else:
                        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="Stop right there. Is your brain dead or hand broken? TYPE THE CORRECT TEAM!"))
                team[user][1]=time.time()
                fb.put(url+"team/"+user+"/", data=team[user][1], name=1)
            if event.message.text == "viagra" or event.message.text == "Viagra":
                season = fb.get(url+"season/", None)
                try:
                    if time.time()-team[user][1]>1800:
                        reply = []
                        reply.append(TextSendMessage(text=name+" swallowed a pill of viagra......"))
                        if random.randint(1, 100)>(season[team[user][0]][2]-1)*50:
                            season[team[user][0]][2] = season[team[user][0]][2]+0.02
                            fb.put(url, data=season, name="season")
                            reply.append(TextSendMessage(text="Got a small boost on his dick."))
                        else:
                            reply.append(TextSendMessage(text="Seems like "+name+" is very bad at chemistry, "+name+" uses the wrong ingredients. Nothing happened"))
                        line_bot_api.reply_message(event.reply_token, reply)
                    else:
                        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="You little idiot! Your viagra is still creating. You need to wait for "+str(int((1800-(time.time()-team[user][1]))//60))+"M "+str(int((1800-(time.time()-team[user][1]))%60//1))+"S to get the pill."))
                except KeyError:
                    if user not in totalTeams:
                        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="you are not in this season, please sign up for the next season to join."))
                    else:
                        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="Stop right there. Is your brain dead or hand broken? TYPE THE CORRECT TEAM!"))
                team[user][1] = time.time()
                fb.put(url+"team/"+user+"/", data=team[user][1], name=1)
            if normal(user)==True:
                print("normal user")
                team[user][2] = int(fb.get(url+"team/"+user+"/2/", None))
                print(time.time()-team[user][2])
                print(team[user][3])
                if time.time()-team[user][2]<=15:
                    print("on time")
                    if event.message.text == "fuck" or event.message.text == "Fuck":
                        team[user][3]+=random.randint(100, 500)
                        print("get")
                elif time.time()-team[user][2]>10 and team[user][3]!=0:
                    season[team[user][0]][0]+=team[user][3]
                    fb.put(url, data=season, name="season")
                    reply = TextSendMessage(text="Time's up!, you got "+str(team[user][3])+"points for your team.")
                    team[user][3]=0
                    print("end")
                    line_bot_api.reply_message(event.reply_token, reply)
                else:
                    print("nothing")
            if (event.message.text.split(" ")[0] == "fuck" or event.message.text.split(" ")[0] == "Fuck") and len(event.message.text.split(" "))>1:
                season = fb.get(url+"season/", None)
                bank = fb.get(url+"bank/", None)
                banktimer = fb.get(url+"banktimer/", None)
                special = 0
                try:
                    reply = []
                    if time.time()-team[user][1]>1800:
                        try:
                            if random.randint(1, 100)>season[event.message.text.split(" ")[1]][1]:
                                if random.randint(1, 100)==50:
                                    special = 1
                                if random.randint(1, 20) == 1:
                                    stole = int(random.randint(0, 200)*200*season[team[user][0]][2])
                                    season[team[user][0]][0]+=stole
                                    season[event.message.text.split(" ")[1]][0] -= stole
                                    reply.append(TextSendMessage(text="💥BOOM!!!💥 YOU FUCKED THE HELL OUTTA "+event.message.text.split(" ")[1]+"'s TEAM!!!"))
                                    reply.append(TextSendMessage(text="Took extra points of "+str(stole)))
                                    fb.put(url, data=season, name="season")
                                else:
                                    stole = int(random.randint(0, 200)*100*season[team[user][0]][2])
                                    season[team[user][0]][0]+=stole
                                    season[event.message.text.split(" ")[1]][0]-=stole
                                    reply.append(TextSendMessage(text="success! you fucked "+event.message.text.split(" ")[1]+"'s team and get "+str(stole)+" points."))
                                    fb.put(url, data=season, name="season")
                            else:
                                if random.randint(1, 5) == 1:
                                    stole = int(random.randint(0, 200))
                                    season[team[user][0]][0]-=stole
                                    season[event.message.text.split(" ")[1]][0] += stole
                                    reply.append(TextSendMessage(text="You fucked "+event.message.text.split(" ")[1]+"'s team. But your dick was stucked inside them, so your dick was yanked out of you by "+str(season[event.message.text.split(" ")[1]][1])+" bitches, they beat you up and imprisoned you."))
                                    reply.append(TextSendMessage(text="Your team paid "+str(stole)+" points for ransom."))
                                    fb.put(url, data=season, name="season")
                                else:
                                    reply.append(TextSendMessage(text="You tried to fuck "+event.message.text.split(" ")[1]+"'s team. But you've been beaten up and hurled away by "+str(season[event.message.text.split(" ")[1]][1])+" bitches."))
                            team[user][1]=time.time()
                            fb.put(url+"team/"+user+"/", data=team[user][1], name=1)
                        except AttributeError:
                            reply.append("Fuck you stupid idiot! Decide a team to fuck! Format:fuck theTeamToFuck")
                    else:
                        reply.append(TextSendMessage(text="Fuck you son of a bitch, you need to wait "+str(int((1800-(time.time()-team[user][1]))//60))+"M "+str(int((1800-(time.time()-team[user][1]))%60//1))+"S to fuck again."))
                    if special == 1:
                        print("nigga")
                        reply.append(TextSendMessage(text="⚠️SPECIAL EVENT⚠️ Type as much 'fuck' as you can."))
                        team[user][2]=time.time()
                        fb.put(url+"team/"+user+"/", data=team[user][2], name=2)
                    line_bot_api.reply_message(event.reply_token, reply)         
                except KeyError:
                    if user not in team.keys():
                        if user == "U4e5ae01224117b28f662c288775be0a7":
                            pass
                        else:
                            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="you are not in this season, please sign up for the next season to join."))
                    else:
                        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="Stop right there. Is your brain dead or hand broken? TYPE THE CORRECT TEAM!"))
            season = fb.get(url+"season/", None)
            banktimer = fb.get(url+"banktimer/", None)
            bank = fb.get(url+"bank/", None)
            for i in range(len(list(season.keys()))):
                k=list(season.keys())
                if season[k[i]][0]<0:
                    miss=0-season[k[i]][0]
                    hours = int((time.time()-banktimer[k[i]])//3600)
                    for j in range(hours):
                        bank[k[i]] *= 1.005
                    bank[k[i]]-=miss*2
                    banktimer[k[i]]=time.time()
                    season[k[i]][0]=0
                    fb.put(url, data=bank, name="bank")
                    fb.put(url, data=banktimer, name="banktimer")
                    fb.put(url, data=season, name="season")
        else:
            if seasontime!=0:
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text="Season has ended, please contact the administrator to announce the result or use !stat command to see it yourself."))
    print(group)
    if group in toggle["Debug"]:
        if user == "U4e5ae01224117b28f662c288775be0a7":
            if event.message.text.split(" ")[0] == "!display":
                day = fb.get(url+"day/", None)
                all = fb.get(url, None)
                t = fb.get(url+"team/", None)
                displayList = {"help":"ctime: current time\nttime: total time\nseason: all info in season\nteam: all info in team\ntoggle: current toggles",
                               "ctime":time.time()-seasontime,
                               "ttime":day*60*60*24,
                               "season":all,
                               "team":t,
                               "toggle":toggle
                               }
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text=str(displayList[event.message.text.split(" ")[-1]])))
    if group == "C4b8e02e1ef606a620c7d5e8fd03a4824":
        if user == "U4e5ae01224117b28f662c288775be0a7":
            if event.message.text=="mode fuck":
                mode = "fuck"
            elif event.message.text == "mode echo":
                mode = "echo"
        else:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="FUCK YOU!!!HAHA YOU IDIOT HOW DARE YOU TRY CHANGING MY COMMANDS"))
        if mode=="fuck":
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="FUCK YOU!!!"))
        elif mode=="echo":
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=str(event.message.text)))
    #text = event.message.text
    #reply = 'You said: ' + text
    #line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply))
if __name__ == '__main__':
    app.run()
