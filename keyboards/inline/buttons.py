from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData


# button callbacks
select_callback = CallbackData('select', "name")
status_callback = CallbackData("create", "status", "order_id", "user_id")
update_callback = CallbackData('update', 'field')
reply_callback = CallbackData("reply", "action", "user_id")

# Admin boshqaruv tugmalari
async def order_buttons(order_id, user_id):
    status_menu = InlineKeyboardMarkup(
        inline_keyboard=[
            [ InlineKeyboardButton(text="Yangi", callback_data=status_callback.new(status="pending", order_id=order_id, user_id=user_id)) ,
             InlineKeyboardButton(text="Jarayonda", callback_data=status_callback.new(status="inprogress", order_id=order_id, user_id=user_id)) ],
             [InlineKeyboardButton(text="Bajarildi", callback_data=status_callback.new(status="done", order_id=order_id, user_id=user_id)) ,
             InlineKeyboardButton(text="Bekor Qilish", callback_data=status_callback.new(status="canceled", order_id=order_id, user_id=user_id)) ],
            [ InlineKeyboardButton(text="Javob Yozish", callback_data=status_callback.new(status="reply", order_id=order_id, user_id=user_id)) ],
        ],
    )
    return status_menu

# reply to user
async def reply_button(user_id):
    reply_menu = InlineKeyboardMarkup(
        inline_keyboard=[
            [ InlineKeyboardButton(text="Javob Yozish", callback_data=reply_callback.new(action="reply_user",user_id=user_id)) ],
            #[ InlineKeyboardButton(text="Xabarni O'chirish", callback_data=reply_callback.new(action="del_msg",user_id=user_id)) ],
        ],
    )
    return reply_menu

# select menu si (orqaga va boshmenu tugmalari)
Select_menu = InlineKeyboardMarkup(row_width=2)
head_menu = InlineKeyboardButton(text="Bosh Menu", callback_data=select_callback.new(name="go_head"))
Select_menu.insert(head_menu)

go_back = InlineKeyboardButton(text="Orqaga", callback_data=select_callback.new(name="goback"))
Select_menu.insert(go_back)

Update_menu = InlineKeyboardMarkup(row_width=1)
update_button = InlineKeyboardButton(text="Ma'lumotlarni Yangilash", callback_data=update_callback.new(field="all"))
Update_menu.insert(update_button)