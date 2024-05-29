from pymysql import connect
from pymysql.cursors import DictCursor

database = connect(
    database="weather_bot",
    user="root",
    password= "12345678",
    host= "localhost",
    port= 3306,
    cursorclass= DictCursor
)

cursor = database.cursor()


def get_user(telegram_id: int) -> dict:
    """
    Returns user object from users table
    """
    cursor.execute(
        """
            SELECT * FROM users 
            WHERE telegram_id = %s
        """, (telegram_id,)
    )
    user = cursor.fetchone()
    return user


def get_cities(user_id: int) -> list[dict]:
    """
    Returns list of cities
    """
    cursor.execute(
        """
            SELECT * FROM cities WHERE user_id = %s
        """, (user_id,)
    )
    cities = cursor.fetchall()
    return cities


def register_user(telegram_id: str, fullname: str, username: str) -> None:
    """
    Registers user in users table
    """
    cursor.execute(
        """
            INSERT INTO users (telegram_id, fullname, username) 
            VALUES (%s, %s, %s)
        """, (telegram_id, fullname, username)
    )
    database.commit()


def register_city(user_id: int, city_name: str) -> None:
    """
    Registers city in cities table
    """
    cursor.execute(
        """
            INSERT INTO cities (user_id, city_name)
            VALUES (%s, %s)
        """, (user_id, city_name)
    )
    database.commit()


def create_users_table() -> None:
    """
    Creates users table in database
    """
    cursor.execute(
        """
            CREATE TABLE IF NOT EXISTS users(
                id INT PRIMARY KEY AUTO_INCREMENT,
                telegram_id VARCHAR(200) NOT NULL UNIQUE,
                fullname VARCHAR(200),
                username VARCHAR(200)
            )
        """
    )


def create_cities_table() -> None:
    """
    Creates cities table
    """
    cursor.execute(
        """
            CREATE TABLE IF NOT EXISTS cities(
                id INT PRIMARY KEY AUTO_INCREMENT,
                user_id INT NOT NULL,
                city_name VARCHAR(200),

                CONSTRAINT unique_city_name_for_user UNIQUE(user_id, city_name)
            )
        """
    )


def clear_cities_list(user_id: int) ->None :
    cursor.execute("DELETE FROM cities WHERE user_id = %s", (user_id,))
    database.commit

if __name__ == "__main__":
    create_users_table()
    create_cities_table()