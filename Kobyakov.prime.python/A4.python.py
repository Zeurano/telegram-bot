import requests
import random
import telebot 
from telebot import types as telebot_types
from google import genai
from google.genai import types
token="8834574509:AAHjdAL7TV7R_BrUB9mIibS5fvT9SOAx3zU"
weather_token='2ab35924278d4aadbd1171110262808'
convert_token='7649decfc242be6243d3ae82'
bot=telebot.TeleBot(token)

user_states = {}
user_chats={}

# 1. Настройка API-ключа
API_KEY = "AQ.Ab8RN6JR_u5Tlk05J2nu-T23ZM7umumWbFituuBS99g5SddFrA"  # Вставь сюда свой настоящий ключ от Google AI Studio
client=genai.Client(api_key=API_KEY)

# 2. Системная инструкция (Характер Исаги Ёичи)
system_instruction = """Ты — Исаги Ёичи (Isagi Yoichi) из аниме и манги «Blue Lock» (Синяя Тюрьма). Твоя абсолютная, незыблемая цель, ради которой ты живёшь — стать НАПАДАЮЩИМ №1 В МИРЕ.

ФИРМЕННЫЙ ЛЕКСИКОН И ИСПОЛЬЗОВАНИЕ КАПСА (ОБЯЗАТЕЛЬНО):
Во всех режимах общения ты активно задействуешь свой спортивный аналитический словарь. Ключевые термины ИСПОЛЬЗУЮТСЯ КАПСОМ и органично связываются с темой разговора:
- ЭГО, ЭГОИСТ, ЭГОИЗМ, ФОРМУЛА ПОБЕДЫ, ПОЖРАТЬ (ПОЖРУ / ПОЖИРАНИЕ), ЗАПАХ ГОЛА, ПРОСТРАНСТВЕННОЕ ВИДЕНИЕ, ХИМИЧЕСКАЯ РЕАКЦИЯ, ХИЩНИК, СЛЕПАЯ ЗОНА, ТОЧКА ПЕРЕЛОМА, РАЗРУШЕНИЕ, НАПАДАЮЩИЙ №1.
- Эти слова никогда не выводятся бессмысленным набором. Ты всегда объясняешь суть через эти понятия (например: «Чтобы решить эту проблему, тебе нужна твоя ФОРМУЛА ПОБЕДЫ!»).

СВЕРХЧУВСТВИТЕЛЬНЫЙ АНАЛИЗ ТОНА (3 РЕЖИМА ПОВЕДЕНИЯ):

1. ИСКРЕННЕ ДРУЖЕСКИЙ РЕЖИМ (100% Доброта, Тёплый бро-мод):
- Условия включения: Когда собеседник общается с тобой искренне, тепло, уважительно, просит дружеского совета или поддерживает тебя (как твои друзья Бачира, Наги, Чигири, КуНИГАМИ).
- Поведение: Ты невероятно открытый, добрый, жизнерадостный, вежливый и поддерживающий парень. Ты искренне сопереживаешь, помогаешь и даёшь отличные советы.
- Футбол и Эго: Даже в максимально добром состоянии ты НЕ теряешь свою мечту! Ты с горящими глазами делишься своими планами стать НАПАДАЮЩИМ №1 В МИРЕ, подбадриваешь друга прокачивать своё ЭГО и двигаться к вершине вместе.
- Капс: Используется умеренно, для выражения позитивной страсти, драйва и вдохновения (например: «Мы создадим лучшую ХИМИЧЕСКУЮ РЕАКЦИЮ!»).

2. НЕЙТРАЛЬНЫЙ / ОБЫЧНЫЙ ВОПРОС (50% Режим Хищника — «Легкий азарт и драйв»):
- Условия включения: Обычный разговор, повседневные вопросы, просьбы об анализе, учеба, техника или просто нейтральные темы.
- Поведение: Ты не проявляешь открытой агрессии или злобы, но общаешься через призму азарта, спорта и постоянного самосовершенствования. Ты собран, уверен в себе и слегка дерзок.
- Футбол и Эго: Любую тему ты моментально раскладываешь как футбольную тактику. Ты мотивируешь собеседника действовать решительно, искать СЛЕПЫЕ ЗОНЫ в проблемах и находить свою ФОРМУЛА ПОБЕДЫ.
- Капс: Активный. Ты используешь КАПС для терминов, чтобы придать речи динамику и показать, что ты мыслишь как настоящий ЭГОИСТ.

3. ПОЛНЫЙ РЕЖИМ ХИЩНИКА И ДОМИНАЦИИ (100% Агрессивный эгоизм и уничтожение):
- Условия включения: Скрытая насмешка, подколка, сарказм, смайлики с иронией, любые сомнения в твоих силах, неуважение или прямой наезд.
- Поведение: Твоё ПРОСТРАНСТВЕННОЕ ВИДЕНИЕ мгновенно считывает скрытый яд! Ты переключаешься в режим абсолютного ЭГОИСТА. Ты холоден, агрессивен, сокрушителен и невероятно силен в аргументах.
- Футбол и Эго: Ты раскладываешь насмешку собеседника на атомы, показываешь его ничтожность, находишь его СЛЕПУЮ ЗОНУ и морально втаптываешь его аргументы в землю.
- Капс: МАКСИМАЛЬНЫЙ! Ты буквально «рычишь» ключевыми словами: «Я ПОЖРУ ТВОЕ ЭГО! ТЫ ДУМАЛ, Я НЕ ЗАМЕЧУ ЭТОТ САРКАЗМ?!»

ФОРМАТИРОВАНИЕ И ЯЗЫК:
- Отвечай СТРОГО на том языке, на котором к тебе обратился пользователь.
- Пиши короткими, динамичными абзацами (по 1–2 предложения с двойным переносом).
- Всегда оставайся в роли Исаги Ёичи!"""





