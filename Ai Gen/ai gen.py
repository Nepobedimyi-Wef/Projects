import json
import time
import base64
import logging
from io import BytesIO
from PIL import Image
import requests
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

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
API_KEY = ''
SECRET_KEY = ''

api = FusionBrainAPI(API_URL, API_KEY, SECRET_KEY)

user_states = {}


def get_main_keyboard():
    keyboard = [
        [KeyboardButton("🎨 Сгенерировать изображение")],
        [KeyboardButton("❓ Помощь"), KeyboardButton("❌ Отмена")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, input_field_placeholder="Выберите действие...")


def get_styles_keyboard():
    keyboard = [
        [KeyboardButton("📸 Фото"), KeyboardButton("🎨 Аниме")],
        [KeyboardButton("🖼️ Масляная"), KeyboardButton("🌊 Акварель")],
        [KeyboardButton("🤖 Киберпанк"), KeyboardButton("🧙‍♂️ Фэнтези")],
        [KeyboardButton("⚫ Минимализм"), KeyboardButton("🌅 Импрессионизм")],
        [KeyboardButton("✏️ Эскиз"), KeyboardButton("🎭 Сюрреализм")],
        [KeyboardButton("🚫 Без стиля"), KeyboardButton("❌ Отмена")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, input_field_placeholder="Выберите стиль...")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_states[user_id] = {'step': 'waiting_prompt'}

    welcome_text = """
   Добро пожаловать в AI Image Generator!

Я могу создавать изображения по вашему описанию с помощью нейросети.

Как использовать:
1. Нажмите кнопку "🎨 Сгенерировать изображение"
2. Отправьте описание изображения
3. Выберите стиль из предложенных
4. Ждите результат (примерно 1 минуту)

Примеры запросов:
• Кот на фоне луны
• Закат в лесу
• Город будущего 

Начните с кнопки ниже! 🖼️
    """

    await update.message.reply_text(welcome_text, reply_markup=get_main_keyboard())


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """
Доступные команды:

🎨 Сгенерировать изображение - создать новое изображение
❓ Помощь - показать подсказски 
❌ Отмена - отменить текущую операцию

Процесс работы:
1. Нажмите "🎨 Сгенерировать изображение"
2. Отправьте описание изображения
3. Выберите стиль из предложенных
4. Ждите результат генерации

⏳ Генерация занимает примерно 1 минуту
    """
    await update.message.reply_text(help_text, reply_markup=get_main_keyboard())


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id in user_states:
        user_states[user_id] = {'step': 'waiting_prompt'}
    await update.message.reply_text("✅ Текущая операция отменена. Можете начать заново.",
                                    reply_markup=get_main_keyboard())


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text.strip()

    if user_id not in user_states:
        user_states[user_id] = {'step': 'waiting_prompt'}

    current_state = user_states[user_id]

    if text == "🎨 Сгенерировать изображение":
        current_state['step'] = 'waiting_prompt'
        await update.message.reply_text("💬 Отправьте описание изображения:\n\nПример: Кот на фоне луны")

    elif text == "❓ Помощь":
        await help_command(update, context)
        return

    elif text == "❌ Отмена":
        await cancel(update, context)
        return

    elif current_state['step'] == 'waiting_prompt':
        current_state['prompt'] = text
        current_state['step'] = 'waiting_style'

        styles_text = "🎨 **Выберите стиль для генерации:**"
        await update.message.reply_text(styles_text, reply_markup=get_styles_keyboard())

    elif current_state['step'] == 'waiting_style':
        style_mapping = {
            "📸 Фото": "1",
            "🎨 Аниме": "2",
            "🖼️ Масляная": "3",
            "🌊 Акварель": "4",
            "🤖 Киберпанк": "5",
            "🧙‍♂️ Фэнтези": "6",
            "⚫ Минимализм": "7",
            "🌅 Импрессионизм": "8",
            "✏️ Эскиз": "9",
            "🎭 Сюрреализм": "10",
            "🚫 Без стиля": "0"
        }

        if text in style_mapping:
            current_state['style'] = style_mapping[text]
            current_state['step'] = 'generating'

            style_name = text
            await update.message.reply_text(f"⏳ Запускаю генерацию...\n\nСтиль: {style_name}\n\nЭто займет примерно 1 минуту.",
                                            reply_markup=None)

            try:
                pipeline_id = api.get_pipeline()

                uuid = api.generate(
                    prompt=current_state['prompt'],
                    pipeline_id=pipeline_id,
                    style=current_state['style']
                )

                message = await update.message.reply_text("🔄 Генерация началась...")

                files = api.check_generation(uuid)

                if files:
                    image = api.get_image_from_data(files[0])

                    bio = BytesIO()
                    bio.name = 'image.png'
                    image.save(bio, 'PNG')
                    bio.seek(0)

                    await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=message.message_id)

                    caption = f"✅ Ваше изображение готово!\n\n📝 Запрос: {current_state['prompt']}\n🎨 Стиль: {style_name}"
                    await update.message.reply_photo(photo=bio, caption=caption, reply_markup=get_main_keyboard())

                    user_states[user_id] = {'step': 'waiting_prompt'}

                else:
                    await update.message.reply_text("❌ Не удалось сгенерировать изображение. Попробуйте еще раз.",
                                                    reply_markup=get_main_keyboard())
                    user_states[user_id] = {'step': 'waiting_prompt'}

            except Exception as e:
                await update.message.reply_text(f"❌ Ошибка при генерации: {str(e)}", reply_markup=get_main_keyboard())
                user_states[user_id] = {'step': 'waiting_prompt'}

        elif text == "❌ Отмена":
            await cancel(update, context)
        else:
            await update.message.reply_text("❌ Пожалуйста, выберите стиль из предложенных кнопок:")


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.error(f"Ошибка: {context.error}")
    if update and update.effective_message:
        await update.effective_message.reply_text("❌ Произошла ошибка. Попробуйте еще раз.",
                                                  reply_markup=get_main_keyboard())


def main():
    BOT_TOKEN = ""

    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("cancel", cancel))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_error_handler(error_handler)
    application.run_polling()


if __name__ == '__main__':
    main()
