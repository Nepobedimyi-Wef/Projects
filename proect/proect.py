import os
import telebot
import speech_recognition as sr
import librosa
import soundfile as sf
import requests
import base64
import urllib3
import json
import time
import logging
from io import BytesIO
from PIL import Image
from gtts import gTTS
import tempfile
import re

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

bot = telebot.TeleBot("8207839620:AAH8sgsnS5XhGnnzVRbjGPhnc_ihAIaXeFk")

CLIENT_ID = "0199d69e-6286-7bca-8023-233f0896bb58"
CLIENT_SECRET = "64696851-27b0-4755-aab7-0bb089d8e5a8"

KANDINSKY_URL = 'https://api-key.fusionbrain.ai/'
KANDINSKY_API_KEY = '11AEF3776EBCFEB61F0754EE5B79364C'
KANDINSKY_SECRET_KEY = 'AF576A16CA4DEDF0D0D238D4ADF51CB2'

VOICE_MESSAGE_DIR = "temp_voice_messages"


class FusionBrainAPI:
    def __init__(self, url, api_key, secret_key):
        self.URL = url
        self.AUTH_HEADERS = {
            'X-Key': f'Key {api_key}',
            'X-Secret': f'Secret {secret_key}',
        }

        self.FOOD_STYLES = {
            "1": "📸 Фотореалистичный",
            "2": "🎨 Профессиональная фуд-фотография",
            "3": "🖼️ Художественный стиль",
            "4": "🌊 Акварельный скетч",
            "5": "⚫ Минимализм",
            "0": "🚫 Без стиля"
        }

        self.FOOD_STYLE_PROMPTS = {
            "1": "фотореалистично, высокое качество, детализировано, профессиональная фотография",
            "2": "профессиональная фуд-фотография, аппетитно, красивая подача, хорошее освещение",
            "3": "художественный стиль, живопись, творческий подход",
            "4": "акварельный скетч, легкий рисунок, нежные цвета",
            "5": "минимализм, чистая композиция, простой фон",
            "0": ""
        }

    def get_pipeline(self):
        response = requests.get(self.URL + 'key/api/v1/pipelines', headers=self.AUTH_HEADERS)
        data = response.json()
        return data[0]['id']

    def generate(self, prompt, pipeline_id, images=1, width=1024, height=1024, style="0"):
        style_prompt = self.FOOD_STYLE_PROMPTS.get(style, "")
        full_prompt = f"{prompt}, {style_prompt}" if style_prompt else prompt

        params = {
            "type": "GENERATE",
            "numImages": images,
            "width": width,
            "height": height,
            "generateParams": {
                "query": full_prompt
            }
        }

        data = {
            'pipeline_id': (None, pipeline_id),
            'params': (None, json.dumps(params), 'application/json')
        }
        response = requests.post(self.URL + 'key/api/v1/pipeline/run', headers=self.AUTH_HEADERS, files=data)
        data = response.json()
        return data['uuid']

    def check_generation(self, request_id, attempts=20, delay=10):
        while attempts > 0:
            response = requests.get(self.URL + 'key/api/v1/pipeline/status/' + request_id, headers=self.AUTH_HEADERS)
            data = response.json()
            if data['status'] == 'DONE':
                return data['result']['files']
            elif data['status'] == 'FAIL':
                raise Exception("Generation failed")

            attempts -= 1
            time.sleep(delay)

        raise Exception("Timeout waiting for generation")

    def get_image_from_data(self, image_data):
        if isinstance(image_data, list):
            image_data = image_data[0]

        image_bytes = base64.b64decode(image_data)
        return Image.open(BytesIO(image_bytes))


kandinsky_api = FusionBrainAPI(KANDINSKY_URL, KANDINSKY_API_KEY, KANDINSKY_SECRET_KEY)


def get_access_token():
    auth_url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"

    credentials = f"{CLIENT_ID}:{CLIENT_SECRET}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()

    auth_headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json',
        'Authorization': f'Basic {encoded_credentials}',
        'RqUID': '6f0b1291-c7f3-43c6-bb2e-9f3efc2e4568'
    }

    auth_data = {'scope': 'GIGACHAT_API_PERS'}

    print("🔐 Получаю токен...")
    auth_response = requests.post(auth_url, headers=auth_headers, data=auth_data, verify=False)

    if auth_response.status_code != 200:
        print(f"❌ Ошибка аутентификации: {auth_response.status_code}")
        return None

    access_token = auth_response.json()['access_token']
    print("✅ Токен получен")
    return access_token


