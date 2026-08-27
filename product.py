class Product:
    """Represent a single product in the warehouse inventory."""

    def __init__(
        self,
        product_name: str,
        sku: str,
        price: float,
        minimum_stock: int,
        description: str | None = None,
        product_id: int | None = None,
    ) -> None:
        """
        Initialize a product object.

        Args:
            product_name: The product name.
            sku: Unique product sku.
            price: The product price.
            minimum_stock: The product minimum_stock.
            description: The product description.
            product_id: Unique product ID.

        """
        self.product_id = product_id
        self.product_name = product_name
        self.sku = sku
        self.price = price
        self.minimum_stock = minimum_stock
        self.description = description

    def __repr__(self) -> str:
        return (
            f"Product(product_id ={self.product_id!r},product_name = {self.product_name!r},"
            f"sku = {self.sku!r},price = {self.price!r},minimum_stock = {self.minimum_stock!r},"
            f"description = {self.description!r})"
        )



