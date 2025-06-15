#!/usr/bin/env python3
"""
Smart Basket Recommender - Demo Script
Tests the recommendation system and chatbot functionality
"""

import requests
import json
import time

# API base URL
BASE_URL = "http://localhost:8000"

def test_api_health():
    """Test if the API is running"""
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"✅ API Health Check: {response.json()}")
        return True
    except requests.exceptions.ConnectionError:
        print("❌ API is not running. Please start the backend server first.")
        return False

def test_products():
    """Test getting all products"""
    try:
        response = requests.get(f"{BASE_URL}/products")
        products = response.json()["products"]
        print(f"✅ Found {len(products)} products in catalog")
        return products
    except Exception as e:
        print(f"❌ Error getting products: {e}")
        return []

def test_search():
    """Test product search"""
    try:
        response = requests.get(f"{BASE_URL}/search?query=apple")
        results = response.json()["products"]
        print(f"✅ Search for 'apple' found {len(results)} results")
        for product in results[:3]:
            print(f"   - {product['name']} (${product['price']})")
        return results
    except Exception as e:
        print(f"❌ Error searching products: {e}")
        return []

def test_recommendations():
    """Test recommendation system"""
    # Sample cart with some items
    cart_items = [
        {
            "id": "apple_001",
            "name": "Fresh Red Apples",
            "category": "Fruits",
            "price": 2.99,
            "quantity": 2
        },
        {
            "id": "chicken_001",
            "name": "Chicken Breast",
            "category": "Meat",
            "price": 8.99,
            "quantity": 1
        }
    ]
    
    try:
        response = requests.post(f"{BASE_URL}/recommend", json={"cart_items": cart_items})
        data = response.json()
        
        print(f"✅ Got {len(data['recommendations'])} recommendations")
        print(f"📊 Nutrition: {data['nutrition_info']['calories']} calories")
        print(f"🎁 Bundle discounts: {len(data['bundle_discounts'])} available")
        print(f"⚠️ Health warnings: {len(data['health_warnings'])} found")
        
        # Show top recommendations
        print("\nTop recommendations:")
        for i, rec in enumerate(data['recommendations'][:3], 1):
            print(f"   {i}. {rec['name']} - ${rec['price']}")
        
        return data
    except Exception as e:
        print(f"❌ Error getting recommendations: {e}")
        return None

def test_chatbot():
    """Test chatbot functionality"""
    cart_items = [
        {
            "id": "apple_001",
            "name": "Fresh Red Apples",
            "category": "Fruits",
            "price": 2.99,
            "quantity": 2
        }
    ]
    
    test_messages = [
        "Suggest a side dish for my basket",
        "Add vegan alternatives",
        "Make a recipe with these items"
    ]
    
    for message in test_messages:
        try:
            print(f"\n🤖 Testing chatbot with: '{message}'")
            response = requests.post(f"{BASE_URL}/chatbot", json={
                "message": message,
                "cart_items": cart_items
            })
            
            bot_response = response.json()["response"]
            print(f"💬 Bot response: {bot_response[:100]}...")
            time.sleep(1)  # Small delay between requests
            
        except Exception as e:
            print(f"❌ Error testing chatbot: {e}")

def main():
    """Run all demo tests"""
    print("🛒 Smart Basket Recommender - Demo")
    print("=" * 50)
    
    # Test API health
    if not test_api_health():
        return
    
    print("\n" + "=" * 50)
    
    # Test products
    products = test_products()
    
    print("\n" + "=" * 50)
    
    # Test search
    test_search()
    
    print("\n" + "=" * 50)
    
    # Test recommendations
    test_recommendations()
    
    print("\n" + "=" * 50)
    
    # Test chatbot
    test_chatbot()
    
    print("\n" + "=" * 50)
    print("🎉 Demo completed successfully!")
    print("🌐 Open http://localhost:3000 to use the web interface")

if __name__ == "__main__":
    main() 