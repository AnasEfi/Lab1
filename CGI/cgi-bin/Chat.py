#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8

import cgi, cgitb, codecs, sys, os, http.cookies
from email import message
from pickle import TRUE
from time import sleep
from Client import SClient
from msg import *
from dataclasses import dataclass

cgitb.enable()
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

def LoadTpl(tplName):
    docrootname = 'PATH_TRANSLATED'
    with open(os.environ[docrootname]+'/tpl/'+tplName+'.tpl', 'rt') as f:
        return f.read().replace('{currentLink}', os.environ['SCRIPT_NAME'])

class ChatMessage:
    def __init__(self):
        self.From = 0
        self.To = 0
        self.Type = 0
        self.Text = ''
    
    def SetData(self, From, To, Type, Text) -> None:
        self.From = From
        self.To = To
        self.Type = Type
        self.Text = Text
    
    def Show(self):
        print (LoadTpl('chatMsg').format(**self.__dict__))

class Chat:
    
    uid = -1
    messages = []

    def __init__(self):
        self.messages = []
    
    def ShowMessages(self, countMessages):
        i = 0
        reversedMessages = self.messages[::-1]
        while i < countMessages:
            if i >= len(reversedMessages):
                break
            reversedMessages[i].Show()
            i = i + 1
    
    # add message at local chat
    def AddMessage(self, receivedMessage : Message):
        message = ChatMessage()
        message.SetData(receivedMessage.Header.From, receivedMessage.Header.To, receivedMessage.Header.Type, receivedMessage.Data)
        self.messages.append(message)

# Проверить наличие кук
# Загрузить чат
# Загрузить возможность писать в чат

cookie = http.cookies.SimpleCookie(os.environ.get('HTTP_COOKIE'))
uName = cookie.get('userName')
uID = cookie.get('userId')

if uName is None or uID is None:
    print("""Content-Type: text/html\n
        <DOCTYPE HTML>
        <html><head><meta charset='utf-8'></head><body>
            <h2>Вы не авторизованы, чтобы использовать чат</h2>
            <form method='get' action='../index.html'>
                <input type='submit' value='На главную'>
            </form>
        </body></html>
    """)
    quit()

uName = uName.value
uID = uID.value

# Клиент для взаимодействия с MessageServer (клиентский сокет)
client = SClient(name = uName, id = int(uID))

# Если человек нажал кнопку отправить сообщение, то его переадресует вновь сюда, но уже с параметрами:
# messageText - текст сообщения
# to - кому отправить (All всем)
form = cgi.FieldStorage()
messageText = form.getfirst('messageText', None)
messageTo = form.getfirst('to', None)
messageConfirm = None


# Проверим, пришли ли параметры, если да, то отправим в чат сообщение а уже после будем загружать чат
if messageText is not None and messageTo is not None:
    # Отпрвляем сообщение в чат
   
    if str(messageTo) == 'All':
        messageTo = MR_ALL
    
    try:

        messageTo = int(messageTo)

        if messageTo == MR_STORAGE:
            messageConfirm = "Недопустимый ID"
            sys.exit(1)

        message = client.SendMessage(messageTo, MT_DATA_WITH_RESPONSE, messageText, True)

        if message.Header.Type == MT_CONFIRM: 
            messageConfirm = message.Data
        elif message.Header.Type == MT_NOUSER:
            messageConfirm = "Пользователя с данным ID не найдено"
        else:
           messageConfirm = "Невозможно сохранить сообщение в StorageServer, тип: {}, from: {}, to: {}, text: {}".format(message.Header.Type, message.Header.From, message.Header.To, message.Data)
        sleep(1.5)
    except:
        print('<h1>Укажите корректный ID получателя или All для отправки всем</h1>')

# get 10 last messages

chat = Chat()

# Обработать ошибку MT_CONNECT_ERROR
reqMessages = 10
for i in range(reqMessages):
    response = client.SendMessage(MR_BROKER, MT_GETDATA_WITH_OFFSET, i, True)
    if response.Header.Type == MT_AUTH_ERROR:
        print("""Content-Type: text/html\n
        <DOCTYPE HTML>
        <html><head><meta charset='utf-8'></head><body>
            <h2>Для взаимодействия с чатом необходима авторизация</h2>
            <a href='../index.html'>На главную</a>""")
        quit()

    if response.Header.Type == MT_NO_FOUND_MESSAGE or response.Header.Type == MT_CONNECT_ERROR:
        continue
    chat.AddMessage(response)

#print('[Всего сообщений получено {}] Получено сообщение от сервера сообщений: {}'.format(str(len(chat.messages)), str(response.Data)))

print("""Content-Type: text/html\n
        <DOCTYPE HTML>
        <html><head><meta charset='utf-8'></head><body>
            <h2>Добро пожаловать в чат, {}. Ваш ID: {}</h2>
            <h3>Текущий чат:</h3><br>
            
""".format(uName, uID))

for msg in chat.messages:
    msg.Show()

if messageConfirm is not None:
    print("<h2>Внимание! {} </h2>".format(messageConfirm))

print("""<form method='get' action='chat.py'>
            <input type='submit' value='Обновить чат'>
            </form>
        <br>
        <form method='get' action='chat.py'>
            <label>
                Напишите ваше сообщение <input type='text' name='messageText'>
            <label><br>
            <label>
                Кому отправить <input type='text' name='to'>
            <label><br>
            <input type='submit' value='Отправить'>
        </form><br>
        <form method='get' action='auth.py'>
            <input type='submit' value='В личный кабинет'>
        </form>""")
print('</body></html>')
