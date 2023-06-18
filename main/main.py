import os
import requests
from io import BytesIO

from pydub import AudioSegment
import speech_recognition as sr
from dotenv import load_dotenv
from telegram.ext import Updater, MessageHandler, Filters
from telegram import Bot
import telegram


load_dotenv()
tg_token = os.getenv('TOKEN')

def translate_voice(update, context):
    try:
        # Получаем аудиофайл из голосового сообщения
        audio_file = update.message.voice.get_file()
        audio_data = requests.get(audio_file.file_path).content

        # Конвертируем аудиофайл в формат WAV
        audio = AudioSegment.from_file(BytesIO(audio_data))
        audio.export('voice.wav', format='wav')

        # Используем библиотеку SpeechRecognition
        recognizer = sr.Recognizer()

        with sr.AudioFile('voice.wav') as source:
            audio_text = recognizer.record(source)
            text = recognizer.recognize_google(audio_text, language='ru')  # Выбрать требуемый язык

        # Отправляем переведенный текст в ответном сообщении
        update.message.reply_text(text)

    except Exception as e:
        # Выводим сообщение с ошибкой
        print(f'An error occurred: {e}')

        main()


def main():
    # создаем объект Bot с передачей токена
    bot = Bot(token=tg_token, request=telegram.utils.request.Request(con_pool_size=8))

    # создаем объект Updater, передавая объект Bot
    updater = Updater(bot=bot)

    # регистрируем обработчик голосовых сообщений
    updater.dispatcher.add_handler(MessageHandler(Filters.voice, translate_voice))

    # запускаем бота
    updater.start_polling()

    # остановка бота при нажатии Ctrl+C
    updater.idle()


if __name__ == '__main__':
    main()
