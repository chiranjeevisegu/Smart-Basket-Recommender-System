from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import google.generativeai as genai
import json
import os
from dotenv import load_dotenv
from recommendation_engine import RecommendationEngine
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

# Initialize recommendation engine and product catalog
recommendation_engine = RecommendationEngine()
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
        recommendations = recommendation_engine.get_recommendations(request.cart_items)
        nutrition_info = recommendation_engine.calculate_nutrition(request.cart_items)
        bundle_discounts = recommendation_engine.find_bundle_discounts(request.cart_items)
        health_warnings = recommendation_engine.check_health_warnings(request.cart_items)
        
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 