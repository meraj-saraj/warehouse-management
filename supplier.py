class Supplier:
    """Represent a single supplier"""

    def __init__(
        self,
        supplier_name: str,
        phone_number: str,
        email: str,
        supplier_id: int | None = None,
    ) -> None:
        """
        Initialize a supplier object.

        Args:
            supplier_name: The supplier name.
            phone_number: The supplier phone number.
            email: The supplier email.
            supplier_id: The supplier ID.
        """
        self.supplier_id = supplier_id
        self.supplier_name = supplier_name
        self.phone_number = phone_number
        self.email = email

    def __repr__(self) -> str:
        return (
            f"Supplier(supplier_id = {self.supplier_id!r}, "
            f"supplier_name = {self.supplier_name!r}, "
            f"phone_number = {self.phone_number!r}, "
            f"email = {self.email!r})"
        )
