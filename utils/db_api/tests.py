from utils.db_api.sqlite import Database

def test():
    db = Database(path_to_db='test.db')
    #db.create_table_users()
    #db.create_table_order()

    #db.add_user(1, "One", "email","+223654")

    # db.add_user(2, "olim", "olim@gmail.com", "+6658444")
    # db.add_user(3, 1)
    # db.add_user(4, 1, 1)
    # db.add_user(5, "John")
    """
    ss = db.select_orders(user_id = 5)
    if ss:
        print(ss)
    else:
        print('xatolik')
    """

    order = db.add_order(5,"llllllll")
    print(order)

    ss = db.select_orders(id=3)
    print("order:",ss)

    # users = db.select_all_users()
    # print(f"Barcha fodyalanuvchilar: {users}")

    # user = db.select_user(id=1)
    # print(f"Bitta foydalanuvchini ko'rish: {user}")

    # user_22 = db.select_user(id=6)
    # print(f"Bitta foydalanuvchini ko'rish: {user_22}")

test()
