import asyncio
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from data.config import ADMINS
from keyboards.inline.buttons import Select_menu, reply_button, reply_callback, select_callback, status_callback
from keyboards.default.services_buttons import cancel_contact, services_menu
from loader import dp, bot
from states.states import ContactState


@dp.message_handler(text="Bog'lanish")
async def contact_def(message: types.Message):
    id = message.from_user.id
    await ContactState.contact.set()
    await message.answer(f"<i>Xabaringizni Kiriting</i>",reply_markup=cancel_contact)

@dp.message_handler(text="Bog'lanishni Yakunlash", state=ContactState.contact)
async def contact_def(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(f"<i>Xabaringiz uchun rahmat</i>",reply_markup=services_menu)

@dp.message_handler(state=ContactState.contact)
async def name_def(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    msg = f"user: @{message.from_user.username}\n {message.text}"
    #await message.forward(chat_id=ADMINS[0])
    contact_button = await reply_button(user_id=user_id)
    await bot.send_message(chat_id=ADMINS[0], text=msg, reply_markup=contact_button)


@dp.callback_query_handler(reply_callback.filter(action='reply_user'),user_id=ADMINS, state="*")
async def reply_msg_def(call: CallbackQuery, callback_data:dict, state:FSMContext):
    user_id = int(callback_data.get('user_id'))
    print(user_id)
    await ContactState.reply_msg.set()
    await state.update_data(
        {'user_id': user_id}
    )
    await call.message.reply(f"Javob xabarini yuboring")

@dp.message_handler(state=ContactState.reply_msg, user_id=ADMINS)
async def name_def(message: types.Message, state: FSMContext):
    msg = message.text
    data = await state.get_data()
    reply_user_id = data.get('user_id')
    await bot.send_message(chat_id=reply_user_id, text=msg)
    await message.answer('Xabar Yuborildi')
    await state.finish()

#filterdan otib ketgan xabarlar uchun
@dp.message_handler(state='*')
async def alter_def(message: types.Message):
    await message.reply('Iltimos Botdan To\'gri Foydalaning')


"""
#bu funksiyadan vos kechilgan
@dp.callback_query_handler(select_callback.filter(name='go_head'), state=ContactState.contact)
@dp.callback_query_handler(select_callback.filter(name='goback'), state=ContactState.contact)
async def cancel_def(call: CallbackQuery, state:FSMContext):
    await call.message.answer("Bog'lanish Bekor Qilindi",reply_markup=services_menu)
    await state.finish()
"""