import sqlite3
from aiogram import types
from aiogram.types import CallbackQuery

from states.states import RegisterState
from keyboards.inline.buttons import Update_menu, update_callback

from data.config import ADMINS
from loader import dp, db, bot

@dp.message_handler(text="Mening Ma'lumotlarim", state='*')
async def user_data_def(message: types.Message):
    id = message.from_user.id
    try:
        user = db.select_user(id=id)
        await message.answer(f"<i>Sizning ma'lumotlaringiz</i>\n"
                             f"<b>Ism: </b>{user[1]}\n<b>Telefon Raqam: </b>{user[2]}\n<b>Email: </b>{user[3]}",
                             reply_markup=Update_menu)
    except sqlite3.IntegrityError as err:
        await bot.send_message(chat_id=ADMINS[0], text=err)


@dp.callback_query_handler(update_callback.filter(field='all'), state='*')
async def update_data_def(call: CallbackQuery):
    await call.message.answer("Ismingizni Kiriting")
    await RegisterState.name.set()
    await  call.message.edit_reply_markup()


@dp.message_handler(text="Mening Buyurtmalarim", state='*')
async def user_orders_list_def(message: types.Message):
    user_id = message.from_user.id
    try:
        response = "Sizning Buyurtmalaringiz\n\n"
        orders = db.select_orders(user_id=user_id)
        if orders:
            for index, order in enumerate(orders, start=1):
                response += f"{index}. Holati:{order[3]}\n Buyurtma Matni:{order[2]}\n\n"
            await message.answer(response)
        else:
            await message.answer('Afsuski siz hozirgacha buyurtmalar bermagansiz')
    except sqlite3.IntegrityError as err:
        await bot.send_message(chat_id=ADMINS[0], text=err)

