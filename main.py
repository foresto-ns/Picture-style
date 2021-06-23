import os
import sys
from aiogram import Bot, types
from aiogram.types import InputFile
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher

from model import run_style_transfer, show_results


#bot = Bot(token=getToken())
bot = Bot(token="1832589895:AAEdKs6qGYjNq8wRiSBtERrGIwpr-9sN9Vw")
dp = Dispatcher(bot)
dir_path = 'C:/Users/Admin/Desktop/Aviahack/PictureStyleBot/pictures/'

async def sendHello(message):
    reply = f'Привет!\nПришли в одном сообщении 2 изображения.\nПервое - которое ты хочешь стилизовать.\nВторое - стилизация'''
    await message.reply(reply)
    print(reply.replace("\n", " "))

@dp.message_handler(content_types=['photo'])
async def handle_docs_photo(message):
    client_id = message["from"]["id"]

    message.photo[0].download(f'{dir_path}{client_id}original.jpg')
    message.photo[1].download(f'{dir_path}{client_id}style.jpg')

    best_poc, best_loss = run_style_transfer(f'{dir_path}{client_id}original.jpg',
                                             f'{dir_path}{client_id}style.jpg')
    await show_results(best_poc, f'{dir_path}{client_id}original.jpg',
                       f'{dir_path}{client_id}style.jpg')

    await bot.send_document(chat_id=client_id, document=best_poc)


@dp.message_handler(commands=["start"])
async def botStart(message):
    print(message)
    await sendHello(message)


# @dp.message_handler()
# async def botMessageReciever(message):
#     print(message)
#     if message["text"] in ['income', 'outcome', 'unread']:
#         r = requests.get(f"{url}/{message['text']}?user_id=2")
#         if len(r.json()['data']) != 0:
#             await message.reply(' '.join(str(x) for x in r.json()['data']))
#         else:
#             await message.reply('Сообщений нет')
#
#     else:
#         botAnswer = f'Привет, {message["from"]["first_name"]}!\nХочешь пообщаться?'
#         await message.reply(botAnswer)
#         logger.botMessage(botAnswer)


if __name__ == '__main__':
    print("Polling started")
    executor.start_polling(dp)
    print("Polling over")