def get_gigachat_response(message):

    recipe_prompt = f"""Предоставь подробный рецепт блюда: {message}. 

Включи:
1. Список ингредиентов с количествами
2. Пошаговую инструкцию приготовления
3. Время приготовления
4. Советы по подаче

Если это не блюдо, вежливо сообщи, что ты специализируешься только на рецептах.

Форматируй ответ с использованием эмодзи и четкой структурой."""

    access_token = get_access_token()
    if not access_token:
        return "Извините, произошла ошибка при подключении к сервису рецептов."

    chat_url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

    chat_headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    chat_data = {
        "model": "GigaChat",
        "messages": [
            {
                "role": "user",
                "content": recipe_prompt
            }
        ],
        "temperature": 0.7,
        "max_tokens": 2000
    }

    chat_response = requests.post(chat_url, headers=chat_headers, json=chat_data, verify=False)

    if chat_response.status_code == 200:
        response_text = chat_response.json()['choices'][0]['message']['content']
        print(f"🤖 Ответ GigaChat получен")
        return response_text
    else:
        print(f"❌ Ошибка запроса: {chat_response.status_code}")
        return "Извините, не удалось получить рецепт. Попробуйте позже."


def generate_food_image_kandinsky(dish_name, recipe_description, style="2"):
    try:
        image_prompt = f"""
        Аппетитное блюдо: {dish_name}. 
        Профессиональная фуд-фотография, высокое качество, детализировано, 
        красивая подача, хорошее освещение, на белом фоне, фотореалистично.
        Еда выглядит свежей и вкусной.
        """

        print("🎨 Запускаю генерацию изображения через Kandinsky...")

        pipeline_id = kandinsky_api.get_pipeline()

        uuid = kandinsky_api.generate(
            prompt=image_prompt,
            pipeline_id=pipeline_id,
            style=style,
            width=1024,
            height=1024
        )

        print(f"🔄 ID генерации: {uuid}")

        files = kandinsky_api.check_generation(uuid, attempts=15, delay=10)

        if files:
            image = kandinsky_api.get_image_from_data(files[0])

            bio = BytesIO()
            bio.name = 'food_image.png'
            image.save(bio, 'PNG')
            bio.seek(0)

            print("✅ Изображение сгенерировано успешно")
            return bio

        else:
            print("❌ Не удалось сгенерировать изображение")
            return None

    except Exception as e:
        print(f"❌ Ошибка при генерации изображения: {e}")
        return None


def convert_ogg_to_wav(ogg_path, wav_path):
    try:
        audio, sr_rate = librosa.load(ogg_path, sr=16000)
        sf.write(wav_path, audio, sr_rate, format='WAV')
        return True
    except Exception as e:
        print(f"Ошибка конвертации: {e}")
        return False


def recognize_speech(audio_path):
    recognizer = sr.Recognizer()

    try:
        wav_path = audio_path.replace('.ogg', '.wav')

        if not convert_ogg_to_wav(audio_path, wav_path):
            return "Ошибка конвертации аудио"

        with sr.AudioFile(wav_path) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data, language="ru-RU")

        if os.path.exists(wav_path):
            os.unlink(wav_path)

        return text

    except sr.UnknownValueError:
        if os.path.exists(wav_path):
            os.unlink(wav_path)
        return "Не удалось распознать речь"
    except Exception as e:
        if os.path.exists(wav_path):
            os.unlink(wav_path)
        print(f"Ошибка распознавания: {e}")
        return f"Ошибка: {e}"


def clean_text_for_speech(text):
    text = re.sub(r'[^\w\s\.\,\!\?\-\:\;\(\)\"\']', '', text)

    text = re.sub(r'\.{2,}', '.', text)  # Заменяем многоточия на одну точку
    text = re.sub(r'\!{2,}', '!', text)  # Заменяем множественные восклицательные знаки
    text = re.sub(r'\?{2,}', '?', text)  # Заменяем множественные вопросительные знаки

    text = re.sub(r'[\*\#\@\$\&\+\=\[\]\<\>]', '', text)

    text = re.sub(r'<[^>]+>', '', text)  # Удаляем HTML-теги
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)  # Удаляем жирный текст **
    text = re.sub(r'\*(.*?)\*', r'\1', text)  # Удаляем курсив *
    text = re.sub(r'_(.*?)_', r'\1', text)  # Удаляем подчеркивание _

    text = re.sub(r'\s+', ' ', text).strip()

    return text


