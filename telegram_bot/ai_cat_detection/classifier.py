from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from database.mongo import get_user_category_samples


class CategoryClassifier:
    def __init__(self, category_examples: dict):
        """
        Category_examples: dict of categories with example phrases
        """
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.categories = []
        self.example_texts = []
        self.example_labels = []

        for category, examples in category_examples.items():
            for ex in examples:
                self.example_texts.append(ex)
                self.example_labels.append(category)
            self.categories.append(category)

        self.example_embeddings = self.model.encode(self.example_texts)

    def classify(self, user_input: str) -> str:
        user_embedding = self.model.encode([user_input])
        similarities = cosine_similarity(user_embedding, self.example_embeddings)
        best_match_index = np.argmax(similarities)
        return self.example_labels[best_match_index]


async def get_category(user_id: int, desc: str) -> str:
    categories = await get_user_category_samples(user_id)
    classifier = CategoryClassifier(categories)
    category = classifier.classify(desc)
    return category
