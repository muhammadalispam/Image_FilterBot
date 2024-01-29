import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext

from btns import *
from states import *
from utils import *
from database import *
import os

BOT_TOKEN = '6540031921:AAGPSCYkhsvo173yxgp9iFRFr8sgpQhF2Rs'
ADMINS = [127158713]

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN, parse_mode='html')
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


async def command_menu(dp: Dispatcher):
    await create_tables()
    await dp.bot.set_my_commands(
        [
            types.BotCommand('start', 'start'),
            types.BotCommand('stats', 'users\' statistics'),
            types.BotCommand('id', 'id'),
            types.BotCommand('stats', 'statisticks'),
        ]
    )


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    btn = await start_btn()
    await add_user(
        user_id=message.from_user.id,
        username=message.from_user.username
    )
    await message.answer(f"Welcome @{message.from_user.username}", reply_markup=btn)


@dp.message_handler(text="Filter Image🖼")
async def effect_to_image_handler(message: types.Message):
    btn = await filters_btn(filters)
    await message.answer("Choose a necessary filter: ", reply_markup=btn)


@dp.message_handler(text='⬅️')
async def back_handler(message: types.Message):
    await effect_to_image_handler(message)


@dp.message_handler(text='⬅️⬅️')
async def back_handler(message: types.Message):
    await start_command(message)


@dp.message_handler(commands=['id'])
async def get_user_stats_handler(message: types.Message):
    await message.answer(f"<code>{message.from_user.id}</code>")


@dp.message_handler(commands=['stats'])
async def get_user_stats_handler(message: types.Message):
    if message.from_user.id in ADMINS:
        count = await get_all_users()
        await message.answer(f"Bot users number: {count}")


@dp.message_handler(state=UserStates.get_image, content_types=['photo', 'text'])
async def get_image_state(message: types.Message, state: FSMContext):
    content = message.content_type
    if content == "text":
        await start_command(message)
    else:
        filename = f"rasm_{message.from_user.id}.jpg"
        await message.photo[-1].download(destination_file=filename)
        await message.answer(f"Rasimingiz qabul qilindi! 😊")
        data = await state.get_data()

        await filter_user_image(filename, filter=data['filter'])
        await message.answer_photo(
            photo=types.InputFile(filename),
            caption=f"Rasmingiz filtratsiya qilindi! 😊😊"
        )
        os.remove(filename)
        await start_command(message)
    await state.finish()


@dp.message_handler(content_types=['text'])
async def selected_filter_handler(message: types.Message, state: FSMContext):
    text = message.text

    if text in filters:
        await state.update_data(filter=text)
        btn = await cancel_btn()
        await message.answer("Send an image: ", reply_markup=btn)
        await UserStates.get_image.set()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=command_menu)
    # print("End")