def text_to_speech(text, filename):
    try:
        cleaned_text = clean_text_for_speech(text)

        if len(cleaned_text) > 3000:
            cleaned_text = cleaned_text[:3000] + " Текст сокращен для озвучки."

        print(f"🔊 Озвучиваю текст длиной {len(cleaned_text)} символов")

        tts = gTTS(text=cleaned_text, lang='ru', slow=False)
        tts.save(filename)
        return True
    except Exception as e:
        print(f"❌ Ошибка преобразования текста в речь: {e}")
        return False


@bot.message_handler(commands=['start'])
def start_handler(message):
    welcome_text = """
🍳 Привет! Я бот-шеф! 🍲

Я помогу тебе найти рецепты вкусных блюд и покажу, как они выглядят!

Просто напиши название блюда или отправь голосовое сообщение с названием, и я:
1. 🍽️ Пришлю подробный рецепт
2. 🔊 Озвучу рецепт голосом
3. 🎨 Сгенерирую аппетитное изображение блюда!

Например:
• "рецепт борща"
• "как приготовить пасту карбонара" 
• "десерт тирамису"

⏳ Генерация изображения занимает около 1-2 минут
    """
    bot.send_message(message.chat.id, welcome_text)


@bot.message_handler(commands=['help'])
def help_handler(message):
    help_text = """
📖 Как пользоваться ботом:

1. Отправь текстовое сообщение с названием блюда
2. Или отправь голосовое сообщение с названием блюда
3. Я найду для тебя подробный рецепт, озвучу его и создам изображение блюда!

Примеры запросов:
• "рецепт пиццы маргарита"
• "как приготовить плов"
• "блины на завтрак"

⚠️ Генерация изображения занимает примерно 1 минуту
    """
    bot.send_message(message.chat.id, help_text)


@bot.message_handler(content_types=['text'])
def text_message_handler(message):
    user_message = message.text.strip()

    if not user_message:
        bot.send_message(message.chat.id, "Пожалуйста, введите название блюда!")
        return

    status_msg = bot.send_message(
        message.chat.id,
        "🔍 Ищу рецепт для вас..."
    )

    try:
        recipe = get_gigachat_response(user_message)

        if "извините" in recipe.lower() or "ошибка" in recipe.lower():
            bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=status_msg.message_id,
                text=recipe
            )
            return

        if len(recipe) > 4000:
            parts = [recipe[i:i + 4000] for i in range(0, len(recipe), 4000)]
            for i, part in enumerate(parts):
                if i == 0:
                    bot.edit_message_text(
                        chat_id=message.chat.id,
                        message_id=status_msg.message_id,
                        text=part
                    )
                else:
                    bot.send_message(message.chat.id, part)
        else:
            bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=status_msg.message_id,
                text=recipe
            )

        voice_msg = bot.send_message(
            message.chat.id,
            "🔊 Озвучиваю рецепт..."
        )

        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_audio:
            temp_filename = temp_audio.name

        if text_to_speech(recipe, temp_filename):
            with open(temp_filename, 'rb') as audio_file:
                bot.send_voice(
                    message.chat.id,
                    audio_file,
                    caption=f"🔊 Озвученный рецепт: {user_message}",
                    reply_to_message_id=message.message_id
                )
            bot.delete_message(message.chat.id, voice_msg.message_id)
        else:
            bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=voice_msg.message_id,
                text="❌ Не удалось озвучить рецепт, но текстовый вариант готов! 📝"
            )

        if os.path.exists(temp_filename):
            os.unlink(temp_filename)

        generating_msg = bot.send_message(
            message.chat.id,
            "🎨 Генерирую изображение блюда... Это займет 1-2 минуты ⏳"
        )

        image_bytes = generate_food_image_kandinsky(user_message, recipe)

        if image_bytes:
            bot.send_photo(
                message.chat.id,
                image_bytes,
                caption=f"🍽️ Вот как может выглядеть ваше блюдо(не всегда изображение показывает верный результат): {user_message}"
            )
            bot.delete_message(message.chat.id, generating_msg.message_id)
        else:
            bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=generating_msg.message_id,
                text="❌ Не удалось сгенерировать изображение блюда, но рецепт готов! 🍳"
            )

    except Exception as e:
        print(f"Ошибка обработки текстового сообщения: {e}")
        bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=status_msg.message_id,
            text="Извините, произошла ошибка при поиске рецепта. Попробуйте еще раз."
        )


