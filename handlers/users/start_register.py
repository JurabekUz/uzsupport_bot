import sqlite3
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart

from states.states import RegisterState
from keyboards.default.services_buttons import Numboard, services_menu

from data.config import ADMINS
from loader import dp, db, bot

@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    user = db.select_user(id=message.from_user.id)
    if user:
        print('user mavjud')
        await message.answer('Salom Botga Xush Kelibsiz',reply_markup=services_menu)
    else:
        await message.answer("<b>Xush kelibsiz!</b>\nIltimos Ismingizizni Kiriting")
        await RegisterState.name.set()

@dp.message_handler(state=RegisterState.name)
async def name_def(message: types.Message, state: FSMContext):
    name = message.text
    if name.isalpha():
        await state.update_data(
            {'full_name': name }
        )
        await message.answer('Telefon Raqam Kiriting', reply_markup=Numboard)
        await RegisterState.next()
    else:
        await message.reply('Iltimos Ism kiriting!')

@dp.message_handler(state=RegisterState.phone,content_types='contact')
async def answer_phnum(message: types.Message, state: FSMContext):
    contact=message.contact
    await state.update_data({
        "phone": contact['phone_number']})
    await message.answer("Emailingizni Kiriting")
    await RegisterState.next()

@dp.message_handler(state=RegisterState.phone)
async def phone_def(message: types.Message, state: FSMContext):
    phone = message.text
    await state.update_data(
        {'phone': phone }
    )
    await message.answer('Emailingizni Kiriting')
    await RegisterState.next()

@dp.message_handler(state=RegisterState.email)
async def email_def(message: types.Message, state: FSMContext):
    email = message.text
    print(email)
    data = await state.get_data()
    full_name = data.get('full_name')  # listda saqlangan vasollarning qiymatlari
    phone = data.get('phone')
    user_id = message.from_user.id

    if db.select_user(id=user_id):
        print('update user data')
        db.update_user_data(
            id=user_id,
            full_name=full_name,
            phone=phone,
            email=email
        )
    else:
        try:
            #add new user
            db.add_user(
                id=user_id,
                full_name=full_name,
                phone=phone,
                email=email
            )
        except sqlite3.IntegrityError as err:
            await bot.send_message(chat_id=ADMINS[0], text=err)

    await message.answer(f"<i>Sizning ma'lumotlaringiz</i>\n"
        f"<b>Ism: </b>{full_name}\n<b>Telefon Raqam: </b>{phone}\n<b>Email: </b>{email}",
                         reply_markup=services_menu)
    await state.finish()

    # Adminga xabar beramiz
    count = db.count_users()[0]
    msg = f"{full_name} bazaga qo'shildi.\nBazada {count} ta foydalanuvchi bor."
    await bot.send_message(chat_id=ADMINS[0], text=msg)

