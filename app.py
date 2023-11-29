import telebot
import threading
import os
import schedule
from flask import Flask, request

#----------------------------------------------------

token="6712996073:AAFx9dx4ZDEHk-fkxNbM9qt-kQ3kmaptNjk"
portt=80

#----------------------------------------------------

bot=telebot.TeleBot(token)
internt={}
def timc():
    while True:
        schedule.run_pending()
timcc=threading.Thread(target=timc)
timcc.start()
def ggt():
    global internt
    intr=list(internt.keys())
    for i in intr:
        if internt[intr]==0:
            senderr(intr,'Превышено время ожидания с отслеживаемым хостом.')
        internt[intr]=0
        
def sockt():
    app = Flask(__name__)

    @app.route('/sendMessage', methods=['POST'])
    def send_message():
        data = request.json
        senderr(data['message'].split(';')[0],data['message'].split(';')[1])
    @app.route('/internet', methods=['POST'])
    def internet():
        data = request.json
        global internt
        internt[data['message']]=1
    app.run(host='0.0.0.0', port=portt)
sck=threading.Thread(target=sockt)
sck.start()
schedule.every().hour.at("00:00").do(ggt)

schedule.every().hour.at("15:00").do(ggt)

schedule.every().hour.at("30:00").do(ggt)

schedule.every().hour.at("45:00").do(ggt)

def senderr(idu,ptxt):
    bot.send_message(idu,ptxt)

def cm(a,b):
    return a.text.count(b)==1

@bot.message_handler()
def al(mes):
    if cm(mes,'!код'):
        bot.reply_to(mes,mes.chat.id)
bot.infinity_polling()
