import json
from typing import Dict, List

from langchain_core.tools import tool

from vector_store import FlowerShopVectorStore

vector_store = FlowerShopVectorStore()

customer_db = [
    {
        "name": "Anika Sharma",
        "dob": "1995/07/23",
        "customer_id": "CUST001",
        "mobile": "+91 9876543210",
        "email": "anika.sharma@gmail.com",
    },
    {
        "name": "Vijay Kumar",
        "dob": "1988/12/15",
        "customer_id": "CUST002",
        "mobile": "+91 7890123456",
        "email": "vijay.kumar@gmail.com",
    },
    {
        "name": "Priya Patel",
        "dob": "2002/03/08",
        "customer_id": "CUST003",
        "mobile": "+91 6789012345",
        "email": "priya.patel@gmail.com",
    },
]

orders_db = [
    {
        "order_id": "ORD001",
        "customer_id": "CUST001",
        "status": "Processing",
        "products": ["Bouquet of Roses", "Bouquet of Lilies"],
    },
    {
        "order_id": "ORD002",
        "customer_id": "CUST002",
        "status": "Delivered",
        "products": ["Bouquet of Tulips"],
    },
]

with open("inventory.json") as f:
    inventory_db = json.load(f)


@tool
def data_protection_check(
    name: str, year_of_birth: int, month_of_birth: int, day_of_birth: int
) -> str:
    """
    Check if the user's data is stored in the database and return the user's information if it is.

    Args:
        name (str): The name of the user
        year_of_birth (int): The year of birth of the user
        month_of_birth (int): The month of birth of the user
        day_of_birth (int): The day of birth of the user

    Returns:
        Dict[str, str]: The user's information if it is stored in the database
    """
    dob = f"{year_of_birth}/{month_of_birth:02d}/{day_of_birth:02d}"
    for customer in customer_db:
        if customer["name"] == name and customer["dob"] == dob:
            return f"DPA Check passed - Customer details:\n {customer}"
    return "DPA Check failed - Customer details not found"


@tool
def create_new_customer(
    first_name: str,
    last_name: str,
    year_of_birth: int,
    month_of_birth: int,
    day_of_birth: int,
    mobile: str,
    email: str,
) -> str:
    """
    Create a new customer in the database.

    Args:
        first_name (str): The first name of the customer
        last_name (str): The last name of the customer
        year_of_birth (int): The year of birth of the customer
        month_of_birth (int): The month of birth of the customer
        day_of_birth (int): The day of birth of the customer
        mobile (str): The mobile number of the customer
        email (str): The email address of the customer

    Returns:
        str: A message confirming the creation of the new customer
    """
    if len(mobile) != 10:
        return "Invalid mobile number. Please enter a 10-digit mobile number."

    dob = f"{year_of_birth}/{month_of_birth:02d}/{day_of_birth:02d}"
    customer_id = f"CUST{len(customer_db) + 1:03d}"
    customer_db.append(
        {
            "name": f"{first_name} {last_name}",
            "dob": dob,
            "customer_id": customer_id,
            "mobile": mobile,
            "email": email,
        }
    )
    return f"New customer created - Customer ID: {customer_id}"


@tool
def query_knowledge_base(query: str) -> list:
    """
    Look up the information in a knowledge base to help with answering customer questions and getting information on business processes.

    Args:
        query (str): The query to search for in the knowledge base


        Return:
        List[Dict[str, str]]: Potentially relevant question and answer pairs from the knowledge base
    """
    return vector_store.query_faqs(query=query)


@tool
def search_for_product_recommendations(description: str) -> List[Dict[str, str]]:
    """
    Look up the information in a knowledge base to help with product recommendations for customers.
    For example:
    'Bouquets suitable for birthdays, maybe with red flowers'
    'Flowers for a wedding'
    'Bouquet for my girlfrind for our anniversary'
    'A cheap bouquet with wildflowers'

    Args:
        query (str): Description of product features


        Return:
        List[Dict[str, str]]: Potentially relevant products based on the description
    """
    return vector_store.query_inventories(query=description)


@tool
def retrieve_existing_customer_orders(customer_id: str) -> List[Dict]:
    """
    Retrieve the order history of an existing customer, including their status, items and order ID.

    Args:
        customer_id (str): The ID of the customer

    Returns:
        List[Dict]: The order history of the customer
    """
    orders = [order for order in orders_db if order["customer_id"] == customer_id]
    if not orders:
        return f"No orders found for customer {customer_id}"
    return orders


@tool
def place_order(customer_id: str, products: Dict[str, int]) -> str:
    """
    Place an order for a customer with the specified products nd their quantities.

    Args:
        customer_id (str): The ID of the customer
        products (Dict[str, int]): The products to be ordered, with item id as the key and quantity of that item as the value

    Returns:
        str: A message confirming the placement of the order
    """
    availability_messages = []
    valid_item_ids = [item["id"] for item in inventory_db]

    for item_id, quantity in products.items():
        if item_id not in valid_item_ids:
            availability_messages.append(
                f"Item with ID: {item_id} not found in inventory"
            )
        else:
            inventory_item = [item for item in inventory_db if item["id"] == item_id][0]
            if quantity > inventory_item["quantity"]:
                availability_messages.append(
                    f"Insufficient quantity for item: {inventory_item['name']}. Available quantity: {inventory_item['quantity']}"
                )
    if availability_messages:
        return f"Cannot place the order due to following issues:\n {'\n'.join(availability_messages)}"

    order_id = f"ORD{len(orders_db) + 1:03d}"
    orders_db.append(
        {
            "order_id": order_id,
            "customer_id": customer_id,
            "status": "Processing",
            "products": list(products.keys()),
            "quantity": list(products.values()),
        }
    )

    for item_id, quantity in products.items():
        inventory_item = [item for item in inventory_db if item["id"] == item_id][0]
        inventory_item["quantity"] -= quantity
        inventory_item["quantity"] = max(0, inventory_item["quantity"])
    return f"Order placed - Order ID: {order_id}"
