#----------------------------------------------------

token=='ваш телеграм токен'
port='порт открытый на вашей машине, который будет использоваться для связи'

#----------------------------------------------------

import telebot
import threading
import os
import schedule
from flask import Flask, request

#создание телеграм бота с вашим токеном
bot=telebot.TeleBot(token)

#объявление словаря для проверки онлайн ли клиент
OnlineList={}

#функция для отсчета времени для задач Schedule
def timeCheck():
    while True:
        schedule.run_pending()


#запуск функции timc() в параллельный поток
timeCheckT=threading.Thread(target=timeCheck)
timeCheckT.start()


#функция для проверки, кто из клиентов отправил запрос с указанием, что он онлайн
def OnlineCheck():
    global OnlineList
    ClientsOnline=list(OnlineList.keys())
    for client in ClientsOnline:
        if OnlineList[client]==0:
            senderr(client,'Превышено время ожидания с отслеживаемым хостом.')
        OnlineList[client]=0

#Функция запускающая веб-приложение осуществляющее прием сообщений от клиентов
def ServerApp():
    
    #создание Flask веб-приложения
    app = Flask(__name__)

    #отслеживание, если клиент отправит сообщение '/sendMessage', то выполнится функция send_message() 
    @app.route('/sendMessage', methods=['POST'])
    
    #функция обрабатывающая сообщение от клиента и отправляющая нужные данные пользователю в телеграм
    def send_message():
        data = request.json
        senderr(data['message'].split(';')[0],data['message'].split(';')[1])

    #отслеживание, если клиент отправит сообщение '/internet', то выполнится функция OnlineWrite() 
    @app.route('/internet', methods=['POST'])

    #функция, обрабатывающая сообщение от клиента и меняющая/подтверждающая его Online-статус
    def OnlineWrite():
        data = request.json
        global OnlineList
        OnlineList[data['message']]=1

    #запуск веб-приложения, слушающего определенный порт, на определенном локальном адресе
    app.run(host='0.0.0.0', port=int(port))

#запуск веб-приложения в параллельный поток
server=threading.Thread(target=ServerApp)
server.start()


#постановка задач Schedule для проверки, какие клиенты онлайн
schedule.every().hour.at("00:00").do(OnlineCheck)
schedule.every().hour.at("15:00").do(OnlineCheck)
schedule.every().hour.at("30:00").do(OnlineCheck)
schedule.every().hour.at("45:00").do(OnlineCheck)

#функция для отправки пользователю с кодом idu, сообщения ptxt
def senderr(idu,ptxt):
    bot.send_message(idu,ptxt)

#функция для отслеживания команд в сообщениях боту
def cm(a,b):
    return a.text.count(b)==1

#отслеживание, отправки боту сообщений
@bot.message_handler()
def command(mes):
    if cm(mes,'!код'):
        bot.reply_to(mes,mes.chat.id)
bot.infinity_polling()
