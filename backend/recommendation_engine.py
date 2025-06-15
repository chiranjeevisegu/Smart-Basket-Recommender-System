import random
import numpy as np
from typing import List, Dict, Any
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import spacy

class RecommendationEngine:
    def __init__(self):
        self.sentence_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.nlp = spacy.load("en_core_web_sm")
        
        # Dummy user baskets for collaborative filtering
        self.user_baskets = self._initialize_user_baskets()
        
        # Popular bundles for discount recommendations
        self.popular_bundles = [
            ["Fresh Red Apples", "Organic Bananas", "Fresh Oranges"],
            ["Chicken Breast", "Brown Rice", "Fresh Broccoli"],
            ["Whole Milk", "Cheddar Cheese", "Large Eggs"],
            ["Ground Beef", "Spaghetti", "Canned Tomatoes"],
            ["Fresh Tomatoes", "Iceberg Lettuce", "Baby Carrots"],
            ["Atlantic Salmon", "Steel Cut Oats", "Fresh Spinach"],
            ["Greek Yogurt", "Mixed Nuts", "Fresh Red Apples"],
            ["Whole Wheat Bread", "Unsalted Butter", "Jam"],
            ["Pork Chops", "Fresh Garlic", "Yellow Onions"],
            ["Frozen Pizza", "Cola", "Potato Chips"]
        ]
        
        # Health warnings for unhealthy combinations
        self.health_warnings = {
            "high_sugar": ["Chocolate Chip Cookies", "Cola", "Orange Juice", "Strawberry Jam", "Vanilla Ice Cream"],
            "high_sodium": ["Potato Chips", "Canned Tuna", "Canned Tomatoes", "Soy Sauce"],
            "high_fat": ["Ground Beef", "Pork Chops", "Mayonnaise", "Extra Virgin Olive Oil"]
        }
        
        # Category relationships for recommendations
        self.category_relationships = {
            "Fruits": ["Vegetables", "Dairy"],
            "Vegetables": ["Fruits", "Meat", "Grains"],
            "Meat": ["Vegetables", "Grains", "Condiments"],
            "Dairy": ["Fruits", "Grains"],
            "Grains": ["Vegetables", "Meat", "Dairy"],
            "Seafood": ["Vegetables", "Grains"],
            "Snacks": ["Beverages"],
            "Beverages": ["Snacks"],
            "Frozen": ["Beverages"],
            "Canned": ["Grains", "Vegetables"],
            "Condiments": ["Meat", "Grains"]
        }
    
    def _initialize_user_baskets(self) -> List[List[str]]:
        """Initialize dummy user baskets for collaborative filtering"""
        return [
            ["Fresh Red Apples", "Organic Bananas", "Whole Milk", "Cheddar Cheese"],
            ["Chicken Breast", "Brown Rice", "Fresh Broccoli", "Fresh Carrots"],
            ["Ground Beef", "Spaghetti", "Canned Tomatoes", "Fresh Garlic"],
            ["Atlantic Salmon", "Steel Cut Oats", "Fresh Spinach", "Fresh Tomatoes"],
            ["Greek Yogurt", "Mixed Nuts", "Fresh Red Apples", "Honey"],
            ["Whole Wheat Bread", "Unsalted Butter", "Jam", "Milk"],
            ["Pork Chops", "Fresh Garlic", "Yellow Onions", "Fresh Broccoli"],
            ["Frozen Pizza", "Cola", "Potato Chips", "Ice Cream"],
            ["Fresh Tomatoes", "Iceberg Lettuce", "Baby Carrots", "Cucumber"],
            ["Large Eggs", "Bacon", "Whole Wheat Bread", "Butter"]
        ]
    
    def get_recommendations(self, cart_items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Get top 5 recommendations based on cart items"""
        if not cart_items:
            return self._get_popular_items()
        
        # Get product names from cart
        cart_product_names = [item["name"] for item in cart_items]
        cart_categories = [item["category"] for item in cart_items]
        
        # Combine different recommendation strategies
        recommendations = []
        
        # 1. Collaborative filtering based on similar baskets
        cf_recommendations = self._collaborative_filtering(cart_product_names)
        recommendations.extend(cf_recommendations[:2])
        
        # 2. Category-based recommendations
        category_recommendations = self._category_based_recommendations(cart_categories)
        recommendations.extend(category_recommendations[:2])
        
        # 3. Semantic similarity based on product descriptions
        semantic_recommendations = self._semantic_similarity_recommendations(cart_items)
        recommendations.extend(semantic_recommendations[:1])
        
        # Remove duplicates and cart items
        unique_recommendations = []
        seen_products = set(cart_product_names)
        
        for rec in recommendations:
            if rec["name"] not in seen_products:
                unique_recommendations.append(rec)
                seen_products.add(rec["name"])
        
        return unique_recommendations[:5]
    
    def _collaborative_filtering(self, cart_items: List[str]) -> List[Dict[str, Any]]:
        """Collaborative filtering based on similar user baskets"""
        # Find baskets with similar items
        similar_baskets = []
        for basket in self.user_baskets:
            overlap = len(set(cart_items) & set(basket))
            if overlap > 0:
                similar_baskets.append((basket, overlap))
        
        # Sort by overlap and get recommendations
        similar_baskets.sort(key=lambda x: x[1], reverse=True)
        
        recommendations = []
        for basket, _ in similar_baskets[:3]:
            for item in basket:
                if item not in cart_items:
                    # Find product details
                    product = self._find_product_by_name(item)
                    if product:
                        recommendations.append(product)
        
        return recommendations[:3]
    
    def _category_based_recommendations(self, cart_categories: List[str]) -> List[Dict[str, Any]]:
        """Get recommendations based on category relationships"""
        related_categories = set()
        for category in cart_categories:
            if category in self.category_relationships:
                related_categories.update(self.category_relationships[category])
        
        recommendations = []
        for category in related_categories:
            products = self._get_products_by_category(category)
            if products:
                recommendations.extend(random.sample(products, min(2, len(products))))
        
        return recommendations[:3]
    
    def _semantic_similarity_recommendations(self, cart_items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Get recommendations based on semantic similarity of product descriptions"""
        if not cart_items:
            return []
        
        # Get descriptions from cart items
        cart_descriptions = [item["description"] for item in cart_items if "description" in item]
        if not cart_descriptions:
            return []
        
        # Get all available products
        all_products = self._get_all_products()
        
        # Calculate similarity scores
        similarities = []
        for product in all_products:
            if "description" in product and product["name"] not in [item["name"] for item in cart_items]:
                product_desc = product["description"]
                
                # Calculate similarity using sentence transformers
                cart_embeddings = self.sentence_model.encode(cart_descriptions)
                product_embedding = self.sentence_model.encode([product_desc])
                
                similarity = cosine_similarity(cart_embeddings, product_embedding).mean()
                similarities.append((product, similarity))
        
        # Sort by similarity and return top recommendations
        similarities.sort(key=lambda x: x[1], reverse=True)
        return [product for product, _ in similarities[:3]]
    
    def calculate_nutrition(self, cart_items: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate total nutrition for cart items"""
        total_nutrition = {
            "calories": 0,
            "protein": 0,
            "carbs": 0,
            "fat": 0,
            "fiber": 0,
            "sugar": 0
        }
        
        for item in cart_items:
            if "nutrition" in item:
                nutrition = item["nutrition"]
                quantity = item.get("quantity", 1)
                
                for key in total_nutrition:
                    if key in nutrition:
                        total_nutrition[key] += nutrition[key] * quantity
        
        return total_nutrition
    
    def find_bundle_discounts(self, cart_items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Find available bundle discounts"""
        cart_product_names = [item["name"] for item in cart_items]
        available_bundles = []
        
        for bundle in self.popular_bundles:
            bundle_items_in_cart = [item for item in bundle if item in cart_product_names]
            if len(bundle_items_in_cart) >= 2:
                missing_items = [item for item in bundle if item not in cart_product_names]
                if missing_items:
                    available_bundles.append({
                        "bundle_name": f"Bundle with {', '.join(bundle_items_in_cart)}",
                        "discount": "15% off",
                        "missing_items": missing_items[:2],
                        "savings": "$2.50"
                    })
        
        return available_bundles[:3]
    
    def check_health_warnings(self, cart_items: List[Dict[str, Any]]) -> List[str]:
        """Check for health warnings based on cart items"""
        warnings = []
        cart_product_names = [item["name"] for item in cart_items]
        
        # Check for high sugar items
        high_sugar_items = [item for item in cart_product_names if item in self.health_warnings["high_sugar"]]
        if len(high_sugar_items) >= 2:
            warnings.append(f"⚠️ High sugar content detected: {', '.join(high_sugar_items)}")
        
        # Check for high sodium items
        high_sodium_items = [item for item in cart_product_names if item in self.health_warnings["high_sodium"]]
        if len(high_sodium_items) >= 2:
            warnings.append(f"⚠️ High sodium content detected: {', '.join(high_sodium_items)}")
        
        # Check for high fat items
        high_fat_items = [item for item in cart_product_names if item in self.health_warnings["high_fat"]]
        if len(high_fat_items) >= 2:
            warnings.append(f"⚠️ High fat content detected: {', '.join(high_fat_items)}")
        
        return warnings
    
    def _get_popular_items(self) -> List[Dict[str, Any]]:
        """Get popular items when cart is empty"""
        popular_items = [
            "Fresh Red Apples", "Organic Bananas", "Whole Milk", 
            "Chicken Breast", "Fresh Tomatoes", "Whole Wheat Bread"
        ]
        
        recommendations = []
        for item_name in popular_items:
            product = self._find_product_by_name(item_name)
            if product:
                recommendations.append(product)
        
        return recommendations[:5]
    
    def _find_product_by_name(self, name: str) -> Dict[str, Any]:
        """Find product by name (placeholder - would connect to product catalog)"""
        # This would normally connect to the product catalog
        # For now, return a dummy product
        return {
            "id": f"{name.lower().replace(' ', '_')}_001",
            "name": name,
            "category": "General",
            "price": round(random.uniform(1.99, 8.99), 2),
            "nutrition": {"calories": 100, "protein": 5, "carbs": 15, "fat": 3, "fiber": 2, "sugar": 8},
            "image": "🛒",
            "description": f"Popular {name.lower()} product"
        }
    
    def _get_products_by_category(self, category: str) -> List[Dict[str, Any]]:
        """Get products by category (placeholder)"""
        # This would normally connect to the product catalog
        return []
    
    def _get_all_products(self) -> List[Dict[str, Any]]:
        """Get all products (placeholder)"""
        # This would normally connect to the product catalog
        return [] 