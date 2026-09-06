import sqlite3
from product import Product
from warehouse import Warehouse


class Database:
    def __init__(self, file_name: str = "database.db") -> None:
        """
        Manage Database.

        Args:
          file_name: The name of the file.

        Returns:
          None
        """
        self.file_name = file_name
        self.connection = sqlite3.connect(self.file_name)
        cursor = self.connection.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        self.create_tables()

    def create_tables(self) -> None:
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

    def add_product(self, product: Product) -> bool:
        """
        Add a product to products table.

        Args:
          product: A Product object.
        Returns:
          True if product was added; otherwise, False.
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                """
    INSERT INTO products(
    product_name,sku,price,minimum_stock,description
    )
    VALUES(?,?,?,?,?)
    """,
                (
                    product.product_name,
                    product.sku,
                    product.price,
                    product.minimum_stock,
                    product.description,
                ),
            )
            self.connection.commit()
            product.product_id = cursor.lastrowid
            return True
        except sqlite3.Error as e:
            print(f"Error: {e}")
            return False

    def row_to_product(self, row: tuple) -> Product:
        """
        Create a Product object.

        Args:
          row: A tuple from columns of products table.

        Returns:
          A Product object.
        """
        product_id = row[0]
        product_name = row[1]
        sku = row[2]
        price = row[3]
        minimum_stock = row[4]
        description = row[5]
        product = Product(
            product_id=product_id,
            product_name=product_name,
            sku=sku,
            price=price,
            minimum_stock=minimum_stock,
            description=description,
        )
        return product

    def rows_to_objects(self, rows: list[tuple], row_to_object) -> list[object]:
        """
        Convert a list of database rows into a list of objects.

        Args:
          rows: A list of tuples fetched from the database.
          row_to_object: A function that converts a single row into an object.

        Returns:
          A list of objects built from the rows.
        """
        objects = []
        for row in rows:
            objects.append(row_to_object(row))
        return objects

    def find_product(self, product_id: int) -> Product | None:
        """
        Find and return specifice product by ID.

        Args:
          product_id: The ID of the product.

        Returns:
          A Product object if found; otherwise, None.
        """
        cursor = self.connection.cursor()
        cursor.execute(
            """SELECT product_id,product_name,sku,price,minimum_stock,description FROM products WHERE product_id = ?""",
            (product_id,),
        )
        row = cursor.fetchone()
        if not row:
            return None
        return self.row_to_product(row)

    def get_all_products(self) -> list[Product]:
        """
        Get all products in products table.

        Returns:
          A list of Product objects.
        """
        cursor = self.connection.cursor()
        cursor.execute(
            """SELECT product_id,product_name,sku,price,minimum_stock,description FROM products"""
        )

        rows = cursor.fetchall()
        return self.rows_to_objects(rows, self.row_to_product)

    def commit_if_affected(self, rowcount: int) -> bool:
        """
        Check if a database operation affected any rows and commit if so.

        Args:
          rowcount: The number or rows affected by the last operation.

        Returns:
          True if at least one row was affected; otherwise, False.
        """
        if rowcount == 0:
            return False
        self.connection.commit()
        return True

    def value_not_none(
        self, value: str | int | float, field_name: str
    ) -> str | float | int:
        """
        Check value.

        Args:
          value: The value.
          field_name: The name of the field.

        Raises:
          ValueError:If value is None.

        Returns:
          The value.
        """
        if value is None:
            raise ValueError(f"The {field_name} can't be None.")
        return value

    def edit_product_name(self, product_id: int, product_new_name: str) -> bool:
        """
        Edit the name of the product.

        Args:
          product_id: The ID of the product.
          product_new_name: The new name of product.

        Raises:
          ValueError: If product_new_name is None.

        Returns:
          True if product name was edited; otherwise, False.
        """
        product_new_name = self.value_not_none(product_new_name, "product_name")
        cursor = self.connection.cursor()
        cursor.execute(
            """UPDATE products SET product_name = ? WHERE product_id = ?""",
            (product_new_name, product_id),
        )
        rowcount = cursor.rowcount
        return self.commit_if_affected(rowcount)

    def edit_sku(self, product_id: int, sku: str) -> bool:
        """
        Edit the product SKU.

        Args:
          product_id: The ID of the product.
          sku: The SKU of the product.

        Raises:
          ValueError: If sku is None
          sqlite3.IntegrityError: If sku already exists for another product.

        Returns:
          True if sku was edited; otherwise, False.
        """
        sku = self.value_not_none(sku, "product_SKU")
        cursor = self.connection.cursor()
        cursor.execute(
            """UPDATE products SET sku = ? WHERE product_id = ?""",
            (sku, product_id),
        )
        rowcount = cursor.rowcount
        return self.commit_if_affected(rowcount)

    def edit_price(self, product_id: int, new_price: float) -> bool:
        """
        Edit the product price.

        Args:
          product_id: The ID of the product.
          new_price: The product new price.

        Raises:
          ValueError: If new_price is None.
          sqlite3.IntegrityError: If new_price is not a positive number.

        Returns:
          True if price was edited; otherwise, False.
        """
        new_price = self.value_not_none(new_price, "product_price")
        cursor = self.connection.cursor()
        cursor.execute(
            """UPDATE products SET price = ? WHERE product_id = ?""",
            (new_price, product_id),
        )
        rowcount = cursor.rowcount
        return self.commit_if_affected(rowcount)

    def edit_minimum_stock(self, product_id: int, new_minimum_stock: int) -> bool:
        """
        Edit the product minimum_stock.

        Args:
          product_id: The ID of product.
          new_minimum_stock: The product new_minimum_stock.

        Raises:
          ValueError: If new_minimum_stock is None.
          sqlite3.IntegrityError: If new_minimum_stock is a negative number.

        Returns:
          True if minimum_stock was edited; otherwise, False.
        """
        new_minimum_stock = self.value_not_none(new_minimum_stock, "minimum_stock")
        cursor = self.connection.cursor()
        cursor.execute(
            """UPDATE products SET minimum_stock = ? WHERE product_id = ?""",
            (new_minimum_stock, product_id),
        )
        rowcount = cursor.rowcount
        return self.commit_if_affected(rowcount)

    def edit_description(self, product_id: int, new_description: str | None) -> bool:
        """
        Edit the product description.

        Args:
          product_id: The ID of product.
          new_description: The product new_description.

        Returns:
          True if descriptin was edited; otherwise, False.
        """
        cursor = self.connection.cursor()
        cursor.execute(
            """UPDATE products SET description = ? WHERE product_id = ?""",
            (new_description, product_id),
        )
        rowcount = cursor.rowcount
        return self.commit_if_affected(rowcount)

    def remove_product(self, product_id: int) -> bool:
        """
        Remove a product from products table.

        Args:
          product_id: The ID of the product.
        Raises:
          sqlite3.IntegrityError: If the product has related transactions and therefore cannot be deleted.
        Returns:
          True if product was removed; otherwise, False.
        """
        cursor = self.connection.cursor()
        cursor.execute(
            """DELETE FROM products WHERE product_id = ?""",
            (product_id,),
        )
        rowcount = cursor.rowcount
        return self.commit_if_affected(rowcount)

    def add_warehouse(self, warehouse: Warehouse) -> bool:
        """
        Add a warehouse to warehouses table.

        Args:
          warehouse: A Warehouse object.

        Returns:
          True if warehouse was added; otherwise, False.
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                """
    INSERT INTO warehouses(
    warehouse_name,location
    )
    VALUES(?,?)
    """,
                (warehouse.warehouse_name, warehouse.location),
            )
            self.connection.commit()
            warehouse.warehouse_id = cursor.lastrowid
            return True
        except sqlite3.Error as e:
            print(f"Error: {e}")
            return False

    def row_to_warehouse(self, row: tuple) -> Warehouse:
        """
        Create a Warehouse object.

        Args:
          row: A tuple from columns of warehouses table.

        Returns:
          A Warehouse object.
        """
        warehouse_id = row[0]
        warehouse_name = row[1]
        location = row[2]
        warehouse = Warehouse(
            warehouse_id=warehouse_id, warehouse_name=warehouse_name, location=location
        )
        return warehouse

    def find_warehouse(self, warehouse_id: int) -> Warehouse | None:
        """
        Find and return specifice warehouse by ID.

        Args:
          warehouse_id: The warehouse ID.

        Returns:
          A Warehouse object if found;otherwise, None.
        """
        cursor = self.connection.cursor()
        cursor.execute(
            """SELECT warehouse_id,warehouse_name,location FROM warehouses WHERE warehouse_id = ?""",
            (warehouse_id,),
        )
        row = cursor.fetchone()
        if not row:
            return None
        return self.row_to_warehouse(row)

    def get_all_warehouses(self) -> list[Warehouse]:
        """
        Get all warehouses in warehouses table.

        Returns:
          A list of Warehouse object.
        """

        cursor = self.connection.cursor()
        cursor.execute(
            """SELECT warehouse_id,warehouse_name,location FROM warehouses"""
        )
        rows = cursor.fetchall()
        return self.rows_to_objects(rows, self.row_to_warehouse)

    def edit_warehouse_name(self, warehouse_id: int, warehouse_new_name: str) -> bool:
        """
        Edit the warehouse name.

        Args:
          warehouse_id: The warehouse ID.
          warehouse_new_name: The warehouse new name.

        Raises:
          ValueError: If warehouse_new_name is None.

        Returns:
          True if warehouse name was edited; otherwise, False.
        """
        warehouse_new_name = self.value_not_none(warehouse_new_name, "warehouse name")
        cursor = self.connection.cursor()
        cursor.execute(
            """UPDATE warehouses SET warehouse_name = ? WHERE warehouse_id = ?""",
            (warehouse_new_name, warehouse_id),
        )
        rowcount = cursor.rowcount
        return self.commit_if_affected(rowcount)

    def edit_location(self, warehouse_id: int, new_location: str) -> bool:
        """
        Edit the warehouse location.

        Args:
          warehouse_id: The warehouse ID.
          new_location: The warehouse new location.

        Raises:
          ValueError: If warehouse_new_location is None.

        Returns:
          True if location was edited; otherwise, False.
        """
        new_location = self.value_not_none(new_location, "location")
        cursor = self.connection.cursor()
        cursor.execute(
            """UPDATE warehouses SET location = ? WHERE warehouse_id = ?""",
            (new_location, warehouse_id),
        )
        rowcount = cursor.rowcount
        return self.commit_if_affected(rowcount)

    def remove_warehouse(self, warehouse_id: int) -> bool:
        """
        Remove a warehouse from warehouses table.

        Args:
          warehouse_id: The warehouse ID.

        Raises:
          sqlite3.IntegrityError: If the warehouse has related transactions and therefore cannot be deleted.

        Returns:
          True if warehouse was removed; otherwise, False.
        """
        cursor = self.connection.cursor()
        cursor.execute(
            """DELETE FROM warehouses WHERE warehouse_id = ?""", (warehouse_id,)
        )
        rowcount = cursor.rowcount
        return self.commit_if_affected(rowcount)