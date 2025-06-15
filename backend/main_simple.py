from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import google.generativeai as genai
import json
import os
from dotenv import load_dotenv
from product_catalog import ProductCatalog

load_dotenv()

app = FastAPI(title="Smart Basket Recommender", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Google Generative AI
genai.configure(api_key="AIzaSyCbWtjx2aaFYixR5QMG_93Bxf_pRlW74xk")
model = genai.GenerativeModel('gemini-pro')

# Initialize product catalog
product_catalog = ProductCatalog()

class CartItem(BaseModel):
    id: str
    name: str
    category: str
    price: float
    quantity: int = 1

class ChatMessage(BaseModel):
    message: str
    cart_items: List[CartItem]

class RecommendationRequest(BaseModel):
    cart_items: List[CartItem]

class RecommendationResponse(BaseModel):
    recommendations: List[Dict[str, Any]]
    nutrition_info: Dict[str, Any]
    bundle_discounts: List[Dict[str, Any]]
    health_warnings: List[str]

@app.get("/")
async def root():
    return {"message": "Smart Basket Recommender API"}

@app.get("/products")
async def get_products():
    """Get all available products"""
    return {"products": product_catalog.get_all_products()}

@app.post("/recommend", response_model=RecommendationResponse)
async def get_recommendations(request: RecommendationRequest):
    """Get recommendations based on cart items"""
    try:
        # Simple recommendation logic without spaCy
        recommendations = get_simple_recommendations(request.cart_items)
        nutrition_info = calculate_nutrition(request.cart_items)
        bundle_discounts = find_bundle_discounts(request.cart_items)
        health_warnings = check_health_warnings(request.cart_items)
        
        return RecommendationResponse(
            recommendations=recommendations,
            nutrition_info=nutrition_info,
            bundle_discounts=bundle_discounts,
            health_warnings=health_warnings
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chatbot")
async def chat_with_bot(chat_message: ChatMessage):
    """Chat with the AI assistant"""
    try:
        # Format cart items for the AI
        cart_summary = "\n".join([f"- {item.name} ({item.category})" for item in chat_message.cart_items])
        
        prompt = f"""
        You are a helpful supermarket assistant. The user has the following items in their cart:
        
        {cart_summary}
        
        User message: {chat_message.message}
        
        Please provide helpful, specific advice related to their cart and request. 
        If they ask for recipes, suggest simple recipes using their items.
        If they ask for alternatives, suggest specific products.
        Keep responses concise and practical.
        """
        
        response = model.generate_content(prompt)
        return {"response": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/search")
async def search_products(query: str):
    """Search products by name or category"""
    results = product_catalog.search_products(query)
    return {"products": results}

# Simple recommendation functions (without spaCy)
def get_simple_recommendations(cart_items: List[CartItem]) -> List[Dict[str, Any]]:
    """Simple recommendation logic"""
    if not cart_items:
        return get_popular_items()
    
    cart_categories = [item.category for item in cart_items]
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
    cart_product_names = [item.name for item in cart_items]
    
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

def get_popular_items() -> List[Dict[str, Any]]:
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

def calculate_nutrition(cart_items: List[CartItem]) -> Dict[str, Any]:
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

def find_bundle_discounts(cart_items: List[CartItem]) -> List[Dict[str, Any]]:
    """Find available bundle discounts"""
    popular_bundles = [
        ["Fresh Red Apples", "Organic Bananas", "Fresh Oranges"],
        ["Chicken Breast", "Brown Rice", "Fresh Broccoli"],
        ["Whole Milk", "Cheddar Cheese", "Large Eggs"],
        ["Ground Beef", "Spaghetti", "Canned Tomatoes"],
        ["Fresh Tomatoes", "Iceberg Lettuce", "Baby Carrots"]
    ]
    
    cart_product_names = [item.name for item in cart_items]
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

def check_health_warnings(cart_items: List[CartItem]) -> List[str]:
    """Check for health warnings based on cart items"""
    warnings = []
    cart_product_names = [item.name for item in cart_items]
    
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

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Smart Basket Recommender (Simple Version)")
    print("📍 Server will be available at: http://localhost:8000")
    print("📚 API documentation at: http://localhost:8000/docs")
    print("🔄 Press Ctrl+C to stop the server")
    print("-" * 50)
    uvicorn.run(app, host="0.0.0.0", port=8000) 