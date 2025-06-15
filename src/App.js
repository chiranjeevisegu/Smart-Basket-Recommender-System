import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { motion, AnimatePresence } from 'framer-motion';
import { FiShoppingCart, FiSearch, FiPlus, FiTrash2, FiGift, FiAlertTriangle, FiFileText, FiInfo } from 'react-icons/fi';
import './App.css';

function getTotalNutrition(cart) {
  return cart.reduce((total, item) => {
    const nutrition = item.nutrition || {};
    const quantity = item.quantity || 1;
    return {
      calories: total.calories + (nutrition.calories || 0) * quantity,
      protein: total.protein + (nutrition.protein || 0) * quantity,
      carbs: total.carbs + (nutrition.carbs || 0) * quantity,
      fat: total.fat + (nutrition.fat || 0) * quantity,
      fiber: total.fiber + (nutrition.fiber || 0) * quantity,
      sugar: total.sugar + (nutrition.sugar || 0) * quantity
    };
  }, { calories: 0, protein: 0, carbs: 0, fat: 0, fiber: 0, sugar: 0 });
}

function getShoppingTips(cart) {
  if (cart.length === 0) {
    return [
      "Start by searching for your favorite groceries!",
      "Add fresh fruits and vegetables for a healthy basket.",
      "Look for bundle discounts as you add more items."
    ];
  }
  const tips = [];
  const categories = cart.map(item => item.category);
  if (!categories.includes('Fruits')) tips.push("Add some fruits for vitamins and fiber.");
  if (!categories.includes('Vegetables')) tips.push("Vegetables add color and nutrition to your meals.");
  if (cart.some(item => item.category === 'Snacks')) tips.push("Balance snacks with healthy options like nuts or yogurt.");
  if (cart.length > 5) tips.push("You have a full basket! Check for bundle discounts.");
  if (cart.reduce((sum, item) => sum + (item.nutrition?.sugar || 0) * item.quantity, 0) > 50) tips.push("Watch out for high sugar content.");
  if (cart.reduce((sum, item) => sum + (item.nutrition?.calories || 0) * item.quantity, 0) > 2000) tips.push("High calorie intake detected. Consider lighter options.");
  if (tips.length === 0) tips.push("Great basket! You're making smart choices.");
  return tips;
}

