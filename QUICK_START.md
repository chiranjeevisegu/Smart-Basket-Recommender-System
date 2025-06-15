# 🚀 Quick Start Guide

Get the Smart Basket Recommender running in 5 minutes!

## 📋 Prerequisites

- **Python 3.8+** (check with `python --version`)
- **Node.js 16+** (check with `node --version`)
- **npm** (comes with Node.js)

## ⚡ Super Quick Setup

### 1. Start Backend (Terminal 1)
```bash
# Windows
python start_backend.py

# OR manually:
cd backend
pip install -r ../requirements.txt
python -m spacy download en_core_web_sm
python main.py
```

### 2. Start Frontend (Terminal 2)
```bash
# Windows
start_frontend.bat

# Mac/Linux
chmod +x start_frontend.sh
./start_frontend.sh

# OR manually:
cd frontend
npm install
npm start
```

### 3. Open Your Browser
- **Frontend**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs

## 🧪 Test the System

Run the demo script to test everything:
```bash
python demo.py
```

## 🎯 What You'll See

### Frontend Features
- **Search Bar**: Type "apple", "chicken", "milk" to find products
- **Cart Panel**: Add items and see real-time updates
- **Recommendations**: Smart suggestions appear as you add items
- **Chatbot**: Click "AI Assistant" on the left for help
- **Health Warnings**: Get alerts for unhealthy combinations
- **Bundle Discounts**: See special offers for product combinations

### Try These Examples
1. **Search for "apple"** → Add to cart
2. **Search for "chicken"** → Add to cart
3. **Watch recommendations appear** automatically
4. **Click AI Assistant** → Ask "Suggest a side dish"
5. **Add more items** → See health warnings and bundle discounts

## 🔧 Troubleshooting

### Backend Issues
- **Port 8000 in use**: Kill existing process or change port in `main.py`
- **spaCy model error**: Run `python -m spacy download en_core_web_sm`
- **Import errors**: Make sure all requirements are installed

### Frontend Issues
- **Port 3000 in use**: Kill existing process or change port
- **npm install fails**: Check Node.js version and internet connection
- **Proxy errors**: Make sure backend is running on port 8000

### API Connection Issues
- **CORS errors**: Backend CORS is configured for localhost:3000
- **Connection refused**: Make sure backend is running first
- **Timeout errors**: Check if Google AI API key is working

## 🎉 Success Indicators

✅ Backend running on http://localhost:8000  
✅ Frontend running on http://localhost:3000  
✅ Can search and add products  
✅ Recommendations appear in real-time  
✅ Chatbot responds to questions  
✅ Health warnings and discounts show up  

## 🚀 Next Steps

1. **Explore the API**: Visit http://localhost:8000/docs
2. **Try different products**: Search for various food items
3. **Test the chatbot**: Ask for recipes and alternatives
4. **Check recommendations**: Add different combinations
5. **Customize**: Modify product catalog or add new features

---

**Need help?** Check the main README.md for detailed documentation! 