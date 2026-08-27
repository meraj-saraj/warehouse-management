class Warehouse:
    def __init__(
        self, warehouse_name: str, location: str, warehouse_id: int | None = None
    ) -> None:
        """
        Initialize a warehouse object.

        Args:
            warehouse_name: The warehouse name.
            location: The warehouse location.
            warehouse_id: The warehouse ID.
        """

        self.warehouse_id = warehouse_id
        self.warehouse_name = warehouse_name
        self.location = location

    def __repr__(self) -> str:
        return (
            f"Warehouse(warehouse_id = {self.warehouse_id!r},"
            f"warehouse_name = {self.warehouse_name!r},"
            f"location = {self.location!r})"
        )


w1 = Warehouse("warehose_1", "Tehran")
print(w1)
