# -*- coding: utf-8 -*-

import logging
from linebot import LineBotApi, WebhookParser, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage
from linebot.models import TextSendMessage
import os

from flask import Flask, request
import random
import time
import math

from firebase import firebase
url = 'https://fuck-ae07c-default-rtdb.firebaseio.com/'
fb = firebase.FirebaseApplication(url, None)

comp = {}
boost = {}
w = []
season = {}
team = {}
totalTeams=[]
seasontime=0
mode = "echo"
toggle = "None" #None Competitoin Season
#################
#import openai
	
#openai.api_key = os.getenv("OPENAI_API_KEY")
line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
#parser = WebhookParser(os.getenv("LINE_CHANNEL_SECRET"))
handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET")) 

'''
conversation = []

#class ChatGPT:  
    

#    def __init__(self):
        
#        self.messages = conversation
#        self.model = os.getenv("OPENAI_MODEL", default = "gpt-3.5-turbo")



    def get_response(self, user_input):
        conversation.append({"role": "user", "content": user_input})
        

        response = openai.ChatCompletion.create(
	            model=self.model,
                messages = self.messages

                )

        conversation.append({"role": "assistant", "content": response['choices'][0]['message']['content']})
        
        print("AI回答內容：")        
        print(response['choices'][0]['message']['content'].strip())


        
        return response['choices'][0]['message']['content'].strip()
	



#chatgpt = ChatGPT()
'''

app = Flask(__name__)
#run_with_ngrok(app)   #starts ngrok when the app is run

