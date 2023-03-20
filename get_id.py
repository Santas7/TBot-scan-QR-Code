import telebot

bot = telebot.TeleBot(TOKEN)
print(bot.get_chat('@group_testi').id)