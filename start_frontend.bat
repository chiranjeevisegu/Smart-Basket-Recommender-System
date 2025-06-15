@echo off
echo 🛒 Smart Basket Recommender - Frontend Setup
echo ================================================

echo 📦 Installing Node.js dependencies...
cd frontend
call npm install

if %errorlevel% neq 0 (
    echo ❌ Error installing dependencies. Please check your Node.js installation.
    pause
    exit /b 1
)

echo ✅ Dependencies installed successfully
echo 🚀 Starting React development server...
echo 📍 App will be available at: http://localhost:3000
echo 🔄 Press Ctrl+C to stop the server
echo ----------------------------------------

call npm start

pause 