@bot.message_handler(content_types=['voice'])
def voice_message_handler(message):
    voice = message.voice
    print("Обработка голосового сообщения...")

    try:
        status_msg = bot.send_message(
            message.chat.id,
            "🎤 Обрабатываю ваше голосовое сообщение..."
        )

        voice_file_info = bot.get_file(voice.file_id)
        voice_file = bot.download_file(voice_file_info.file_path)

        temp_file_path = os.path.join(VOICE_MESSAGE_DIR, f"voice_{message.message_id}.ogg")

        with open(temp_file_path, 'wb') as f:
            f.write(voice_file)

        print(f"Голосовое сообщение сохранено: {os.path.basename(temp_file_path)}")

        bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=status_msg.message_id,
            text="🔍 Распознаю речь..."
        )

        recognized_text = recognize_speech(temp_file_path)

        os.unlink(temp_file_path)

        if recognized_text.lower() in ["не удалось распознать речь",
                                       "ошибка конвертации аудио"] or recognized_text.startswith("Ошибка:"):
            bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=status_msg.message_id,
                text=f"❌ Не удалось распознать голосовое сообщение. Попробуйте отправить текстовый запрос."
            )
            return

        bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=status_msg.message_id,
            text=f"🔍 Распознано: '{recognized_text}'\n\nИщу рецепт..."
        )

        recipe = get_gigachat_response(recognized_text)

        if "извините" in recipe.lower() or "ошибка" in recipe.lower():
            bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=status_msg.message_id,
                text=recipe
            )
            return

        if len(recipe) > 4000:
            parts = [recipe[i:i + 4000] for i in range(0, len(recipe), 4000)]
            for i, part in enumerate(parts):
                if i == 0:
                    bot.edit_message_text(
                        chat_id=message.chat.id,
                        message_id=status_msg.message_id,
                        text=part
                    )
                else:
                    bot.send_message(message.chat.id, part)
        else:
            bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=status_msg.message_id,
                text=recipe
            )

        voice_msg = bot.send_message(
            message.chat.id,
            "🔊 Озвучиваю рецепт..."
        )

        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_audio:
            temp_filename = temp_audio.name

        if text_to_speech(recipe, temp_filename):
            with open(temp_filename, 'rb') as audio_file:
                bot.send_voice(
                    message.chat.id,
                    audio_file,
                    caption=f"🔊 Озвученный рецепт: {recognized_text}",
                    reply_to_message_id=message.message_id
                )
            bot.delete_message(message.chat.id, voice_msg.message_id)
        else:
            bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=voice_msg.message_id,
                text="❌ Не удалось озвучить рецепт, но текстовый вариант готов! 📝"
            )

        if os.path.exists(temp_filename):
            os.unlink(temp_filename)

        generating_msg = bot.send_message(
            message.chat.id,
            "🎨 Генерирую изображение блюда... Это займет 1-2 минуты ⏳"
        )

        image_bytes = generate_food_image_kandinsky(recognized_text, recipe)

        if image_bytes:
            bot.send_photo(
                message.chat.id,
                image_bytes,
                caption=f"🍽️ Вот как может выглядеть ваше блюдо: {recognized_text}"
            )
            bot.delete_message(message.chat.id, generating_msg.message_id)
        else:
            bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=generating_msg.message_id,
                text="❌ Не удалось сгенерировать изображение блюда, но рецепт готов! 🍳"
            )

    except Exception as e:
        print(f"Ошибка обработки голосового сообщения: {e}")
        bot.send_message(
            message.chat.id,
            "❌ Произошла ошибка при обработке голосового сообщения. Попробуйте отправить текстовый запрос."
        )


def main():
    if not os.path.exists(VOICE_MESSAGE_DIR):
        os.makedirs(VOICE_MESSAGE_DIR)
        print(f"Создана директория для временных файлов: {VOICE_MESSAGE_DIR}")

    print("Бот запущен...")
    bot.polling(none_stop=True)


if __name__ == '__main__':
    main()
