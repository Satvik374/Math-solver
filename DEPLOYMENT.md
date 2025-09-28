# Deployment Guide

This guide covers how to deploy AppForge to various platforms.

## Prerequisites

- Node.js 16+ and npm
- Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
- Domain name (for production deployment)

## Environment Setup

### 1. Clone and Install
```bash
git clone <repository-url>
cd app-generator
npm run install-all
```

### 2. Configure Environment
```bash
cd backend
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
```

## Development Deployment

### Local Development
```bash
npm run dev
```
This starts both frontend (port 3000) and backend (port 5000).

## Production Deployment

### Option 1: Traditional VPS/Server

#### 1. Server Setup
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Node.js 18 LTS
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Install PM2 for process management
sudo npm install -g pm2

# Install Nginx for reverse proxy
sudo apt install nginx -y
```

#### 2. Deploy Application
```bash
# Clone repository
git clone <repository-url> /var/www/appforge
cd /var/www/appforge

# Install dependencies
npm run install-all

# Build frontend
cd frontend && npm run build && cd ..

# Configure environment
cd backend
cp .env.example .env
# Edit .env with production values
nano .env
```

#### 3. PM2 Configuration
Create `ecosystem.config.js`:
```javascript
module.exports = {
  apps: [{
    name: 'appforge-backend',
    script: 'backend/server.js',
    instances: 'max',
    exec_mode: 'cluster',
    env: {
      NODE_ENV: 'production',
      PORT: 5000
    }
  }]
};
```

Start with PM2:
```bash
pm2 start ecosystem.config.js
pm2 save
pm2 startup
```

#### 4. Nginx Configuration
Create `/etc/nginx/sites-available/appforge`:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    # Serve React build
    location / {
        root /var/www/appforge/frontend/build;
        index index.html index.htm;
        try_files $uri $uri/ /index.html;
    }

    # Proxy API requests to backend
    location /api {
        proxy_pass http://localhost:5000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/appforge /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### 5. SSL with Let's Encrypt
```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d your-domain.com
```

### Option 2: Docker Deployment

#### 1. Create Dockerfile for Backend
Create `backend/Dockerfile`:
```dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .

EXPOSE 5000

CMD ["npm", "start"]
```

#### 2. Create Dockerfile for Frontend
Create `frontend/Dockerfile`:
```dockerfile
FROM node:18-alpine as build

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

#### 3. Create Docker Compose
Create `docker-compose.yml`:
```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    environment:
      - NODE_ENV=production
      - GEMINI_API_KEY=${GEMINI_API_KEY}
      - PORT=5000
    ports:
      - "5000:5000"
    restart: unless-stopped

  frontend:
    build: ./frontend
    ports:
      - "80:80"
    depends_on:
      - backend
    restart: unless-stopped
```

#### 4. Deploy with Docker
```bash
# Create .env file with GEMINI_API_KEY
echo "GEMINI_API_KEY=your_key_here" > .env

# Build and start
docker-compose up -d

# View logs
docker-compose logs -f
```

### Option 3: Vercel (Frontend) + Railway (Backend)

#### Frontend on Vercel
1. Push frontend to GitHub
2. Connect to Vercel
3. Set build command: `npm run build`
4. Set output directory: `build`
5. Add environment variable: `REACT_APP_API_URL=your-backend-url`

#### Backend on Railway
1. Push backend to GitHub
2. Connect to Railway
3. Add environment variables:
   - `GEMINI_API_KEY`
   - `PORT=5000`
   - `NODE_ENV=production`

### Option 4: Heroku

#### Prepare for Heroku
Create `Procfile`:
```
web: cd backend && npm start
```

Create `package.json` in root:
```json
{
  "name": "appforge-heroku",
  "scripts": {
    "build": "cd frontend && npm install && npm run build",
    "start": "cd backend && npm start",
    "heroku-postbuild": "npm run build"
  }
}
```

#### Deploy to Heroku
```bash
# Install Heroku CLI
# Create Heroku app
heroku create your-app-name

# Set environment variables
heroku config:set GEMINI_API_KEY=your_key_here
heroku config:set NODE_ENV=production

# Deploy
git push heroku main
```

## Environment Variables

### Backend (.env)
```env
# Required
GEMINI_API_KEY=your_gemini_api_key_here

# Optional
PORT=5000
NODE_ENV=production
```

### Frontend (if using separate backend URL)
```env
REACT_APP_API_URL=https://your-backend-url.com
```

## Performance Optimization

### 1. Backend Optimizations
- Enable gzip compression
- Implement request rate limiting
- Add response caching for static responses
- Use clustering for multi-core servers

### 2. Frontend Optimizations
- Implement code splitting
- Add service worker for caching
- Optimize images and assets
- Use CDN for static assets

### 3. Database Considerations
For production, consider adding:
- User authentication
- Request logging
- Usage analytics
- Generated app storage

## Monitoring and Maintenance

### 1. Health Checks
Set up monitoring for:
- API endpoint health (`/api/health`)
- Server resources (CPU, memory)
- Response times
- Error rates

### 2. Logs
Configure logging for:
- Application errors
- API requests
- Generation statistics
- Security events

### 3. Backups
- Regular code backups
- Environment configuration backups
- Generated app archives (if stored)

## Security Checklist

- [ ] HTTPS enabled
- [ ] Environment variables secured
- [ ] Rate limiting implemented
- [ ] Input validation on all endpoints
- [ ] CORS properly configured
- [ ] Security headers set
- [ ] Regular dependency updates
- [ ] API key rotation policy

## Troubleshooting

### Common Issues

1. **Gemini API errors**
   - Check API key validity
   - Verify API quotas
   - Check network connectivity

2. **Frontend build errors**
   - Clear node_modules and reinstall
   - Check Node.js version compatibility
   - Verify environment variables

3. **Backend startup issues**
   - Check port availability
   - Verify environment variables
   - Check file permissions

### Support

For deployment issues:
1. Check application logs
2. Verify environment configuration
3. Test API endpoints individually
4. Review system resources

## Cost Optimization

### Gemini API Usage
- Monitor API usage and costs
- Implement request caching
- Add request queuing for high traffic
- Consider usage limits per user

### Server Resources
- Right-size server instances
- Use CDN for static assets
- Implement auto-scaling
- Monitor resource usage