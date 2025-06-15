from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import urllib.parse
from product_catalog import ProductCatalog
import google.generativeai as genai

# Initialize Google Generative AI
genai.configure(api_key="AIzaSyCbWtjx2aaFYixR5QMG_93Bxf_pRlW74xk")
model = genai.GenerativeModel('gemini-pro')

# Initialize product catalog
product_catalog = ProductCatalog()

class SmartBasketHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Handle GET requests"""
        parsed_path = urllib.parse.urlparse(self.path)
        
        if parsed_path.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            response = {"message": "Smart Basket Recommender API"}
            self.wfile.write(json.dumps(response).encode())
            
        elif parsed_path.path == '/products':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            response = {"products": product_catalog.get_all_products()}
            self.wfile.write(json.dumps(response).encode())
            
        elif parsed_path.path.startswith('/search'):
            query_params = urllib.parse.parse_qs(parsed_path.query)
            query = query_params.get('query', [''])[0]
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            results = product_catalog.search_products(query)
            response = {"products": results}
            self.wfile.write(json.dumps(response).encode())
            
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        """Handle POST requests"""
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        if self.path == '/recommend':
            try:
                data = json.loads(post_data.decode('utf-8'))
                cart_items = data.get('cart_items', [])
                
                # Simple recommendation logic
                recommendations = self.get_simple_recommendations(cart_items)
                nutrition_info = self.calculate_nutrition(cart_items)
                bundle_discounts = self.find_bundle_discounts(cart_items)
                health_warnings = self.check_health_warnings(cart_items)
                
                response = {
                    "recommendations": recommendations,
                    "nutrition_info": nutrition_info,
                    "bundle_discounts": bundle_discounts,
                    "health_warnings": health_warnings
                }
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(response).encode())
                
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                error_response = {"error": str(e)}
                self.wfile.write(json.dumps(error_response).encode())
                
        elif self.path == '/chatbot':
            try:
                data = json.loads(post_data.decode('utf-8'))
                message = data.get('message', '')
                cart_items = data.get('cart_items', [])
                
                # Format cart items for the AI
                if cart_items:
                    cart_summary = "\n".join([f"- {item['name']} ({item['category']})" for item in cart_items])
                else:
                    cart_summary = "Your cart is currently empty."
                
                prompt = f"""
                You are a helpful and friendly supermarket shopping assistant. The user has the following items in their cart:
                
                {cart_summary}
                
                User message: "{message}"
                
                Please provide helpful, specific, and friendly advice related to their cart and request. 
                
                If they ask for recipes, suggest simple, delicious recipes using their items.
                If they ask for alternatives, suggest specific healthy or budget-friendly alternatives.
                If they ask for side dishes, suggest complementary items that would go well with their cart.
                If they ask about health, provide nutritional advice.
                
                Keep responses concise (2-3 sentences), practical, and encouraging. Be friendly and helpful!
                """
                
                try:
                    ai_response = model.generate_content(prompt)
                    bot_response = ai_response.text
                except Exception as ai_error:
                    # Fallback responses if AI fails
                    fallback_responses = {
                        "suggest a side dish": "Based on your cart, I'd recommend adding some fresh vegetables like broccoli or a side salad. These would complement your items perfectly!",
                        "add vegan alternatives": "Great choice! I can suggest some vegan alternatives. For dairy products, try almond milk or coconut yogurt. For meat, consider tofu or tempeh.",
                        "make a recipe": "I'd love to help you create a recipe! With your current items, you could make a delicious stir-fry, salad, or pasta dish. What type of cuisine are you in the mood for?",
                        "health": "Your cart looks great! Remember to include plenty of colorful vegetables and whole grains for a balanced diet.",
                        "budget": "Great shopping! To save money, consider buying seasonal produce and looking for store brand alternatives."
                    }
                    
                    message_lower = message.lower()
                    for key, response in fallback_responses.items():
                        if key in message_lower:
                            bot_response = response
                            break
                    else:
                        bot_response = "I'm here to help with your shopping! I can suggest recipes, alternatives, side dishes, and provide health tips. What would you like to know?"
                
                response = {"response": bot_response}
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(response).encode())
                
            except Exception as e:
                print(f"Chatbot error: {e}")
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                error_response = {"response": "I'm having trouble connecting right now, but I'm here to help! Try asking me about recipes, alternatives, or shopping tips."}
                self.wfile.write(json.dumps(error_response).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def get_simple_recommendations(self, cart_items):
        """Simple recommendation logic"""
        if not cart_items:
            return self.get_popular_items()
        
        cart_categories = [item['category'] for item in cart_items]
        all_products = product_catalog.get_all_products()
        
        # Get products from related categories
        related_categories = {
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
        
        recommendations = []
        cart_product_names = [item['name'] for item in cart_items]
        
        for category in cart_categories:
            if category in related_categories:
                for related_cat in related_categories[category]:
                    for product in all_products:
                        if (product["category"] == related_cat and 
                            product["name"] not in cart_product_names and
                            product not in recommendations):
                            recommendations.append(product)
                            if len(recommendations) >= 5:
                                return recommendations
        
        return recommendations[:5]
    
    def get_popular_items(self):
        """Get popular items when cart is empty"""
        popular_names = [
            "Fresh Red Apples", "Organic Bananas", "Whole Milk", 
            "Chicken Breast", "Fresh Tomatoes", "Whole Wheat Bread"
        ]
        
        all_products = product_catalog.get_all_products()
        recommendations = []
        
        for name in popular_names:
            for product in all_products:
                if product["name"] == name:
                    recommendations.append(product)
                    break
        
        return recommendations[:5]
    
    def calculate_nutrition(self, cart_items):
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
    
    def find_bundle_discounts(self, cart_items):
        """Find available bundle discounts"""
        popular_bundles = [
            ["Fresh Red Apples", "Organic Bananas", "Fresh Oranges"],
            ["Chicken Breast", "Brown Rice", "Fresh Broccoli"],
            ["Whole Milk", "Cheddar Cheese", "Large Eggs"],
            ["Ground Beef", "Spaghetti", "Canned Tomatoes"],
            ["Fresh Tomatoes", "Iceberg Lettuce", "Baby Carrots"]
        ]
        
        cart_product_names = [item['name'] for item in cart_items]
        available_bundles = []
        
        for bundle in popular_bundles:
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
    
    def check_health_warnings(self, cart_items):
        """Check for health warnings based on cart items"""
        warnings = []
        cart_product_names = [item['name'] for item in cart_items]
        
        high_sugar_items = ["Chocolate Chip Cookies", "Cola", "Orange Juice", "Strawberry Jam", "Vanilla Ice Cream"]
        high_sodium_items = ["Potato Chips", "Canned Tuna", "Canned Tomatoes", "Soy Sauce"]
        high_fat_items = ["Ground Beef", "Pork Chops", "Mayonnaise", "Extra Virgin Olive Oil"]
        
        # Check for high sugar items
        high_sugar_in_cart = [item for item in cart_product_names if item in high_sugar_items]
        if len(high_sugar_in_cart) >= 2:
            warnings.append(f"⚠️ High sugar content detected: {', '.join(high_sugar_in_cart)}")
        
        # Check for high sodium items
        high_sodium_in_cart = [item for item in cart_product_names if item in high_sodium_items]
        if len(high_sodium_in_cart) >= 2:
            warnings.append(f"⚠️ High sodium content detected: {', '.join(high_sodium_in_cart)}")
        
        # Check for high fat items
        high_fat_in_cart = [item for item in cart_product_names if item in high_fat_items]
        if len(high_fat_in_cart) >= 2:
            warnings.append(f"⚠️ High fat content detected: {', '.join(high_fat_in_cart)}")
        
        return warnings

def run_server():
    """Start the HTTP server"""
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, SmartBasketHandler)
    print("🚀 Starting Smart Basket Recommender (Basic Version)")
    print("📍 Server will be available at: http://localhost:8000")
    print("📚 API documentation at: http://localhost:8000/docs")
    print("🔄 Press Ctrl+C to stop the server")
    print("-" * 50)
    httpd.serve_forever()

if __name__ == "__main__":
    run_server() 