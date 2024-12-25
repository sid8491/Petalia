import json
from typing import List

from chromadb import EmbeddingFunction, Embeddings, PersistentClient
from langchain_ollama import OllamaEmbeddings

DB_PATH = "./.chroma_db"
EMBED_MODEL_NAME = "nomic-embed-text"
FAQ_FILE_PATH = "FAQ.json"
INVENTORY_FILE_PATH = "inventory.json"


class Product:
    def __init__(
        self,
        name: str,
        id: str,
        description: str,
        price: float,
        quantity: int,
        type: str,
    ):
        self.name = name
        self.id = id
        self.description = description
        self.price = price
        self.quantity = quantity
        self.type = type


class QuestionAnswer:
    def __init__(self, question: str, answer: str):
        self.question = question
        self.answer = answer


class CustomEmbeddingClass(EmbeddingFunction):
    def __init__(self, model_name):
        self.embedding_model = OllamaEmbeddings(model=model_name)

    def __call__(self, input_texts: List[str]) -> Embeddings:
        embeddings = []

        for text in input_texts:
            response = self.embedding_model.embed_query(text)
            embeddings.append(response)
        return embeddings


class FlowerShopVectorStore:
    def __init__(self):
        db = PersistentClient(path=DB_PATH)
        custom_embedding_function = CustomEmbeddingClass(EMBED_MODEL_NAME)

        self.faq_collection = db.get_or_create_collection(
            name="FAQ", embedding_function=custom_embedding_function
        )
        self.inventory_collection = db.get_or_create_collection(
            name="Inventory", embedding_function=custom_embedding_function
        )

        if self.faq_collection.count() == 0:
            self._load_faq_collection(FAQ_FILE_PATH)

        if self.inventory_collection.count() == 0:
            self._load_inventory_collection(INVENTORY_FILE_PATH)

    def _load_faq_collection(self, faq_file_path: str):
        with open(faq_file_path, "r") as file:
            faqs = json.load(file)

        self.faq_collection.add(
            documents=[f"{faq['question']} {faq['answer']}" for faq in faqs],
            ids=[f"faq-{i}" for i in range(len(faqs))],
            metadatas=[
                {"question": faq["question"], "answer": faq["answer"]} for faq in faqs
            ],
        )

    def _load_inventory_collection(self, inventory_file_path: str):
        with open(inventory_file_path, "r") as file:
            inventories = json.load(file)

        self.inventory_collection.add(
            documents=[inventory["description"] for inventory in inventories],
            ids=[f"inventory-{i}" for i in range(len(inventories))],
            metadatas=inventories,
        )

    def query_faqs(self, query: str):
        return self.faq_collection.query(query_texts=[query], n_results=5)

    def query_inventories(self, query: str):
        return self.inventory_collection.query(query_texts=[query], n_results=5)
