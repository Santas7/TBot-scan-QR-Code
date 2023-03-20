import os
import telebot
import cv2
from telebot import types
from pyzbar.pyzbar import decode
from PIL import Image

bot = telebot.TeleBot(TOKEN)
NUMBER = 1


@bot.message_handler(commands=['start'])
def start(message):
    """
        function is start bot (command /start)
    """
    # create panel buttons
    panel = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # create main buttons
    btn_1 = types.KeyboardButton('📸Qr-Code Scanning')
    # added buttons in panel
    panel.add(btn_1)
    bot.send_message(message.chat.id, 'Hi! I am a qr-code scanning bot!', reply_markup=panel)


@bot.message_handler(content_types=["text"])
def text(message):
    global NUMBER
    chat_id = message.chat.id
    if message.text == '📸Qr-Code Scanning':
        bot.send_message(message.chat.id, 'Send me your qr-code and hit send!')
    else:
        bot.send_message(message.chat.id, 'Error! I dont understand you!')


@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    global NUMBER
    bot.send_message(message.chat.id, 'Data successfully accepted, wait for results...')

    file_info = bot.get_file(message.photo[-1].file_id)
    file = bot.download_file(file_info.file_path)

    with open(f'img/{NUMBER:05d}.jpg', 'wb') as f:
        f.write(file)
    bot.send_message(message.chat.id, 'Processing...')

    # upload image
    img = Image.open(f'img/{NUMBER:05d}.jpg')
    data = decode(img)

    if os.path.exists(f'img/{NUMBER:05d}.jpg'):
        os.remove(f'img/{NUMBER:05d}.jpg')
    # output results
    if data:
        bot.send_message(message.chat.id, f'The QR code contains data: {data[0].data.decode("utf-8")}')
        bot.send_message(message.chat.id, f'Photo send is {message.from_user.first_name} {message.from_user.last_name}')
        bot.send_message(GROUP_CHAT_ID, ".")
    else:
        bot.send_message(message.chat.id, 'QR code not found in the image')


# start bot
bot.polling()