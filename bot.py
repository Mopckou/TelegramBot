import telebot, config, btc, random, threading, time, math


bot = telebot.TeleBot(config.token)
contact_list = []
last_price = 0

@bot.message_handler(content_types=['text'])
def message(msg):
    global contact_list
    msg_list = ['btc', 'биток', 'курс биткоина', 'Btc', 'BTC', 'биточек', 'курс бтк', 'биткоин', 'БТК', 'бтк', 'Курс биткоина']
    if msg.text in msg_list:
        send_btc(msg)
    elif msg.text == 'Старт':
        start_monitor(contact_list, msg)
    elif msg.text == 'Стоп':
        stop_monitor(contact_list, msg)
    else:
        bot.send_message(msg.chat.id, random_message())


def send_btc(msg):
    price_list = update_course()
    if price_list is not None:
        bot.send_message(msg.chat.id, 'курс биткоина = %s$' % price_list[0])
    else:
        bot.send_message(msg.chat.id, 'price list none')


def stop_monitor(contact_list, msg):
    if msg.chat.id in contact_list:
        contact_list.remove(msg.chat.id)
    else:
        bot.send_message(msg.chat.id, 'Монитор не запущен. Напишите "Старт"')


def start_monitor(contact_list, msg):
    if msg.chat.id not in contact_list:
        contact_list.append(msg.chat.id)
    else:
        bot.send_message(msg.chat.id, 'Монитор уже запущен.')


def random_message():
    msg = ['ajo', 'дрог', 'алго', 'НИЧОСЕ', 'НИПОНИЛ', 'ТЫ ЧО', 'КУПИЛ БИТОЧЕК?????????', 'ДРУ ДРО ДРА ДРЫ', 'КАМАПУЛЯ', 'ты чо попутал?', 'о братан', 'напиши мне "курс биткоина"', 'ЭЭЭ СЛЮЩАЙ ИДИ СЮДА ДА']
    index = random.randrange(len(msg))
    return msg[index]

def update_course():
    req = btc.get_inquiry()
    if req is not None:
        return btc.btc_in_usd(req)

class my_thread(threading.Thread):
    def run(self):
        global contact_list, last_price
        while 1:
            try:
                if contact_list != 0:
                    price_list = update_course()
                    if (price_list is not None) and check_change_btc(last_price, price_list[0]):
                        last_price = price_list[0]
                        for contact in contact_list:
                            bot.send_message(contact, "Время - %s\n"
                                                      "Текущая максимальная цена покупки = %s$\n"
                                                      "Текущая минимальная цена продажи = %s$\n"
                                                      "Цена последней сделки = %s$\n" % (time.ctime()[11:-5], price_list[0], price_list[1], price_list[2]))
                    time.sleep(10)
            except Exception as detail:
                print(detail)

def check_change_btc(buy_price, last_price):
    return math.fabs(float(buy_price) - float(last_price)) > 100


if __name__ == '__main__':
    my_thread().start()
    bot.polling(none_stop=True)