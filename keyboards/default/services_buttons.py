from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

services_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Buyurtma Berish'),
            KeyboardButton(text='Bog\'lanish'),
        ],
        [
            KeyboardButton(text="Mening Ma'lumotlarim"),
            KeyboardButton(text='Mening Buyurtmalarim'),
        ],
    ],
    resize_keyboard=True
)

Numboard = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text="Telefon Raqamni Ulashish", request_contact=True)
        ]
    ]
)

cancel_contact = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text="Bog'lanishni Yakunlash")
        ]
    ]
    )