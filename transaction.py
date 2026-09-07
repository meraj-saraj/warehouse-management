class Transaction:
    """
    Represent a single transaction.
    """
    def __init__(self,product_id:int,warehouse_id:int,transaction_type:str,product_quantity:int,date:str|None = None,supplier_id:int |None = None,transaction_id:int|None=None):
        """
        Initialize a transaction object.

        Args:
            product_id: The product ID.
            warehouse_id: The warehouse ID.
            transaction_type: The transaction type(IN or OUT).
            product_quantity: The product quantity.
            date: The transaction date.
            supplier_id: The supplier ID.
            transaction_id: The transaction ID.
        """
        self.transaction_id = transaction_id
        self.product_id = product_id
        self.warehouse_id = warehouse_id
        self.transaction_type = transaction_type
        self.product_quantity = product_quantity
        self.date = date
        self.supplier_id = supplier_id
