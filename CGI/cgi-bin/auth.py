#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cgi,os,sys,codecs,cgitb, http.cookies, datetime
import html
from Client import SClient
from msg import *


cgitb.enable()
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

form = cgi.FieldStorage()
userName = form.getfirst("user_name", '')
userName = html.escape(userName)

#checking cookie
cookie = http.cookies.SimpleCookie(os.environ.get('HTTP_COOKIE'))
uName = cookie.get('userName')
uID = cookie.get('userId')

if len(userName) == 0 and uName is None:
    print("Content-type: text/html\n")
    print("""<!DOCTYPE HTML>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Ошибка авторизации</title>
        </head>
        <body>""")

    print('<h3>Ошибка, не введено имя пользователя.<br>Пожалуйста, введите ваше имя</h3>')
    print("""<form method='get' action="/cgi-bin/auth.py">
        <label>Введите ваше имя: <input type="text" name="user_name"></label><br>
        <button type="submit">Продолжить</button>
    </form>""")
else:
#setting cookie
    if uName is not None:
         uName = uName.value
         uID = uID.value
    else:
        expires = (datetime.datetime.today() + datetime.timedelta(seconds=10))  # time to life cookie
        print("Set-Cookie: userName={}; expires={}".format(userName, expires.strftime('%a %b %d %H:%M:%S %Y')))
        uName=userName                                                          # setting name of client
        client = SClient(name = uName)                                           # creating a new client 
        response = client.SendMessage(MR_BROKER, MT_INIT, uName, True)          # send a message of init to MessageServer
        uID = response.Header.To                                                # set cookie on ID
        print("Set-Cookie: userId={}; expires={}".format(uID, expires.strftime('%a %b %d %H:%M:%S %Y')))

    print("Content-type: text/html\n")
    print("""<!DOCTYPE HTML>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Личный кабинет</title>
        </head>
        <body>""")
    print('<h3>Добро пожаловать, {}</h3>'.format(uName))
    print('<h5>Сервер выдал вам ID: {}</h5>'.format(uID))

    
    print("""<form method='get' action='Chat.py'>
            <input type='submit' name='action' value='Перейти в чат'>
        </form>
        <form method='get' action='Exit.py'>
            <input type='hidden' name='uID' value='{}'>
            <input type='hidden' name='uName' value='{}'>
            <input type='submit' value='Выход'>
        </form>""".format(uID, uName))

print('</body></html>')


