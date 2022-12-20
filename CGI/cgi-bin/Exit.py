#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cgi, cgitb, sys, codecs

from Client import SClient
from msg import *

cgitb.enable()
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

form = cgi.FieldStorage()

expires_past_time = 'Wed, 28 Aug 2013 18:30:00 GMT' 

print('Set-Cookie: userId={}; expires={}'.format(str(-1), expires_past_time))
print('Set-Cookie: userName={}; expires={}'.format('Deleted', expires_past_time))

client = SClient(id = int(form.getfirst('uID')))
client.SendMessage(MR_BROKER, MT_EXIT, "")

print("Content-type: text/html\n")
print("""<!DOCTYPE HTML>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Выход из аккаунта</title>
    </head>
    <body>""")

print("""
    <h2>Вы успешно вышли из аккаунта [{}] с ID [{}]</h2>
    <form method='get' action='../index.html'>
        <input type='submit' value='На главную'>
    </form>""".format(form.getfirst('uName'), form.getfirst('uID')))


print('</body></html>')