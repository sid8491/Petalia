from langchain_core.tools import tool

from vector_store import FlowerShopVectorStore

vector_store = FlowerShopVectorStore()


@tool
def query_knowledge_base(query: str):
    """
    Look up the information in a knowledge base to help with answering customer questions and getting information on business processes.

    Args:
        query (str): The query to search for in the knowledge base


        Return:
        List[Dict[str, str]]: Potentially relevant question and answer pairs from the knowledge base
    """
    return vector_store.query_faqs(query=query)


@tool
def search_for_product_recommendations(description: str):
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
