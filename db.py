# db.py

import sqlite3
import bcrypt

DB_FILE = "volunteer.db"


# Узагальнені категорії волонтерської діяльності
volunteer_categories = [
    "Допомога у школі",
    "Освітні та навчальні проєкти",
    "Соціальні ініціативи",
    "Екологічні акції",
    "Культурні та мистецькі проєкти",
    "Спортивні заходи",
    "Громадські ініціативи",
    "Інше"
]









def init_db():
    """Створює таблицю, якщо її ще немає"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS volunteer (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            hours INTEGER NOT NULL,
            category TEXT,
            description TEXT,
            photo BLOB
        )
    """)
    conn.commit()
    conn.close()



def add_volunteer(name, hours, category=None, description=None, photo=None):
    """Додає запис у базу"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        INSERT INTO volunteer (name, hours, category, description, photo)
        VALUES (?, ?, ?, ?, ?)
    """, (name, hours, category, description, photo))
    conn.commit()
    conn.close()



def get_volunteers():
    """Повертає всі записи з бази"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    # Додаємо колонку category у SELECT
    c.execute("SELECT id, name, hours, category, description, photo FROM volunteer")
    rows = c.fetchall()
    conn.close()
    return rows















    
#Де можна допомогти




def init_dh():
    """Створює таблицю, якщо її ще немає"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS volh (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            colh TEXT NOT NULL,
            detail TEXT NOT NULL,
            hours INTEGER NOT NULL
        )
    """)
    conn.commit()
    conn.close()



def add_dh(colh, detail, hours=None):
    """Додає запис у базу"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        INSERT INTO volh (colh, detail, hours)
        VALUES (?, ?, ? )
    """, (colh, detail, hours))
    conn.commit()
    conn.close()



def get_volh():
    """Повертає всі записи з бази"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    # Додаємо колонку category у SELECT
    c.execute("SELECT id, colh, detail, hours  FROM volh")
    rows = c.fetchall()
    conn.close()
    return rows


#Для авторизації


def init_db_users():
    """Створює таблицю users, якщо її ще немає"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT UNIQUE,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'user',  -- 'user' або 'admin'
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()





# Функція для створення фіксованого адміна
def create_admin_if_not_exists():
    """Створює фіксованого адміна, якщо його немає"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT username FROM users WHERE username = 'admin'")
    if not c.fetchone():
        # Пароль: 123!
        plain_password = "123"
        hashed = bcrypt.hashpw(plain_password.encode('utf-8'), bcrypt.gensalt())
        c.execute("""
            INSERT INTO users (username, name, email, password_hash, role)
            VALUES (?, ?, ?, ?, ?)
        """, ("admin", "Адміністратор", "admin@example.com", hashed.decode('utf-8'), "admin"))
        conn.commit()
    conn.close()

# Функція реєстрації користувача
def register_user(username, name, email, password, role="user"):
    """Реєстрація нового користувача"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    try:
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        c.execute("""
            INSERT INTO users (username, name, email, password_hash, role)
            VALUES (?, ?, ?, ?, ?)
        """, (username, name, email, hashed, role))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False  # username або email вже зайняті
    finally:
        conn.close()

# Функція аутентифікації користувача
def authenticate_user(username, password):
    """Перевірка логіну, повертає (success, name, role) або (False, None, None)"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT name, password_hash, role FROM users WHERE username = ?", (username,))
    row = c.fetchone()
    conn.close()
    
    if row:
        name, stored_hash, role = row
        if bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8')):
            return True, name, role
    return False, None, None

# Додаткова функція для отримання загальної кількості годин
def get_total_hours():
    """Повертає загальну кількість волонтерських годин"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT SUM(hours) FROM volunteer")
    total = c.fetchone()[0]
    conn.close()
    return int(total) if total is not None else 0