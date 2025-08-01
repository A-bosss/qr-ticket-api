import os, sqlite3

# Ruta de tu base de datos SQLite
DB_PATH = os.getenv("DB_PATH", "database.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """
    Crea la tabla inventory si no existe y
    inicializa el stock con 100 boletos si está vacía.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY,
            available INTEGER NOT NULL
        );
    """)
    # Si no hay ninguna fila, insertamos stock inicial
    cursor.execute("SELECT COUNT(*) FROM inventory;")
    if cursor.fetchone()[0] == 0:
        cursor.execute(
            "INSERT INTO inventory (available) VALUES (?);",
            (100,)  # stock inicial: 100 boletos
        )
    conn.commit()
    cursor.close()
    conn.close()

def descontar_boleto(cantidad: int) -> bool:
    """
    Resta 'cantidad' boletos de inventory.available sólo si hay stock suficiente.
    Devuelve True si la resta se aplicó, False si no había suficiente stock.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE inventory
        SET available = available - ?
        WHERE id = 1 AND available >= ?
        """,
        (cantidad, cantidad)
    )
    conn.commit()
    success = (cursor.rowcount == 1)
    cursor.close()
    conn.close()
    return success
