# 🛒 Smart Basket Recommender System

A real-time AI-powered supermarket recommendation system that enhances the shopping experience with intelligent product suggestions, comprehensive nutrition tracking, and dynamic shopping tips.

## ✨ Features Overview

This system is designed to provide a seamless and smart grocery shopping experience with its core functionalities and a user-friendly interface.

### 🎯 Core Functionalities

*   **Real-time Product Recommendations**: Get instant, personalized product suggestions as you add items to your shopping cart. This ensures you never miss out on complementary items or popular choices.
*   **Dynamic Shopping Tips**: Receive helpful, context-aware tips based on your current basket. These tips can guide you towards healthier choices, bundle deals, or simply remind you of common grocery additions.
*   **Intelligent Basket Analysis**: The system employs sophisticated algorithms including collaborative filtering (for broader suggestions based on similar user habits) and semantic similarity (for product suggestions based on descriptions) to offer highly relevant recommendations.
*   **Comprehensive Nutrition Tracking**: Monitor your basket's nutritional content in real-time. The system calculates total calories, protein, carbs, fats, fiber, and sugar, helping you make informed dietary decisions.
*   **Automatic Bundle Discounts Detection**: Discover popular product combinations and receive alerts for potential discounts when you have 2 or more items that belong to a recognized bundle.
*   **Health Warnings**: Get alerted to potentially unhealthy combinations or excessive amounts of certain nutrients (e.g., too much sugar, high fat) based on your cart contents, promoting healthier shopping habits.
*   **Interactive Checkout Summary**: A dedicated checkout page provides a detailed bill summary and a comprehensive nutritional breakdown of your entire basket.

### 🎨 User Interface (UI) Highlights

*   **Clean and Modern Design**: Features a visually appealing aesthetic with smooth gradients, intuitive layouts, and an easy-to-navigate interface.
*   **Responsive Layout**: Optimized to provide a consistent and enjoyable experience across various devices, including desktops, tablets, and mobile phones.
*   **Real-time Updates**: The UI dynamically updates suggestions, totals, and tips instantly as you interact with your cart.
*   **Interactive Elements**: Engaging user experience with subtle hover effects, smooth transitions, and clear calls to action.

### 🛠️ Technology Stack

This project is built using a modern full-stack approach, leveraging popular and robust technologies:

#### Backend (Python)
*   **FastAPI**: A high-performance, easy-to-use Python web framework for building robust APIs.
*   **Google Generative AI (Gemini Pro)**: Utilized for advanced natural language understanding to provide smart chatbot responses for recipe suggestions, alternatives, and shopping advice.
*   **spaCy (or simpler alternatives)**: For natural language processing (NLP) tasks, specifically for semantic similarity between product descriptions (though a simpler version is provided for ease of setup).
*   **Sentence Transformers**: Used to generate dense vector embeddings from product descriptions, enabling semantic similarity calculations.
*   **scikit-learn**: A popular machine learning library for implementing collaborative filtering algorithms.
*   **Pandas & NumPy**: Essential libraries for data manipulation and numerical operations, especially for managing the product catalog and user basket data.
*   **python-dotenv**: For managing environment variables, such as API keys.
*   **fastapi-cors**: Middleware for handling Cross-Origin Resource Sharing.

#### Frontend (React.js)
*   **React**: A declarative, component-based JavaScript library for building user interfaces.
*   **Framer Motion**: A production-ready motion library for React, used to create fluid animations and transitions throughout the UI.
*   **Axios**: A promise-based HTTP client for making API requests to the backend.
*   **React Icons (Feather Icons)**: A library providing a wide range of customizable SVG icons.
*   **CSS3**: Modern styling techniques including Flexbox, Grid, and responsive design principles for a dynamic and adaptive layout.

## 🚀 Getting Started

Follow these steps to set up and run the Smart Basket Recommender system on your local machine.

### Prerequisites

Before you begin, ensure you have the following installed:

*   **Python 3.8+**: Download from [python.org](https://www.python.org/downloads/)
    *   Verify installation: `python --version`
*   **Node.js 16+**: Download from [nodejs.org](https://nodejs.org/en/download/) (comes with npm)
    *   Verify installation: `node --version` and `npm --version`

### 📦 Backend Setup

1.  **Navigate to the project root:**
    ```bash
    cd C:\Users\venka\OneDrive\Desktop\realtime
    ```
2.  **Install Python dependencies (simplified for quick start):**
    ```bash
    pip install -r requirements_simple.txt
    ```
    *Note: The `requirements.txt` includes spaCy and Sentence Transformers, which might require additional build tools on Windows. `requirements_simple.txt` removes these for a faster setup.*
3.  **Start the Backend Server:**
    ```bash
    python backend/main_basic.py
    ```
    *   The API will be available at: `http://localhost:8000`
    *   API documentation (Swagger UI) at: `http://localhost:8000/docs`
    *   Keep this terminal window open; the server needs to run continuously.

### 🌐 Frontend Setup

1.  **Open a NEW Terminal/Command Prompt window.**
2.  **Navigate to the `frontend` directory:**
    ```bash
    cd C:\Users\venka\OneDrive\Desktop\realtime\frontend
    ```
3.  **Install Node.js dependencies:**
    ```bash
    npm install
    ```
4.  **Start the React Development Server:**
    ```bash
    npm start
    ```
    *   The application will automatically open in your browser at: `http://localhost:3000`
    *   Keep this terminal window open as well.

### 🧪 Test the System (Optional)

You can run a Python script to test the backend API endpoints:

```bash
python demo.py
```
This script will check API health, list products, test search, and verify recommendations and chatbot interaction.

## 📁 Project Structure

```
realtime/
├── backend/                        # Backend FastAPI application
│   ├── main.py                     # Main FastAPI application (full version with spaCy)
│   ├── main_basic.py               # Simplified backend (without spaCy/Sentence Transformers)
│   ├── product_catalog.py          # Manages the dummy product database
│   └── recommendation_engine.py    # (Full version) AI recommendation algorithms
├── frontend/                       # React.js client-side application
│   ├── public/                     # Public assets
│   │   └── index.html              # Main HTML file for the React app
│   ├── src/                        # Source code for the React app
│   │   ├── App.js                  # Main React component, UI logic, API calls
│   │   ├── App.css                 # Styling for the React components
│   │   ├── index.js                # React application entry point
│   │   └── index.css               # Base CSS styles
│   └── package.json                # Frontend dependencies and scripts
├── requirements.txt                # Python dependencies for the full backend
├── requirements_simple.txt         # Python dependencies for the basic backend
├── start_backend.py                # Python script to start the backend (handles setup)
├── start_frontend.bat              # Windows batch script to start the frontend
├── start_frontend.sh               # Unix/Linux shell script to start the frontend
├── demo.py                         # Python script to demonstrate backend API functionality
└── README.md                       # Project documentation (this file)
```

## 🔧 API Endpoints

The backend API runs on `http://localhost:8000`.

### `GET /`
*   **Description**: Checks if the API is running.
*   **Response**: `{"message": "Smart Basket Recommender API"}`

### `GET /products`
*   **Description**: Retrieves a list of all available products from the catalog.
*   **Response**: `{"products": [...]}` (list of product objects)

### `GET /search?query={search_term}`
*   **Description**: Searches for products by name or category based on the provided query.
*   **Query Parameter**: `query` (string) - The search term.
*   **Response**: `{"products": [...]}` (list of matching product objects)

### `POST /recommend`
*   **Description**: Provides real-time product recommendations, nutrition information, bundle discounts, and health warnings based on the current items in the cart.
*   **Request Body**:
    ```json
    {
      "cart_items": [
        {
          "id": "string",
          "name": "string",
          "category": "string",
          "price": float,
          "quantity": int
        }
      ]
    }
    ```
*   **Response**:
    ```