@app.route("/")
def hello():
	return "Hello World from Flask in a uWSGI Nginx Docker container with \
	     Python 3.8 (from the example template)"
         
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
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
    global seasontime
    group = event.source.group_id
    user = event.source.user_id
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
            toggle = event.message.text.split(" ")[1]
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="Successfully toggle to "+toggle))
        else:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="fuck you cheater"))
    if toggle == "Competition":
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
    if toggle == "Season":
        if event.message.text.split(" ")[0] == "!join":
            if user == "U4e5ae01224117b28f662c288775be0a7":
                for i in event.message.mention.mentionees:
                    x = []
                    x.append(event.message.text.split(" ")[-1])
                    print(event.message.text.split(" "))
                    x.append(0)
                    x.append(0)
                    x.append(0)
                    team[i.user_id] = x
                    if x[0] not in totalTeams:
                        totalTeams.append(x[0])
                season[event.message.text.split(" ")[-1]] = [100000, 0, 1]
                fb.put(url, data=season, name="season")
                fb.put(url, data=team, name="team")
                fb.put(url, data=totalTeams, name="totalTeams")
        if event.message.text == "stat" or event.message.text == "stats" or event.message.text == "Stat" or event.message.text == "Stats":
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=str(season)))
        if event.message.text == "!start season":
            if user == "U4e5ae01224117b28f662c288775be0a7":
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
                line_bot_api.reply_message(event.reply_token, reply)
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
        if time.time()-seasontime<1209600:
            if event.message.text == "bitch" or event.message.text == "Bitch":
                if time.time()-team[user][1]>1800:
                    try:
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
                    except KeyError:
                        if user not in totalTeams:
                            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="you are not in this season, please sign up for the next season to join."))
                        else:
                            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="Stop right there. Is your brain dead or hand broken? TYPE THE CORRECT TEAM!"))
                    team[user][1]=time.time()
                    fb.put(url+"team/"+user+"/", data=team[user][1], name=1)
                else:
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text="Fuck you son of a bitch, why are you in such a hurry to throw your mother to the other team? You need to wait for "+str(int((1800-(time.time()-team[user][1]))//60))+"M "+str(int((1800-(time.time()-team[user][1]))%60//1))+"S to do so."))
            if event.message.text == "viagra" or event.message.text == "Viagra":
                if time.time()-team[user][1]>1800:
                    try:
                        reply = []
                        reply.append(TextSendMessage(text=name+" swallowed a pill of viagra......"))
                        if random.randint(1, 100)>(season[team[user][0]][2]-1)*50:
                            season[team[user][0]][2] = season[team[user][0]][2]+0.02
                            fb.put(url, data=season, name="season")
                            reply.append(TextSendMessage(text="Got a small boost on his dick."))
                        else:
                            reply.append(TextSendMessage(text="Seems like "+name+" is very bad at chemistry, instead of C22H30N6O4S, he used C22H30N4O2S2. Nothing happened"))
                        line_bot_api.reply_message(event.reply_token, reply)
                    except KeyError:
                        if user not in totalTeams:
                            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="you are not in this season, please sign up for the next season to join."))
                        else:
                            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="Stop right there. Is your brain dead or hand broken? TYPE THE CORRECT TEAM!"))
                    team[user][1] == time.time()
                    fb.put(url+"team/"+user+"/", data=team[user][1], name=1)
                else:
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text="Fuck you son of a bitch, why are you in such a hurry to throw your mother to the other team? You need to wait for "+str(int((1800-(time.time()-team[user][1]))//60))+"M "+str(int((1800-(time.time()-team[user][1]))%60//1))+"S to do so."))
            if normal(user)==True:
                if time.time()-team[user][2]<=10:
                    if event.message.text == "fuck" or event.message.text == "Fuck":
                        team[user][3]+=5
                elif time.time()-team[user][2]>10 and team[user][3]!=0:
                    season[team[user][0]][0]+=team[user][3]
                    fb.put(url, data=season, name="season")
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text="Time's up!, you got "+str(team[user][3])+"points for your team."))
                    team[user][3]==0
            if (event.message.text.split(" ")[0] == "fuck" or event.message.text.split(" ")[0] == "Fuck") and len(event.message.text.split(" "))>1:
                try:
                    reply = []
                    special = 0
                    if time.time()-team[user][1]>1800:
                        try:
                            if random.randint(1, 100)>season[event.message.text.split(" ")[1]][1]:
                                if random.randint(1, 100)==50:
                                    special = 1
                                if random.randint(1, 20) == 1:
                                    stole = random.randint(0, 200)*200*season[team[user][0]][2]
                                    season[team[user][0]][0]+=stole
                                    season[event.message.text.split(" ")[1]][0] -= stole
                                    reply.append(TextSendMessage(text="💥BOOM!!!💥 YOU FUCKED THE HELL OUTTA "+event.message.text.split(" ")[1]+"'s TEAM!!!"))
                                    reply.append(TextSendMessage(text="Took extra points of "+str(stole)))
                                    fb.put(url, data=season, name="season")
                                else:
                                    stole = random.randint(0, 200)*100*season[team[user][0]][2]
                                    season[team[user][0]][0]+=stole
                                    season[event.message.text.split(" ")[1]][0]-=stole
                                    reply.append(TextSendMessage(text="success! you fucked "+event.message.text.split(" ")[1]+"'s team and get "+str(stole)+" points."))
                                    fb.put(url, data=season, name="season")
                            else:
                                if random.randint(1, 5) == 1:
                                    stole = random.randint(0, 200)
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
                        reply.append(TextSendMessage(text="⚠️SPECIAL EVENT⚠️ Type as much 'fuck' as you can."))
                    line_bot_api.reply_message(event.reply_token, reply)
                    team[user][2]==time.time()
                    fb.put(url+"team/"+user+"/", data=team[user][2], name=2)
                except KeyError:
                    if user not in totalTeams:
                        if user == "U4e5ae01224117b28f662c288775be0a7":
                            pass
                        else:
                            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="you are not in this season, please sign up for the next season to join."))
                    else:
                        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="Stop right there. Is your brain dead or hand broken? TYPE THE CORRECT TEAM!"))
                
        else:
            if seasontime!=0:
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text="Season has ended, please contact the administrator to announce the result or use !stat command to see it yourself."))
    print(group)
    if group == "C4b8e02e1ef606a620c7d5e8fd03a4824":
        if event.message.text=="mode fuck":
            mode = "fuck"
        elif event.message.text == "mode echo":
            mode = "echo"

        if mode=="fuck":
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="FUCK YOU!!!"))
        elif mode=="echo":
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=str(event.message.text)))
    #text = event.message.text
    #reply = 'You said: ' + text
    #line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply))
    






if __name__ == '__main__':
	    app.run(debug=True, port=os.getenv("PORT", default=5000))
