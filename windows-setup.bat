@echo off
echo 🚀 Setting up AppForge - AI-Powered App Generator
echo ==================================================

REM Check if Node.js is installed
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js is not installed. Please install Node.js 16+ and try again.
    echo Download from: https://nodejs.org
    pause
    exit /b 1
)

echo ✅ Node.js detected: 
node --version

echo.
echo 📦 Installing dependencies...
call npm run install-all

if %errorlevel% neq 0 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo ⚙️ Setting up environment...

REM Copy environment file if it doesn't exist
if not exist "backend\.env" (
    copy "backend\.env.example" "backend\.env"
    echo 📝 Created backend\.env from template
    echo ⚠️  Please edit backend\.env and add your GEMINI_API_KEY
) else (
    echo ✅ Environment file already exists
)

echo.
echo 🎉 Setup complete!
echo.
echo Next steps:
echo 1. Edit backend\.env and add your Gemini API key
echo 2. Run 'npm run dev' to start the development servers
echo 3. Open http://localhost:3000 in your browser
echo.
echo Happy coding! 🚀
pause