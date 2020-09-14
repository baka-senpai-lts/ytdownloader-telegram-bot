import telebot
import os
import pytube
import _thread
import uuid
import shutil


bot = telebot.TeleBot(os.environ['BOT_TOKEN'])

active_users = []

users_in_dialog = []

sessions = {}


YES = ["+", "ага", "ок", "оки", "окц", "окей", "хорошо", "да", "д", "дит", "угу", "конечно", "кнчн", "ну да", "yes", "yep", "yeah", "y", "ok", "okay"]

NO = ["-", "нет", "не ок", "не", "ноу", "нит", "нитб", "нет, конечно", "нет конечно", "нет кнчн", "нет, кнчн", "ты еблан?", "н", "no", "nope", "n"]

START_MESSAGE = "Привет, я умею качать видосики и ставить аниме на аву :3\nКстати, если видосик слишком большой, я могу сжать его\nА еще у меня есть пасхалочка))"

HELP_MESSAGE = "Чтобы я скачал ваш видеоматериал, отправьте мне ссыл очку :3"


def print_log(message, log=""):

    print("{} {} ({}) - {} : {} | {}".format(message.from_user.first_name, message.from_user.last_name, message.from_user.username, sessions[message.from_user.id], message.text, log))


def get_unique_name():

    name = str(uuid.uuid1())

    while name in sessions:
        name = str(uuid.uuid1())

    return name


def message_handling(message):

    if message.text == "/start":

        print("{} {} ({}) : {}".format(message.from_user.first_name, message.from_user.last_name, message.from_user.username, message.text))

        bot.send_message(message.from_user.id, START_MESSAGE)

    elif message.text == "/help":

        print("{} {} ({}) : {}".format(message.from_user.first_name, message.from_user.last_name, message.from_user.username, message.text))

        bot.send_message(message.from_user.id, HELP_MESSAGE)

    elif message.text == "Аква топ вайфу":

        print("{} {} ({}) : {}".format(message.from_user.first_name, message.from_user.last_name, message.from_user.username, message.text))

        bot.send_message(message.from_user.id, "Кстати, мой создатель - такая же бесполезность :3")

    elif message.from_user.id in active_users:

        print_log(message)

        bot.send_message(message.from_user.id, "Падажжи, я занят")

    elif message.from_user.id in users_in_dialog:

        active_users.append(message.from_user.id)

        if message.text.lower() in YES:

            print_log(message, log="Получено подтверждение, начинаю сжатие файла")

            bot.send_message(message.from_user.id, "Сейчас сожму, это займет некоторое время :3")

            #print_log(message, log=os.path.getsize("tmp/{}.zip".format(sessions[message.from_user.id])))

            os.system("ffmpeg -y -v fatal -i tmp/{}.mp4 -b:v 75k tmp/{}_compressed.mp4".format(sessions[message.from_user.id], sessions[message.from_user.id]))

            print_log(message, "Файл сжат")

            if os.path.getsize("tmp/{}_compressed.mp4".format(sessions[message.from_user.id])) < 52428800:
                print_log(message, "Файл прошел проверку, отправляю")

                bot.send_message(message.from_user.id, "Отправляю :3")

                bot.send_video(message.from_user.id, open("tmp/{}_compressed.mp4".format(sessions[message.from_user.id]), "rb"))

                print_log(message, log="Завершаю активную сессию")

            else:
                print_log(message, log="Файл не прошел проверку, завершаю активную сессию")

                bot.send_message(message.from_user.id, "Это фиаско, рил слишком большое(")
            
            os.system("rm tmp/{}.mp4 tmp/{}_compressed.mp4".format(sessions[message.from_user.id], sessions[message.from_user.id]))

            users_in_dialog.pop(users_in_dialog.index(message.from_user.id))
            
            sessions.pop(message.from_user.id)

        elif message.text.lower() in NO:

            print_log(message, log="Получен отказ, завершаю активную сессию")
            
            bot.send_message(message.from_user.id, "Ой, ну как хош :3")

            os.system("rm {}.mp4".format(sessions[message.from_user.id]))

            users_in_dialog.pop(users_in_dialog.index(message.from_user.id))
            
            sessions.pop(message.from_user.id)

        else:

            print_log(message, log="Продолжаю диалог")

            bot.send_message(message.from_user.id, "непон")

        active_users.pop(active_users.index(message.from_user.id))

    else:
        
        active_users.append(message.from_user.id)

        #bot.send_message(message.from_user.id, "я тя пока в диалог отправлю :3")
        #users_in_dialog.append(message.from_user.id)

        sessions.update({ message.from_user.id : get_unique_name() })

        #print("{} - {} : {}".format(message.from_user.username, sessions[message.from_user.id], message.text))


        try:
            video = pytube.YouTube(message.text)

            print_log(message, log="Ссылка валидная, начинаю скачивание")

            bot.send_message(message.from_user.id, "Сейчас скачаю :3")

        except:
            bot.send_message(message.from_user.id, "Ссыл очка неправильная(")

            print_log(message, log="Ссылка не является валидной, завершаю активную сессию")

            sessions.pop(message.from_user.id)

            active_users.pop(active_users.index(message.from_user.id))

            return 0


        title = video.streams.first().download("tmp/", sessions[message.from_user.id])

        print_log(message, log="Файл скачан")

        if os.path.getsize(title) < 52428800:
            print_log(message, log="Файл прошел проверку, отправляю")

            bot.send_message(message.from_user.id, "Скачаль, сейчас отправлю :3")

            bot.send_video(message.from_user.id, open(title, "rb"), timeout=200000)

            print_log(message, log="Файл отправлен, удаляю и завершаю сессию")

            os.system("rm {}".format(title))
            
            sessions.pop(message.from_user.id)

        else:
            print_log(message, log="Файл не прошел проверку, вступаю в диалог")

            bot.send_message(message.from_user.id, "Это видео слишком большое, чтобы отправить его просто так(\nМожно сжать? :3")
            
            users_in_dialog.append(message.from_user.id)

        active_users.pop(active_users.index(message.from_user.id))


@bot.message_handler(content_types=["text"])

def get_text_messages(message):

    _thread.start_new_thread(message_handling, (message, ))


bot.polling(none_stop=True, interval=0)
