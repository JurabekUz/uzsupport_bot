import asyncio
import sqlite3

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from data.config import ADMINS
from keyboards.inline.buttons import Select_menu, order_buttons, status_callback
from loader import dp, db, bot
from states.states import ContactState, OrderState


@dp.message_handler(text="Buyurtma Berish", state='*')
async def user_data_def(message: types.Message):
    id = message.from_user.id
    if db.select_user(id=id):
        await OrderState.order.set()
        await message.answer("Buyurtmangiz haqida ma'lumot bitta xabarda (matn ko'rinishida) yuboring")
    else:
        await message.answer("Iltimos Oldin Ro'yxatdan O'ting")


@dp.message_handler(state=OrderState.order)
async def name_def(message: types.Message, state: FSMContext):
    id = message.from_user.id
    print(type(id))
    msg = message.text
    if msg.isalpha:
        try:
            db.add_order(user_id=id,body=msg)
            current_order = db.select_last_order(user_id=id)
            user = db.select_user(id=id)
            print(current_order)
            print(current_order[1])
            manage_button = await order_buttons(order_id=current_order[0],user_id=id)
            order_msg = f" Ism: {user[1]}\n Telefon Raqam: {user[2]}\n Email: {user[3]}\n Buyurtma Holati: Pending\n{msg}"
            await bot.send_message(chat_id=ADMINS[0],text=order_msg, reply_markup=manage_button)
            await state.finish()
            await message.answer("Buyurtma Yuborildi")
        except sqlite3.IntegrityError as err:
            await bot.send_message(chat_id=ADMINS[0], text=err)
    else:
        await message.answer("ILTIMOS MATN YUBORING!!!")
        await state.finish()

#javob yozish tugamsi uchun handler
@dp.callback_query_handler(status_callback.filter(status='reply'),user_id=ADMINS, state="*")
async def reply_order_msg_def(call: CallbackQuery, callback_data: dict, state: FSMContext):
    user_id = int(callback_data.get('user_id'))
    await OrderState.order_msg.set()
    await state.update_data(
        {'user_id': user_id} )
    await call.message.reply(f"Javob xabarini yuboring")

#javob yozish tugamsi uchun handler
@dp.message_handler(state=OrderState.order_msg, user_id=ADMINS)
async def name_def(message: types.Message, state: FSMContext):
    msg = message.text
    data = await state.get_data()
    reply_user_id = data.get('user_id')
    await bot.send_message(chat_id=reply_user_id, text=msg)
    await message.answer('Xabar Yuborildi')
    await state.finish()

@dp.callback_query_handler(status_callback.filter(),user_id=ADMINS, state="*")
async def change_status(call: CallbackQuery, callback_data:dict, state:FSMContext):
    status = callback_data.get('status')
    order_id = int(callback_data.get('order_id'))
    user_id = int(callback_data.get('user_id'))
    order = db.select_orders(id=order_id) #list qaytadi 1 ta element bilan
    # current_order = order[0]
    user = db.select_user(id=user_id)
    try:
        db.update_order_status(status=status, id=order_id)
        manage_button = await order_buttons(order_id=order_id, user_id=user_id)
        order_msg = f"Ism: {user[1]}\nTelefon Raqam: {user[2]}\nEmail: {user[3]}\nBuyurtma Holati: {status}\n {order[0][2]}"
        await call.message.edit_text(text=order_msg, reply_markup=manage_button)
        await call.answer(text='Status Yangilandi')
    except:
        await call.message.reply(text='Statusni Yangilashda Xatolik')


@dp.message_handler(text="/allusers", user_id=ADMINS)
async def get_all_users(message: types.Message):
    users = db.select_all_users()
    print(users[0][0])
    await message.answer(users)

@dp.message_handler(text="/reklama", user_id=ADMINS)
async def send_ad_to_all(message: types.Message):
    users = db.select_all_users()
    for user in users:
        user_id = user[0]
        await bot.send_message(chat_id=user_id, text="@SariqDev kanaliga obuna bo'ling!")
        await asyncio.sleep(0.05)

@dp.message_handler(text="/cleandb", user_id=ADMINS)
async def get_all_users(message: types.Message):
    db.delete_users()
    await message.answer("Baza tozalandi!")