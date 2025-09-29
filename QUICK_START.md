# 🚀 Quick Start Guide

## Error Fix: "Could not read package.json"

If you're seeing this error:
```
npm error code ENOENT
npm error Could not read package.json
```

This means you're in the wrong directory. Follow these steps:

## 📂 Step 1: Navigate to the Correct Directory

Make sure you're in the AppForge project directory (the one containing our app-generator files):

### On Windows:
```cmd
cd C:\path\to\app-generator
```

### On Mac/Linux:
```bash
cd /path/to/app-generator
```

You should see these files in the directory:
- `package.json`
- `frontend/` folder
- `backend/` folder
- `README.md`
- `setup.sh`

## 🔧 Step 2: Verify You're in the Right Place

Run this command to check:
```bash
ls
```
or on Windows:
```cmd
dir
```

You should see output like:
```
backend/
frontend/
package.json
README.md
setup.sh
...
```

## ⚡ Step 3: Run Setup

Once you're in the correct directory:

### Automatic Setup (Recommended):
```bash
# On Mac/Linux:
./setup.sh

# On Windows:
npm run install-all
```

### Manual Setup:
```bash
# Install all dependencies
npm run install-all

# Configure environment
cd backend
copy .env.example .env
# Edit .env and add your GEMINI_API_KEY

# Go back to root
cd ..

# Start development servers
npm run dev
```

## 🌐 Step 4: Access the Application

Once setup is complete:
- Frontend: http://localhost:3000
- Backend: http://localhost:5000

## 🔑 Step 5: Add Your Gemini API Key

1. Get a free API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Edit `backend/.env` file:
   ```
   GEMINI_API_KEY=your_actual_api_key_here
   PORT=5000
   ```

## 🎯 You're Ready!

Navigate to http://localhost:3000 and start generating apps!

---

## Troubleshooting

### Issue: Still getting package.json errors
**Solution**: Make sure you downloaded/cloned the complete AppForge project, not a different project.

### Issue: Permission denied on setup.sh
**Solution**: 
```bash
chmod +x setup.sh
./setup.sh
```

### Issue: Node.js not found
**Solution**: Install Node.js 16+ from https://nodejs.org

### Issue: Backend won't start
**Solution**: Check that you've added your GEMINI_API_KEY to backend/.env

### Issue: Frontend won't connect to backend
**Solution**: Make sure both servers are running with `npm run dev`