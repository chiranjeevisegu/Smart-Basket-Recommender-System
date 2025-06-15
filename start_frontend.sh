#!/bin/bash

echo "🛒 Smart Basket Recommender - Frontend Setup"
echo "================================================"

echo "📦 Installing Node.js dependencies..."
cd frontend

if ! npm install; then
    echo "❌ Error installing dependencies. Please check your Node.js installation."
    exit 1
fi

echo "✅ Dependencies installed successfully"
echo "🚀 Starting React development server..."
echo "📍 App will be available at: http://localhost:3000"
echo "🔄 Press Ctrl+C to stop the server"
echo "----------------------------------------"

npm start 