function App() {
  const [cart, setCart] = useState([]);
  const [recommendations, setRecommendations] = useState([]);
  const [nutritionInfo, setNutritionInfo] = useState({});
  const [bundleDiscounts, setBundleDiscounts] = useState([]);
  const [healthWarnings, setHealthWarnings] = useState([]);
  const [products, setProducts] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [showCheckout, setShowCheckout] = useState(false);

  useEffect(() => {
    fetchProducts();
  }, []);

  useEffect(() => {
    if (cart.length > 0) {
      fetchRecommendations();
    } else {
      setRecommendations([]);
      setNutritionInfo({});
      setBundleDiscounts([]);
      setHealthWarnings([]);
    }
  }, [cart]);

  const fetchProducts = async () => {
    try {
      const response = await axios.get('/products');
      setProducts(response.data.products);
    } catch (error) {
      console.error('Error fetching products:', error);
    }
  };

  const fetchRecommendations = async () => {
    try {
      setIsLoading(true);
      const response = await axios.post('/recommend', {
        cart_items: cart
      });
      setRecommendations(response.data.recommendations);
      setNutritionInfo(response.data.nutrition_info);
      setBundleDiscounts(response.data.bundle_discounts);
      setHealthWarnings(response.data.health_warnings);
    } catch (error) {
      console.error('Error fetching recommendations:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const searchProducts = async (query) => {
    if (query.trim() === '') {
      setSearchResults([]);
      return;
    }
    try {
      const response = await axios.get(`/search?query=${encodeURIComponent(query)}`);
      setSearchResults(response.data.products);
    } catch (error) {
      console.error('Error searching products:', error);
    }
  };

  const addToCart = (product) => {
    const existingItem = cart.find(item => item.id === product.id);
    if (existingItem) {
      setCart(cart.map(item =>
        item.id === product.id
          ? { ...item, quantity: item.quantity + 1 }
          : item
      ));
    } else {
      setCart([...cart, { ...product, quantity: 1 }]);
    }
    setSearchResults([]);
    setSearchQuery('');
  };

  const removeFromCart = (productId) => {
    setCart(cart.filter(item => item.id !== productId));
  };

  const updateQuantity = (productId, newQuantity) => {
    if (newQuantity <= 0) {
      removeFromCart(productId);
      return;
    }
    setCart(cart.map(item =>
      item.id === productId
        ? { ...item, quantity: newQuantity }
        : item
    ));
  };

  const getTotalPrice = () => {
    return cart.reduce((total, item) => total + (item.price * item.quantity), 0);
  };

  const getTotalCalories = () => {
    return cart.reduce((total, item) => {
      const calories = item.nutrition?.calories || 0;
      return total + (calories * item.quantity);
    }, 0);
  };

  const handleCheckout = () => {
    setShowCheckout(true);
  };

  const handleBackToCart = () => {
    setShowCheckout(false);
  };

  const handleClearCart = () => {
    setCart([]);
    setShowCheckout(false);
  };

  // Checkout Page Component
  const CheckoutPage = () => {
    const totalNutrition = getTotalNutrition(cart);
    const totalPrice = getTotalPrice();
    const tax = totalPrice * 0.08; // 8% tax
    const finalTotal = totalPrice + tax;

    return (
      <motion.div 
        className="checkout-page"
        initial={{ opacity: 0, x: 100 }}
        animate={{ opacity: 1, x: 0 }}
        exit={{ opacity: 0, x: -100 }}
      >
        <div className="checkout-header">
          <button onClick={handleBackToCart} className="back-btn">
            Back to Cart
          </button>
          <h1>Checkout</h1>
        </div>

        <div className="checkout-content">
          <div className="bill-section">
            <h2>📋 Bill Summary</h2>
            <div className="bill-items">
              {cart.map((item, index) => (
                <motion.div 
                  key={item.id} 
                  className="bill-item"
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.1 }}
                >
                  <div className="bill-item-info">
                    <span className="bill-item-emoji">{item.image}</span>
                    <div>
                      <h4>{item.name}</h4>
                      <p>Qty: {item.quantity} × ${item.price}</p>
                    </div>
                  </div>
                  <span className="bill-item-total">${(item.price * item.quantity).toFixed(2)}</span>
                </motion.div>
              ))}
            </div>

            <div className="bill-summary">
              <div className="summary-row">
                <span>Subtotal:</span>
                <span>${totalPrice.toFixed(2)}</span>
              </div>
              <div className="summary-row">
                <span>Tax (8%):</span>
                <span>${tax.toFixed(2)}</span>
              </div>
              <div className="summary-row total">
                <span>Total:</span>
                <span>${finalTotal.toFixed(2)}</span>
              </div>
            </div>
          </div>

          <div className="nutrition-section">
            <h2>🍎 Nutrition Summary</h2>
            <div className="nutrition-grid">
              <div className="nutrition-card">
                <h3>🔥 Calories</h3>
                <p className="nutrition-value">{totalNutrition.calories}</p>
                <p className="nutrition-label">kcal</p>
              </div>
              <div className="nutrition-card">
                <h3>💪 Protein</h3>
                <p className="nutrition-value">{totalNutrition.protein.toFixed(1)}</p>
                <p className="nutrition-label">g</p>
              </div>
              <div className="nutrition-card">
                <h3>🌾 Carbs</h3>
                <p className="nutrition-value">{totalNutrition.carbs.toFixed(1)}</p>
                <p className="nutrition-label">g</p>
              </div>
              <div className="nutrition-card">
                <h3>🥑 Fat</h3>
                <p className="nutrition-value">{totalNutrition.fat.toFixed(1)}</p>
                <p className="nutrition-label">g</p>
              </div>
              <div className="nutrition-card">
                <h3>🌿 Fiber</h3>
                <p className="nutrition-value">{totalNutrition.fiber.toFixed(1)}</p>
                <p className="nutrition-label">g</p>
              </div>
              <div className="nutrition-card">
                <h3>🍯 Sugar</h3>
                <p className="nutrition-value">{totalNutrition.sugar.toFixed(1)}</p>
                <p className="nutrition-label">g</p>
              </div>
            </div>

            <div className="health-insights">
              <h3>💡 Health Insights</h3>
              {totalNutrition.calories > 2000 && (
                <p className="health-warning">⚠️ High calorie intake detected</p>
              )}
              {totalNutrition.sugar > 50 && (
                <p className="health-warning">⚠️ High sugar content</p>
              )}
              {totalNutrition.fiber < 25 && (
                <p className="health-tip">💡 Consider adding more fiber-rich foods</p>
              )}
              {totalNutrition.protein > 100 && (
                <p className="health-tip">✅ Good protein intake!</p>
              )}
            </div>
          </div>
        </div>

        <div className="checkout-actions">
          <button onClick={handleClearCart} className="clear-cart-btn">
            Clear Cart
          </button>
          <button className="pay-btn">
            💳 Pay ${finalTotal.toFixed(2)}
          </button>
        </div>
      </motion.div>
    );
  };

  // Main App Component
  if (showCheckout) {
    return <CheckoutPage />;
  }

  return (
    <div className="app">
      <header className="header">
        <h1>🛒 Smart Basket Recommender</h1>
        <div className="header-stats">
          <span>Items: {cart.length}</span>
          <span>Total: ${getTotalPrice().toFixed(2)}</span>
          <span>Calories: {getTotalCalories()}</span>
        </div>
      </header>

      <div className="main-container">
        {/* Left Panel - Smart Shopping Tips */}
        <motion.div 
          className="tips-panel"
          initial={{ x: -300 }}
          animate={{ x: 0 }}
        >
          <div className="tips-header">
            <FiInfo />
            <span>Smart Shopping Tips</span>
          </div>
          <div className="tips-content">
            {getShoppingTips(cart).map((tip, idx) => (
              <div className="tip-item" key={idx}>
                <FiInfo className="tip-icon" /> {tip}
              </div>
            ))}
          </div>
        </motion.div>

        {/* Center Panel - Search and Recommendations */}
        <div className="center-panel">
          {/* Search Bar */}
          <div className="search-container">
            <div className="search-bar">
              <FiSearch className="search-icon" />
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => {
                  setSearchQuery(e.target.value);
                  searchProducts(e.target.value);
                }}
                placeholder="Search for products..."
                className="search-input"
              />
            </div>
            
            {searchResults.length > 0 && (
              <motion.div 
                className="search-results"
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
              >
                {searchResults.map(product => (
                  <motion.div
                    key={product.id}
                    className="search-result-item"
                    whileHover={{ scale: 1.02 }}
                    onClick={() => addToCart(product)}
                  >
                    <span className="product-emoji">{product.image}</span>
                    <div className="product-info">
                      <h4>{product.name}</h4>
                      <p>${product.price}</p>
                    </div>
                    <FiPlus className="add-icon" />
                  </motion.div>
                ))}
              </motion.div>
            )}
          </div>

          {/* Recommendations */}
          <div className="recommendations-section">
            <h2>💡 Smart Recommendations</h2>
            
            {isLoading && (
              <div className="loading">
                <div className="spinner"></div>
                <p>Analyzing your basket...</p>
              </div>
            )}

            {!isLoading && recommendations.length > 0 && (
              <motion.div 
                className="recommendations-grid"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
              >
                {recommendations.map((product, index) => (
                  <motion.div
                    key={product.id}
                    className="recommendation-card"
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: index * 0.1 }}
                    whileHover={{ scale: 1.05 }}
                    onClick={() => addToCart(product)}
                  >
                    <div className="recommendation-emoji">{product.image}</div>
                    <h3>{product.name}</h3>
                    <p className="recommendation-category">{product.category}</p>
                    <p className="recommendation-price">${product.price}</p>
                    <button className="add-to-cart-btn">
                      <FiPlus /> Add to Cart
                    </button>
                  </motion.div>
                ))}
              </motion.div>
            )}

            {/* Bundle Discounts */}
            {bundleDiscounts.length > 0 && (
              <motion.div 
                className="bundle-discounts"
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
              >
                <h3><FiGift /> Bundle Discounts Available!</h3>
                {bundleDiscounts.map((bundle, index) => (
                  <div key={index} className="bundle-item">
                    <p><strong>{bundle.bundle_name}</strong></p>
                    <p>Add {bundle.missing_items.join(', ')} for {bundle.discount}</p>
                    <p className="savings">Save {bundle.savings}</p>
                  </div>
                ))}
              </motion.div>
            )}

            {/* Health Warnings */}
            {healthWarnings.length > 0 && (
              <motion.div 
                className="health-warnings"
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
              >
                <h3><FiAlertTriangle /> Health Warnings</h3>
                {healthWarnings.map((warning, index) => (
                  <p key={index} className="warning-text">{warning}</p>
                ))}
              </motion.div>
            )}
          </div>
        </div>

        {/* Right Panel - Cart */}
        <div className="cart-panel">
          <div className="cart-header">
            <FiShoppingCart />
            <h2>Your Cart</h2>
          </div>

          <div className="cart-items">
            <AnimatePresence>
              {cart.map((item, index) => (
                <motion.div
                  key={item.id}
                  className="cart-item"
                  initial={{ opacity: 0, x: 50 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: -50 }}
                  transition={{ delay: index * 0.1 }}
                >
                  <div className="cart-item-emoji">{item.image}</div>
                  <div className="cart-item-details">
                    <h4>{item.name}</h4>
                    <p>${item.price} each</p>
                    <div className="quantity-controls">
                      <button 
                        onClick={() => updateQuantity(item.id, item.quantity - 1)}
                        className="quantity-btn"
                      >
                        -
                      </button>
                      <span>{item.quantity}</span>
                      <button 
                        onClick={() => updateQuantity(item.id, item.quantity + 1)}
                        className="quantity-btn"
                      >
                        +
                      </button>
                    </div>
                  </div>
                  <div className="cart-item-total">
                    <p>${(item.price * item.quantity).toFixed(2)}</p>
                    <button 
                      onClick={() => removeFromCart(item.id)}
                      className="remove-btn"
                    >
                      <FiTrash2 />
                    </button>
                  </div>
                </motion.div>
              ))}
            </AnimatePresence>

            {cart.length === 0 && (
              <div className="empty-cart">
                <p>Your cart is empty</p>
                <p>Search for products to get started!</p>
              </div>
            )}
          </div>

          {cart.length > 0 && (
            <motion.div 
              className="cart-summary"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
            >
              <div className="summary-row">
                <span>Subtotal:</span>
                <span>${getTotalPrice().toFixed(2)}</span>
              </div>
              <div className="summary-row">
                <span>Total Calories:</span>
                <span>{getTotalCalories()}</span>
              </div>
              <button onClick={handleCheckout} className="checkout-btn">
                Proceed to Checkout
              </button>
            </motion.div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App; 