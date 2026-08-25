import sqlite3

class Database:
  def init(self,file_name:str = "database.db")->None:
    """
    Manage Database.

    Args:
      file_name: The name of the file.

    Returns:
      None
    """
    self.file_name=file_name
    self.connection = sqlite3.connect(self.file_name)
    cursor = self.connection.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")
    self.create_tables()

  def create_tables(self)-> None:
    """
    Create database tables.

    Returns:
      None
    """
    cursor = self.connection.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products(
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
   product_name TEXT NOT NULL,
   sku TEXT UNIQUE NOT NULL,
   price REAL NOT NULL CHECK(price>0),
   minimum_stock INTEGER NOT NULL CHECK(minimum_stock>=0),
   description TEXT
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS warehouses(
    warehouse_id INTEGER PRIMARY KEY AUTOINCREMENT,
    warehouse_name TEXT NOT NULL,
    location TEXT NOT NULL
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS suppliers(
    supplier_id INTEGER PRIMARY KEY AUTOINCREMENT,
    supplier_name TEXT NOT NULL,
    phone_number TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions(
    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL,
    warehouse_id INTEGER NOT NULL,
    type TEXT NOT NULL CHECK (type IN ('IN','OUT')),
    quantity INTEGER NOT NULL CHECK
    (quantity > 0),
    date TEXT DEFAULT CURRENT_TIMESTAMP NOT NULL,
    supplier_id INTEGER CHECK ((type ='IN' AND supplier_id IS NOT NULL)
    OR
    (type = 'OUT' AND supplier_id IS NULL)),
    FOREIGN KEY (product_id) REFERENCES products(product_id),
    FOREIGN KEY (warehouse_id) REFERENCES warehouses(warehouse_id),
    FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id)
    )
    """)
    self.connection.commit()



database = Database(":memory:")
print("Created tables is successfully.")