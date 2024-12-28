# Petalia: Flower Shop Customer Service Chatbot

Petalia is a chatbot designed to provide exceptional customer service for flower shop businesses. Built with cutting-edge AI technologies, it handles customer queries, order management, product recommendations, and more.




## Features

- **Customer Management**
  - Validate customer data with Data Protection Act (DPA) checks.
  - Create new customer profiles with complete details.

- **Order Management**
  - Retrieve customer order history.
  - Place new orders with inventory validation.

- **Product Recommendations**
  - Suggest personalized products based on user descriptions.

- **Knowledge Base Search**
  - Answer FAQs and provide information about business processes.

## Technologies Used

- **Backend**
  - Python
  - [LangChain Core](https://github.com/langchain-ai/langchain)
  - Custom Vector Store for FAQs and inventory queries

- **Frontend**
  - [Streamlit](https://streamlit.io/) for an interactive user interface

- **Databases**
  - Customer and order data are maintained in memory for the prototype.
  - Inventory and FAQs are loaded from a JSON file.


## Agent Flow
![Flow](/images/output_graph.png "Flow")

### Tools:

### 1. Data Protection Check
```python
@tool
def data_protection_check(name: str, year_of_birth: int, month_of_birth: int, day_of_birth: int) -> str:
    # Checks if customer data exists in the database
```

### 2. Create New Customer
```python
@tool
def create_new_customer(first_name: str, last_name: str, year_of_birth: int, month_of_birth: int, day_of_birth: int, mobile: str, email: str) -> str:
    # Adds a new customer to the database
```

### 3. Retrieve Customer Orders
```python
@tool
def retrieve_existing_customer_orders(customer_id: str) -> List[Dict]:
    # Fetches the order history of a customer
```

### 4. Place Order
```python
@tool
def place_order(customer_id: str, products: Dict[str, int]) -> str:
    # Places an order for the customer with inventory validation
```

### 5. Product Recommendations
```python
@tool
def search_for_product_recommendations(description: str) -> List[Dict[str, str]]:
    # Returns personalized product recommendations
```

### 6. Knowledge Base Queries
```python
@tool
def query_knowledge_base(query: str) -> list:
    # Searches for relevant information in the FAQ knowledge base
```

## How It Works

1. The chatbot interacts with customers through Streamlit, providing a seamless experience.
2. Backend tools process customer queries, validate data, and interact with the knowledge base and inventory.
3. Orders are placed only after inventory checks ensure availability.

## Prerequisites

- Python 3.8+
- Streamlit
- LangChain Core
- Langgraph
- A JSON file (`inventory.json`) with inventory details.

## Setup Instructions

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/petalia.git
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the Streamlit app:
   ```bash
   streamlit run gui.py
   ```

4. Access the chatbot at `http://localhost:8501` in your browser.

## Example Inventory JSON Format
```json
[
    {
      "id": "F025",
      "name": "Hydrangea Bouquet",
      "quantity": 12,
      "price": 45,
      "type": "Bouquet",
      "description": "A stunning bouquet of hydrangeas in pastel shades, known for their lush appearance. Perfect for decor or gifting."
    },
    {
      "id": "F026",
      "name": "Gerbera Daisies",
      "quantity": 40,
      "price": 18,
      "type": "Flower",
      "description": "Bright and cheerful gerbera daisies available in multiple colors. Ideal for spreading joy and positivity."
    }
]
```