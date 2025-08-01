
import sqlite3

def init_db():
    with sqlite3.connect("tickets.db") as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS tickets (
                id TEXT PRIMARY KEY,
                nombre TEXT,
                numero TEXT,
                ciudad TEXT,
                email TEXT,
                usado INTEGER DEFAULT 0
            )
        ''')
        c.execute('''
            CREATE TABLE IF NOT EXISTS stock (
                id INTEGER PRIMARY KEY,
                disponibles INTEGER
            )
        ''')
        c.execute('INSERT OR IGNORE INTO stock (id, disponibles) VALUES (1, 100)')
        conn.commit()

def descontar_boleto():
    with sqlite3.connect("tickets.db") as conn:
        c = conn.cursor()
        c.execute('SELECT disponibles FROM stock WHERE id = 1')
        disponibles = c.fetchone()[0]
        if disponibles > 0:
            c.execute('UPDATE stock SET disponibles = disponibles - 1 WHERE id = 1')
            conn.commit()
            return True
        return False
