import random
from typing import List, Dict, Any

class ProductCatalog:
    def __init__(self):
        self.products = self._initialize_products()
        
    def _initialize_products(self) -> List[Dict[str, Any]]:
        """Initialize with 50+ dummy products"""
        products = [
            # Fruits & Vegetables
            {"id": "apple_001", "name": "Fresh Red Apples", "category": "Fruits", "price": 2.99, 
             "nutrition": {"calories": 95, "protein": 0.5, "carbs": 25, "fat": 0.3, "fiber": 4, "sugar": 19},
             "image": "🍎", "description": "Sweet and crisp red apples, perfect for snacking"},
            
            {"id": "banana_001", "name": "Organic Bananas", "category": "Fruits", "price": 1.99,
             "nutrition": {"calories": 105, "protein": 1.3, "carbs": 27, "fat": 0.4, "fiber": 3, "sugar": 14},
             "image": "🍌", "description": "Ripe organic bananas, great source of potassium"},
            
            {"id": "tomato_001", "name": "Fresh Tomatoes", "category": "Vegetables", "price": 3.49,
             "nutrition": {"calories": 22, "protein": 1.1, "carbs": 5, "fat": 0.2, "fiber": 1, "sugar": 3},
             "image": "🍅", "description": "Juicy red tomatoes, perfect for salads and cooking"},
            
            {"id": "lettuce_001", "name": "Iceberg Lettuce", "category": "Vegetables", "price": 1.99,
             "nutrition": {"calories": 14, "protein": 0.9, "carbs": 3, "fat": 0.1, "fiber": 1, "sugar": 1},
             "image": "🥬", "description": "Crisp iceberg lettuce for fresh salads"},
            
            {"id": "carrot_001", "name": "Baby Carrots", "category": "Vegetables", "price": 2.49,
             "nutrition": {"calories": 41, "protein": 0.9, "carbs": 10, "fat": 0.2, "fiber": 3, "sugar": 5},
             "image": "🥕", "description": "Sweet baby carrots, perfect for snacking"},
            
            # Dairy & Eggs
            {"id": "milk_001", "name": "Whole Milk", "category": "Dairy", "price": 3.99,
             "nutrition": {"calories": 150, "protein": 8, "carbs": 12, "fat": 8, "fiber": 0, "sugar": 12},
             "image": "🥛", "description": "Fresh whole milk, rich in calcium and protein"},
            
            {"id": "cheese_001", "name": "Cheddar Cheese", "category": "Dairy", "price": 4.99,
             "nutrition": {"calories": 113, "protein": 7, "carbs": 1, "fat": 9, "fiber": 0, "sugar": 0},
             "image": "🧀", "description": "Sharp cheddar cheese, perfect for sandwiches"},
            
            {"id": "eggs_001", "name": "Large Eggs", "category": "Dairy", "price": 3.49,
             "nutrition": {"calories": 70, "protein": 6, "carbs": 0, "fat": 5, "fiber": 0, "sugar": 0},
             "image": "🥚", "description": "Farm fresh large eggs, great for breakfast"},
            
            {"id": "yogurt_001", "name": "Greek Yogurt", "category": "Dairy", "price": 2.99,
             "nutrition": {"calories": 130, "protein": 23, "carbs": 9, "fat": 4, "fiber": 0, "sugar": 9},
             "image": "🍶", "description": "Creamy Greek yogurt, high in protein"},
            
            # Meat & Poultry
            {"id": "chicken_001", "name": "Chicken Breast", "category": "Meat", "price": 8.99,
             "nutrition": {"calories": 165, "protein": 31, "carbs": 0, "fat": 3.6, "fiber": 0, "sugar": 0},
             "image": "🍗", "description": "Lean chicken breast, perfect for healthy meals"},
            
            {"id": "beef_001", "name": "Ground Beef", "category": "Meat", "price": 6.99,
             "nutrition": {"calories": 250, "protein": 26, "carbs": 0, "fat": 15, "fiber": 0, "sugar": 0},
             "image": "🥩", "description": "Fresh ground beef, 80% lean"},
            
            {"id": "salmon_001", "name": "Atlantic Salmon", "category": "Seafood", "price": 12.99,
             "nutrition": {"calories": 208, "protein": 25, "carbs": 0, "fat": 12, "fiber": 0, "sugar": 0},
             "image": "🐟", "description": "Fresh Atlantic salmon, rich in omega-3"},
            
            # Grains & Bread
            {"id": "bread_001", "name": "Whole Wheat Bread", "category": "Grains", "price": 2.99,
             "nutrition": {"calories": 80, "protein": 4, "carbs": 15, "fat": 1, "fiber": 3, "sugar": 2},
             "image": "🍞", "description": "Nutritious whole wheat bread"},
            
            {"id": "rice_001", "name": "Brown Rice", "category": "Grains", "price": 3.99,
             "nutrition": {"calories": 216, "protein": 5, "carbs": 45, "fat": 1.8, "fiber": 4, "sugar": 0},
             "image": "🍚", "description": "Organic brown rice, high in fiber"},
            
            {"id": "pasta_001", "name": "Spaghetti", "category": "Grains", "price": 1.99,
             "nutrition": {"calories": 200, "protein": 7, "carbs": 42, "fat": 1, "fiber": 2, "sugar": 1},
             "image": "🍝", "description": "Classic spaghetti pasta"},
            
            # Snacks & Beverages
            {"id": "chips_001", "name": "Potato Chips", "category": "Snacks", "price": 3.99,
             "nutrition": {"calories": 160, "protein": 2, "carbs": 15, "fat": 10, "fiber": 1, "sugar": 1},
             "image": "🥔", "description": "Crispy potato chips, classic flavor"},
            
            {"id": "cookies_001", "name": "Chocolate Chip Cookies", "category": "Snacks", "price": 2.99,
             "nutrition": {"calories": 150, "protein": 2, "carbs": 20, "fat": 7, "fiber": 1, "sugar": 12},
             "image": "🍪", "description": "Delicious chocolate chip cookies"},
            
            {"id": "soda_001", "name": "Cola", "category": "Beverages", "price": 1.99,
             "nutrition": {"calories": 150, "protein": 0, "carbs": 39, "fat": 0, "fiber": 0, "sugar": 39},
             "image": "🥤", "description": "Refreshing cola beverage"},
            
            {"id": "water_001", "name": "Bottled Water", "category": "Beverages", "price": 0.99,
             "nutrition": {"calories": 0, "protein": 0, "carbs": 0, "fat": 0, "fiber": 0, "sugar": 0},
             "image": "💧", "description": "Pure spring water"},
            
            # Frozen Foods
            {"id": "pizza_001", "name": "Frozen Pizza", "category": "Frozen", "price": 5.99,
             "nutrition": {"calories": 285, "protein": 12, "carbs": 35, "fat": 12, "fiber": 2, "sugar": 4},
             "image": "🍕", "description": "Delicious frozen pizza, ready to bake"},
            
            {"id": "icecream_001", "name": "Vanilla Ice Cream", "category": "Frozen", "price": 4.99,
             "nutrition": {"calories": 140, "protein": 2, "carbs": 17, "fat": 7, "fiber": 0, "sugar": 16},
             "image": "🍦", "description": "Creamy vanilla ice cream"},
            
            # Canned Goods
            {"id": "beans_001", "name": "Black Beans", "category": "Canned", "price": 1.49,
             "nutrition": {"calories": 120, "protein": 8, "carbs": 22, "fat": 0.5, "fiber": 8, "sugar": 1},
             "image": "🫘", "description": "Nutritious black beans, ready to eat"},
            
            {"id": "tuna_001", "name": "Canned Tuna", "category": "Canned", "price": 2.49,
             "nutrition": {"calories": 100, "protein": 22, "carbs": 0, "fat": 1, "fiber": 0, "sugar": 0},
             "image": "🐟", "description": "Protein-rich canned tuna"},
            
            # Condiments & Spices
            {"id": "ketchup_001", "name": "Tomato Ketchup", "category": "Condiments", "price": 2.99,
             "nutrition": {"calories": 20, "protein": 0, "carbs": 5, "fat": 0, "fiber": 0, "sugar": 4},
             "image": "🍅", "description": "Classic tomato ketchup"},
            
            {"id": "mustard_001", "name": "Yellow Mustard", "category": "Condiments", "price": 1.99,
             "nutrition": {"calories": 5, "protein": 0, "carbs": 1, "fat": 0, "fiber": 0, "sugar": 0},
             "image": "🌶️", "description": "Tangy yellow mustard"},
            
            # Additional products to reach 50+
            {"id": "orange_001", "name": "Fresh Oranges", "category": "Fruits", "price": 3.99,
             "nutrition": {"calories": 62, "protein": 1.2, "carbs": 15, "fat": 0.2, "fiber": 3, "sugar": 12},
             "image": "🍊", "description": "Sweet and juicy oranges, rich in vitamin C"},
            
            {"id": "grapes_001", "name": "Red Grapes", "category": "Fruits", "price": 4.99,
             "nutrition": {"calories": 69, "protein": 0.7, "carbs": 18, "fat": 0.2, "fiber": 1, "sugar": 16},
             "image": "🍇", "description": "Sweet red grapes, perfect for snacking"},
            
            {"id": "broccoli_001", "name": "Fresh Broccoli", "category": "Vegetables", "price": 2.99,
             "nutrition": {"calories": 34, "protein": 2.8, "carbs": 7, "fat": 0.4, "fiber": 2, "sugar": 1},
             "image": "🥦", "description": "Nutritious broccoli, high in vitamins"},
            
            {"id": "spinach_001", "name": "Baby Spinach", "category": "Vegetables", "price": 3.49,
             "nutrition": {"calories": 23, "protein": 2.9, "carbs": 4, "fat": 0.4, "fiber": 2, "sugar": 1},
             "image": "🥬", "description": "Fresh baby spinach, perfect for salads"},
            
            {"id": "onion_001", "name": "Yellow Onions", "category": "Vegetables", "price": 1.99,
             "nutrition": {"calories": 40, "protein": 1.1, "carbs": 9, "fat": 0.1, "fiber": 2, "sugar": 4},
             "image": "🧅", "description": "Fresh yellow onions for cooking"},
            
            {"id": "garlic_001", "name": "Fresh Garlic", "category": "Vegetables", "price": 1.49,
             "nutrition": {"calories": 4, "protein": 0.2, "carbs": 1, "fat": 0, "fiber": 0, "sugar": 0},
             "image": "🧄", "description": "Fresh garlic cloves for flavoring"},
            
            {"id": "butter_001", "name": "Unsalted Butter", "category": "Dairy", "price": 4.99,
             "nutrition": {"calories": 102, "protein": 0.1, "carbs": 0, "fat": 12, "fiber": 0, "sugar": 0},
             "image": "🧈", "description": "Creamy unsalted butter for cooking"},
            
            {"id": "cream_001", "name": "Heavy Cream", "category": "Dairy", "price": 3.99,
             "nutrition": {"calories": 51, "protein": 0.4, "carbs": 0.4, "fat": 5.5, "fiber": 0, "sugar": 0.4},
             "image": "🥛", "description": "Rich heavy cream for cooking"},
            
            {"id": "pork_001", "name": "Pork Chops", "category": "Meat", "price": 7.99,
             "nutrition": {"calories": 231, "protein": 26, "carbs": 0, "fat": 14, "fiber": 0, "sugar": 0},
             "image": "🥩", "description": "Fresh pork chops, perfect for grilling"},
            
            {"id": "turkey_001", "name": "Ground Turkey", "category": "Meat", "price": 5.99,
             "nutrition": {"calories": 189, "protein": 22, "carbs": 0, "fat": 10, "fiber": 0, "sugar": 0},
             "image": "🦃", "description": "Lean ground turkey, healthy alternative"},
            
            {"id": "shrimp_001", "name": "Frozen Shrimp", "category": "Seafood", "price": 9.99,
             "nutrition": {"calories": 85, "protein": 20, "carbs": 0, "fat": 1, "fiber": 0, "sugar": 0},
             "image": "🦐", "description": "Frozen shrimp, ready to cook"},
            
            {"id": "quinoa_001", "name": "Organic Quinoa", "category": "Grains", "price": 5.99,
             "nutrition": {"calories": 120, "protein": 4.4, "carbs": 22, "fat": 1.9, "fiber": 2.8, "sugar": 0.9},
             "image": "🌾", "description": "Nutritious organic quinoa"},
            
            {"id": "oats_001", "name": "Steel Cut Oats", "category": "Grains", "price": 4.99,
             "nutrition": {"calories": 150, "protein": 5, "carbs": 27, "fat": 3, "fiber": 4, "sugar": 1},
             "image": "🌾", "description": "Heart-healthy steel cut oats"},
            
            {"id": "popcorn_001", "name": "Microwave Popcorn", "category": "Snacks", "price": 2.99,
             "nutrition": {"calories": 120, "protein": 3, "carbs": 20, "fat": 4, "fiber": 3, "sugar": 0},
             "image": "🍿", "description": "Light and fluffy microwave popcorn"},
            
            {"id": "nuts_001", "name": "Mixed Nuts", "category": "Snacks", "price": 6.99,
             "nutrition": {"calories": 170, "protein": 6, "carbs": 6, "fat": 15, "fiber": 3, "sugar": 2},
             "image": "🥜", "description": "Delicious mixed nuts, perfect for snacking"},
            
            {"id": "juice_001", "name": "Orange Juice", "category": "Beverages", "price": 3.99,
             "nutrition": {"calories": 110, "protein": 2, "carbs": 26, "fat": 0, "fiber": 0, "sugar": 22},
             "image": "🧃", "description": "Fresh squeezed orange juice"},
            
            {"id": "coffee_001", "name": "Ground Coffee", "category": "Beverages", "price": 8.99,
             "nutrition": {"calories": 2, "protein": 0.3, "carbs": 0, "fat": 0, "fiber": 0, "sugar": 0},
             "image": "☕", "description": "Premium ground coffee beans"},
            
            {"id": "fries_001", "name": "Frozen French Fries", "category": "Frozen", "price": 3.99,
             "nutrition": {"calories": 130, "protein": 2, "carbs": 18, "fat": 6, "fiber": 2, "sugar": 0},
             "image": "🍟", "description": "Crispy frozen french fries"},
            
            {"id": "corn_001", "name": "Frozen Corn", "category": "Frozen", "price": 2.99,
             "nutrition": {"calories": 88, "protein": 3, "carbs": 21, "fat": 1, "fiber": 3, "sugar": 3},
             "image": "🌽", "description": "Sweet frozen corn kernels"},
            
            {"id": "soup_001", "name": "Chicken Noodle Soup", "category": "Canned", "price": 2.99,
             "nutrition": {"calories": 90, "protein": 5, "carbs": 12, "fat": 3, "fiber": 1, "sugar": 2},
             "image": "🥣", "description": "Hearty chicken noodle soup"},
            
            {"id": "tomatoes_canned_001", "name": "Canned Tomatoes", "category": "Canned", "price": 1.99,
             "nutrition": {"calories": 32, "protein": 1.6, "carbs": 7, "fat": 0.4, "fiber": 2, "sugar": 4},
             "image": "🍅", "description": "Canned diced tomatoes for cooking"},
            
            {"id": "mayo_001", "name": "Mayonnaise", "category": "Condiments", "price": 3.99,
             "nutrition": {"calories": 90, "protein": 0, "carbs": 0, "fat": 10, "fiber": 0, "sugar": 0},
             "image": "🥄", "description": "Creamy mayonnaise for sandwiches"},
            
            {"id": "olive_oil_001", "name": "Extra Virgin Olive Oil", "category": "Condiments", "price": 7.99,
             "nutrition": {"calories": 120, "protein": 0, "carbs": 0, "fat": 14, "fiber": 0, "sugar": 0},
             "image": "🫒", "description": "Premium extra virgin olive oil"},
            
            {"id": "salt_001", "name": "Sea Salt", "category": "Condiments", "price": 2.99,
             "nutrition": {"calories": 0, "protein": 0, "carbs": 0, "fat": 0, "fiber": 0, "sugar": 0},
             "image": "🧂", "description": "Natural sea salt for seasoning"},
            
            {"id": "pepper_001", "name": "Black Pepper", "category": "Condiments", "price": 3.99,
             "nutrition": {"calories": 6, "protein": 0.3, "carbs": 1.5, "fat": 0.1, "fiber": 0.6, "sugar": 0.1},
             "image": "🌶️", "description": "Freshly ground black pepper"},
            
            {"id": "honey_001", "name": "Pure Honey", "category": "Condiments", "price": 5.99,
             "nutrition": {"calories": 64, "protein": 0.1, "carbs": 17, "fat": 0, "fiber": 0, "sugar": 17},
             "image": "🍯", "description": "Pure natural honey"},
            
            {"id": "jam_001", "name": "Strawberry Jam", "category": "Condiments", "price": 3.99,
             "nutrition": {"calories": 50, "protein": 0, "carbs": 13, "fat": 0, "fiber": 0, "sugar": 12},
             "image": "🍓", "description": "Sweet strawberry jam"},
            
            {"id": "vinegar_001", "name": "Balsamic Vinegar", "category": "Condiments", "price": 6.99,
             "nutrition": {"calories": 14, "protein": 0, "carbs": 3, "fat": 0, "fiber": 0, "sugar": 3},
             "image": "🍷", "description": "Aged balsamic vinegar for salads"},
            
            {"id": "sauce_001", "name": "Soy Sauce", "category": "Condiments", "price": 2.99,
             "nutrition": {"calories": 8, "protein": 1, "carbs": 1, "fat": 0, "fiber": 0, "sugar": 0},
             "image": "🍶", "description": "Traditional soy sauce for Asian cooking"},
            
            {"id": "salsa_001", "name": "Fresh Salsa", "category": "Condiments", "price": 3.99,
             "nutrition": {"calories": 20, "protein": 1, "carbs": 4, "fat": 0, "fiber": 1, "sugar": 2},
             "image": "🌶️", "description": "Fresh and spicy salsa"},
            
            {"id": "hot_sauce_001", "name": "Hot Sauce", "category": "Condiments", "price": 2.99,
             "nutrition": {"calories": 5, "protein": 0, "carbs": 1, "fat": 0, "fiber": 0, "sugar": 0},
             "image": "🌶️", "description": "Spicy hot sauce for extra flavor"},
        ]
        return products
    
    def get_all_products(self) -> List[Dict[str, Any]]:
        """Get all products"""
        return self.products
    
    def search_products(self, query: str) -> List[Dict[str, Any]]:
        """Search products by name or category"""
        query = query.lower()
        results = []
        for product in self.products:
            if (query in product["name"].lower() or 
                query in product["category"].lower() or
                query in product["description"].lower()):
                results.append(product)
        return results
    
    def get_product_by_id(self, product_id: str) -> Dict[str, Any]:
        """Get product by ID"""
        for product in self.products:
            if product["id"] == product_id:
                return product
        return None 