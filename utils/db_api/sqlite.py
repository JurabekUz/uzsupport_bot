import sqlite3

class Database:
    def __init__(self, path_to_db="main.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
        connection = self.connection
        connection.set_trace_callback(logger)
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()
        connection.close()
        return data

    def create_table_users(self):
        sql = """
        CREATE TABLE Users (
            id int NOT NULL,
            full_name varchar(100) NOT NULL,
            phone varchar(13),
            email varchar(100),
            PRIMARY KEY (id)
            );
"""
        self.execute(sql, commit=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ?" for item in parameters
        ])
        return sql, tuple(parameters.values())

    def add_user(self, id: int, full_name: str, phone: str, email: str):
        # SQL_EXAMPLE = "INSERT INTO Users(id, full_ame, email, phone) VALUES(1, 'John', 'John@gmail.com', '+11100000')"

        sql = """
        INSERT INTO Users(id, full_name, phone, email) VALUES(?, ?, ?, ?)
        """
        self.execute(sql, parameters=(id, full_name, phone, email), commit=True)

    def select_all_users(self):
        sql = """
        SELECT * FROM Users
        """
        return self.execute(sql, fetchall=True)

    def select_user(self, **kwargs):
        # SQL_EXAMPLE = "SELECT * FROM Users where id=1 AND full_name='John'"
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, fetchone=True)

    def count_users(self):
        return self.execute("SELECT COUNT(*) FROM Users;", fetchone=True)

    def update_user_data(self, full_name, phone, email, id):

        sql = f"""
        UPDATE Users SET full_name=? , phone=? , email=? WHERE id=?
        """
        return self.execute(sql, parameters=(full_name, phone, email, id), commit=True)

    def update_user_email(self, email, id):
        # SQL_EXAMPLE = "UPDATE Users SET email=mail@gmail.com WHERE id=12345"

        sql = f"""
        UPDATE Users SET email=? WHERE id=?
        """
        return self.execute(sql, parameters=(email, id), commit=True)

    def update_user_phone(self, phone, id):
        # SQL_EXAMPLE = "UPDATE Users SET phone='+11103212' WHERE id=12345"

        sql = f"""
        UPDATE Users SET phone=? WHERE id=?
        """
        return self.execute(sql, parameters=(phone, id), commit=True)

    def update_user_name(self, full_name, id):
        # SQL_EXAMPLE = "UPDATE Users SET ful_name=Alex WHERE id=12345"

        sql = f"""
        UPDATE Users SET full_name=? WHERE id=?
        """
        return self.execute(sql, parameters=(full_name, id), commit=True)

    def delete_users(self):
        self.execute("DELETE FROM Users WHERE TRUE", commit=True)

    #support table
    #status = "pending" | "inprogress" | "canceled" | "done"
    def create_table_order(self):
        sql = """
        CREATE TABLE Orders(
            id INTEGER PRIMARY KEY ,
            user_id int NOT NULL,
            body varchar(500) NOT NULL,
            status varchar(10) NOT NULL 
            );
        """
        self.execute(sql, commit=True)

    def add_order(self, user_id: int, body: str, status: str = "pending"):
        # SQL_EXAMPLE = "INSERT INTO Orders(user, body) VALUES(1, 'create a support bot')"

        sql = """
        INSERT INTO Orders(user_id, body, status) VALUES(?, ?, ?)
        """
        self.execute(sql, parameters=(user_id, body, status), commit=True)

    def user_all_order(self, user_id):
        sql = """
        SELECT * FROM Orders where user_id=?
        """
        return self.execute(sql, parameters=(user_id,), fetchall=True)

    def select_orders(self, **kwargs):
        # SQL_EXAMPLE = "SELECT * FROM Order where id=1;
        sql = "SELECT * FROM Orders WHERE "
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, fetchall=True)

    def select_last_order(self,user_id):
        sql = """ SELECT *
                  FROM Orders
                  where
                      user_id=?
                 ORDER by id DESC
                 LIMIT 1
            """
        return self.execute(sql, parameters=(user_id,), fetchone=True)

    def update_order_status(self, status: str, id):
        # SQL_EXAMPLE = "UPDATE Orders SET status='done' WHERE id=12345"

        sql = f"""
        UPDATE Orders SET status=? WHERE id=?
        """
        return self.execute(sql, parameters=(status, id), commit=True)

    def delete_order(self, id):
        self.execute("DELETE FROM Orders WHERE id=?",parameters=(id,), commit=True)



def logger(statement):
    print(f"""
_____________________________________________________        
Executing: 
{statement}
_____________________________________________________
""")
