import telebot 
from config import token
from logic import Pokemon, Wizard, Fighter
from random import randint



bot = telebot.TeleBot(token) 

@bot.message_handler(commands=['go'])
def go(message):
    username = message.from_user.username
    if username not in Pokemon.pokemons:
        chance = randint(1, 5)  # 1 из 5 — Wizard, 1 из 5 — Fighter, остальные — обычный
        if chance == 1:
            pokemon = Wizard(username)
        elif chance == 2:
            pokemon = Fighter(username)
        else:
            pokemon = Pokemon(username)
        bot.send_message(message.chat.id, pokemon.info())
        bot.send_photo(message.chat.id, pokemon.show_img())
    else:
        bot.reply_to(message, "Ты уже создал себе покемона")


@bot.message_handler(commands=['attack'])
def attack(message):
    if message.reply_to_message:
        attacker = message.from_user.username
        target = message.reply_to_message.from_user.username

        if attacker in Pokemon.pokemons and target in Pokemon.pokemons:
            pok = Pokemon.pokemons[attacker]
            enemy = Pokemon.pokemons[target]
            result = pok.attack(enemy)
            bot.send_message(message.chat.id, result)
        else:
            bot.send_message(message.chat.id, "Сражаться могут только покемоны. Убедись, что оба игрока создали своих покемонов.")
    else:
        bot.send_message(message.chat.id, "Чтобы атаковать, ответь на сообщение игрока, которого хочешь атаковать.")


@bot.message_handler(commands=['heal'])
def heal(message):
    username = message.from_user.username
    if username in Pokemon.pokemons:
        pok = Pokemon.pokemons[username]
        result = pok.heal()
        bot.send_message(message.chat.id, result)
    else:
        bot.send_message(message.chat.id, "У тебя ещё нет покемона. Создай его командой /go.")


@bot.message_handler(commands=['info'])
def pokemon_info(message):
    username = message.from_user.username
    if username in Pokemon.pokemons:
        pok = Pokemon.pokemons[username]
        bot.send_message(message.chat.id, pok.info())
    else:
        bot.send_message(message.chat.id, "У тебя ещё нет покемона. Создай его с помощью команды /go.")


@bot.message_handler(commands=['feed'])
def feed_pokemon(message):
    username = message.from_user.username
    if username in Pokemon.pokemons:
        pok = Pokemon.pokemons[username]
        # Проверим, есть ли метод feed (он есть только у Wizard и Fighter)
        if hasattr(pok, 'feed'):
            response = pok.feed()
            bot.send_message(message.chat.id, response)
        else:
            bot.send_message(message.chat.id, "Этот покемон не умеет получать корм. Только покемоны-волшебники и бойцы могут питаться.")
    else:
        bot.send_message(message.chat.id, "У тебя пока нет покемона. Создай его с помощью /go.")


bot.infinity_polling(none_stop=True)

