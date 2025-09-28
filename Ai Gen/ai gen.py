import json
import time
import base64
import logging
from io import BytesIO
from PIL import Image
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


class FusionBrainAPI:
    def __init__(self, url, api_key, secret_key):
        self.URL = url
        self.AUTH_HEADERS = {
            'X-Key': f'Key {api_key}',
            'X-Secret': f'Secret {secret_key}',
        }

        self.STYLES = {
            "1": "📸 Фотореалистичный",
            "2": "🎨 Аниме",
            "3": "🖼️ Масляная живопись",
            "4": "🌊 Акварель",
            "5": "🤖 Киберпанк",
            "6": "🧙‍♂️ Фэнтези",
            "7": "⚫ Минимализм",
            "8": "🌅 Импрессионизм",
            "9": "✏️ Эскиз",
            "10": "🎭 Сюрреализм",
            "0": "🚫 Без стиля"
        }

        self.STYLE_PROMPTS = {
            "1": "фотореалистично, высокое качество, детализировано, профессиональная фотография",
            "2": "в стиле аниме, японская анимация, яркие цвета",
            "3": "масляная живопись, художественный стиль, мазки кисти",
            "4": "акварельный рисунок, водяные краски, легкие размытия",
            "5": "киберпанк, неон, футуристично, технологично",
            "6": "фэнтези, волшебство, магия, эпический стиль",
            "7": "минимализм, простые формы, чистые линии, лаконично",
            "8": "импрессионизм, световые эффекты, мягкие контуры",
            "9": "эскиз, набросок карандашом, черно-белый рисунок",
            "10": "сюрреализм, фантастично, нереально, сновидение",
            "0": ""
        }

    def get_pipeline(self):
        response = requests.get(self.URL + 'key/api/v1/pipelines', headers=self.AUTH_HEADERS)
        data = response.json()
        return data[0]['id']

    def generate(self, prompt, pipeline_id, images=1, width=1024, height=1024, style="0"):
        style_prompt = self.STYLE_PROMPTS.get(style, "")
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


API_URL = 'https://api-key.fusionbrain.ai/'
API_KEY = '497FC239DD6DE62B5CA88473EB340B4A'
SECRET_KEY = 'A35BEA9989D8922F6ED9B7C68DF05A3E'

api = FusionBrainAPI(API_URL, API_KEY, SECRET_KEY)

# Состояния пользователей
user_states = {}


# Команда старт
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_states[user_id] = {'step': 'waiting_prompt'}

    welcome_text = """
🎨 Добро пожаловать в AI Image Generator!

Я могу создавать изображения по вашему описанию с помощью нейросети.

Как использовать:
1. Отправьте мне описание изображения
2. Выберите стиль из предложенных
3. Ждите результат (примерно 1 минуту)

Примеры запросов:
• Кот на фоне луны
• Закат в лесу
• Город будущего 

Просто напишите, что хотите увидеть! 🖼️
    """

    await update.message.reply_text(welcome_text)


# Команда помощи
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """
**Доступные команды:**
/start - начать работу
/help - показать эту справку
/cancel - отменить текущую генерацию

**Процесс работы:**
1. Отправьте описание изображения
2. Выберите стиль (от 0 до 10)
3. Ждите результат генерации

Генерация занимает 1-3 минуты ⏳
    """
    await update.message.reply_text(help_text)


# Команда отмены
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id in user_states:
        user_states[user_id] = {'step': 'waiting_prompt'}
    await update.message.reply_text("✅ Текущая операция отменена. Можете начать заново.")


# Обработка текстовых сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text.strip()

    # Если пользователя нет в состояниях, добавляем его
    if user_id not in user_states:
        user_states[user_id] = {'step': 'waiting_prompt'}

    current_state = user_states[user_id]

    if current_state['step'] == 'waiting_prompt':
        # Сохраняем промпт и просим выбрать стиль
        current_state['prompt'] = text
        current_state['step'] = 'waiting_style'

        styles_text = "🎨 **Выберите стиль для генерации:**\n\n"
        for key, name in api.STYLES.items():
            styles_text += f"{key}. {name}\n"

        styles_text += "\nОтправьте номер стиля (0-10):"

        await update.message.reply_text(styles_text)

    elif current_state['step'] == 'waiting_style':
        # Обрабатываем выбор стиля
        if text in api.STYLES:
            current_state['style'] = text
            current_state['step'] = 'generating'

            await update.message.reply_text("⏳ Запускаю генерацию... Это займет примерно 1 минуту.")

            try:
                # Получаем pipeline ID
                pipeline_id = api.get_pipeline()

                # Запускаем генерацию
                uuid = api.generate(
                    prompt=current_state['prompt'],
                    pipeline_id=pipeline_id,
                    style=current_state['style']
                )

                # Ждем завершения с периодическими обновлениями
                message = await update.message.reply_text("🔄 Генерация началась...")

                files = api.check_generation(uuid)

                if files:
                    # Конвертируем и отправляем изображение
                    image = api.get_image_from_data(files[0])

                    bio = BytesIO()
                    bio.name = 'image.png'
                    image.save(bio, 'PNG')
                    bio.seek(0)

                    await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=message.message_id)
                    await update.message.reply_photo(photo=bio, caption="✅ Ваше изображение готово!")

                    # Сбрасываем состояние
                    user_states[user_id] = {'step': 'waiting_prompt'}
                    await update.message.reply_text("Можете отправить новый запрос! ✨")

                else:
                    await update.message.reply_text("❌ Не удалось сгенерировать изображение. Попробуйте еще раз.")
                    user_states[user_id] = {'step': 'waiting_prompt'}

            except Exception as e:
                await update.message.reply_text(f"❌ Ошибка при генерации: {str(e)}")
                user_states[user_id] = {'step': 'waiting_prompt'}

        else:
            await update.message.reply_text("❌ Неверный номер стиля. Отправьте число от 0 до 10:")


# Обработка ошибок
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.error(f"Ошибка: {context.error}")
    if update and update.effective_message:
        await update.effective_message.reply_text("❌ Произошла ошибка. Попробуйте еще раз.")


def main():
    BOT_TOKEN = "8150733026:AAHuJr3-AW1BH-wQ8p3xiEjIykfBRWJI5fM"

    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("cancel", cancel))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.add_error_handler(error_handler)

    application.run_polling()


if __name__ == '__main__':
    main()