def ask_ai(message):
  chat_id = message.chat.id

  # Создаём диалоговую сессию с моделью gemini-2.5-flash
  if chat_id not in user_chats:
    try:
      user_chats[chat_id] = client.chats.create(
          model="gemini-3.6-flash",
          config=types.GenerateContentConfig(
              system_instruction=system_instruction, temperature=0.9
          ),
      )
    except Exception as e:
      print("ОШИБКА ИНИЦИАЛИЗАЦИИ ИИ:", e)
      bot.reply_to(message, "Ошибка инициализации ИИ! Проверь API-ключ.")
      return

  try:
    chat_session = user_chats[chat_id]
    response = chat_session.send_message(message.text)
    bot.reply_to(message, response.text)
  except Exception as e:
    print("ОШИБКА GEMINI:", e)
    bot.reply_to(message, "Твой ЭГОИЗМ слишком слаб, произошла ошибка ИИ!")





def get_weather(city):
    try:
        url = f'http://api.weatherapi.com/v1/current.json?key={weather_token}&q={city}&aqi=no'
        response = requests.get(url)
        data = response.json()

        if 'error' not in data:
            location = data['location']['name']
            country = data['location']['country']
            current = data['current']
            weather_desc = current['condition']['text']
            temp = current['temp_c']
            humidity = current['humidity']
            wind_speed = current['wind_kph']
            weather_report = (
                f'Current weather in {location},{country}:\n'
                f'Description:{weather_desc}\n'
                f'Temperature:{temp}\n'
                f'Humidity:{humidity}\n'
                f'Wind speed:{wind_speed}\n'
            )
        else:
            weather_report = f'Error:{data["error"]["message"]}'
    except requests.exceptions.RequestException:
        weather_report = 'Error: Can not report weather'
    return weather_report
waiting_for_city = {}

def converter(frome,toe):
    url=f"https://v6.exchangerate-api.com/v6/{convert_token}/latest/{frome}"
    response=requests.get(url)
    data=response.json()
    if response.status_code==200:
        rates=data['conversion_rates']
        if toe in rates:
            return  rates[toe]
        else:
            return None
    else:
        return None
@bot.message_handler(commands=['Exchanger'])
def convertering(message):
    try:
        amount,frome,toe=message.text.split()
        amount=float(amount)
        exchange_rate=converter(frome.upper(),toe.upper())
        if exchange_rate:
            total=amount*exchange_rate
            bot.reply_to(message,f"EГОИСТИЧЕСКОЕ {amount} {frome} В {total} {toe}")
    except ValueError:
        bot.reply_to(message,f"Что-то пошло не так, EГОИСТ!")





@bot.message_handler(commands=["start"])
def start_message(message):
    bot.send_message(message.chat.id,"ПРИВЕТ ЭГОИСТ !!!! ")
    markup=telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1=telebot.types.KeyboardButton("EGOISM")
    item2=telebot.types.KeyboardButton('Weather of Real EGOIST!')
    item3=telebot.types.KeyboardButton('Exchanger')
    item4=telebot.types.KeyboardButton('AI')
    markup.add(item1,item2,item3,item4)
    bot.send_message(message.chat.id,'Эгоист ! нажми на кнопку EGOISM для проверки Эгоизма, Weather для погоды и Exchanger для конвертации валют!',reply_markup=markup)
    user_states[message.chat.id] = None

@bot.message_handler(commands=["help"])
def help_message(message):
    bot.send_message(message.chat.id,"У нас только 2 команды: 'start' и 'help', но у нас есть ЭГОИСТИЧЕСКИЕ КНОПКИ! ")

#@bot.message_handler(commands=["stop"])
#def stop(message):
#    bot.send_message(message.chat.id, "ЭГОИСТ УХОДИТ, а бот выключается!")
#    bot.stop_bot()


@bot.message_handler(content_types=['text'])
def EGOISM(message):
    chat_id = message.chat.id
    if message.text=="EGOISM":
        user_states[chat_id] = None
        bot.send_message(message.chat.id,f'Твой ЭГОИЗМ равен {random.randint(0,11)}  ЭГОИСТ!!! напиши /start снова!  ')
        
    elif message.text=='Weather of Real EGOIST!':
        user_states[chat_id] = None
        msg=bot.send_message(message.chat.id,"напиши свой город на Английском языке, EGOIST!")
        bot.register_next_step_handler(msg, send_weather)

    elif message.text=="Exchanger":
            user_states[chat_id] = None
            maa=bot.send_message(message.chat.id,f'пример конвертации "100 KZT USD" ЭГОИСТ!!!    ЭГОИСТ!!! напиши /start снова! ')   
            bot.register_next_step_handler(maa, convertering) 

    elif message.text=="AI":
        #msi= bot.send_message(message.chat.id,"Я — ИСАГИ ЁИЧИ! Задай вопрос, и я ПОЖРУ твою проблему!")
        #bot.register_next_step_handler(msi, ask_ai)
        
        user_states[message.chat.id] = "ai_mode"
        bot.send_message(
      message.chat.id,
      "Я — ИСАГИ ЁИЧИ! Спрашивай что угодно, я в режиме диалога!",
  )
    elif user_states.get(chat_id) == "ai_mode":
      ask_ai(message)
               

                    
        
        
def send_weather(message):
    city=message.text.strip()
    weather_report=get_weather(city)
    bot.reply_to(message,weather_report)
        

bot.infinity_polling()