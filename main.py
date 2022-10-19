from aiogram import Bot, Dispatcher, executor, types
import requests

from ai import get_intent, get_response
from config import API_TOKEN, KEY_SPEECHKIT

bot = Bot(API_TOKEN)
dp = Dispatcher(bot)

STT = "https://stt.api.cloud.yandex.net/speech/v1/stt:recognize";
TTS = "https://tts.api.cloud.yandex.net/speech/v1/tts:synthesize";


@dp.message_handler(content_types=[types.ContentType.VOICE])
async def any_text_message(message: types.Message):
    voice = await message.voice.get_file()
    file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(API_TOKEN, voice.file_path)).content
    res_stt = requests.post(
        STT,
        data=file,
        headers={"Authorization": "Api-Key " + KEY_SPEECHKIT}
    )
    intent = get_intent(res_stt.json()["result"])
    res_tts = requests.post(
        TTS,
        data={
            "voice": "zahar", 
            "emotion": "good", 
            "lang": "ru-RU", 
            "speed": "1.0",
            "format": "oggopus",
            "text": get_response(intent)
        },
        stream=True,
        headers={"Authorization": "Api-Key " + KEY_SPEECHKIT}
    )

    with open("voice.ogg", "wb") as f:
        for chunk in res_tts.iter_content(chunk_size=None):
           f.write(chunk)

    await message.answer_voice(voice=open("voice.ogg", "rb"))

if __name__ == '__main__':
    executor.start_polling(dp)

