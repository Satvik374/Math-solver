# AppForge - AI-Powered App Generator

A responsive web application that allows users to generate desktop and mobile applications automatically using the Gemini API. Features a clean, modern interface inspired by Cursor.

## Features

- 🎨 **Modern UI** - Clean, responsive design inspired by Cursor
- 🤖 **AI-Powered** - Uses Gemini API to generate complete application code
- 🎯 **Multi-Platform** - Generate apps for Web, Windows, macOS, Linux, iOS, and Android
- 📦 **ZIP Download** - Automatically packages generated code into downloadable archives
- ⚡ **Real-time Feedback** - Loading states and error handling
- 📱 **Responsive** - Works perfectly on desktop and mobile devices

## Tech Stack

### Frontend
- React 18 with TypeScript
- Modern CSS with CSS Grid and Flexbox
- Responsive design with mobile-first approach

### Backend
- Node.js with Express
- Google Generative AI (Gemini API)
- JSZip for file packaging
- CORS and security middleware

## Quick Start

### Prerequisites
- Node.js 16+ and npm
- Gemini API key (get one from [Google AI Studio](https://makersuite.google.com/app/apikey))

### Installation

1. **Clone and install dependencies:**
   ```bash
   git clone <repository-url>
   cd app-generator
   npm run install-all
   ```

2. **Configure environment:**
   ```bash
   cd backend
   cp .env.example .env
   # Edit .env and add your GEMINI_API_KEY
   ```

3. **Start development servers:**
   ```bash
   # From project root
   npm run dev
   ```

   This will start:
   - Frontend: http://localhost:3000
   - Backend: http://localhost:5000

### Environment Variables

Create `/backend/.env` with:
```env
GEMINI_API_KEY=your_gemini_api_key_here
PORT=5000
```

## Usage

1. **Open the application** in your browser at http://localhost:3000
2. **Enter app details:**
   - App name (optional)
   - Detailed description of your app
   - Select target platforms
   - Add key features (optional)
3. **Click "Generate App"** and wait for the AI to create your code
4. **Download the ZIP file** containing your generated application

## Supported Platforms

- **Web Apps**: HTML, CSS, JavaScript with modern responsive design
- **Windows**: Python applications with tkinter GUI
- **macOS**: Swift applications with SwiftUI
- **Linux**: C++ applications with GTK
- **iOS**: SwiftUI applications for iPhone/iPad
- **Android**: Java applications with Android SDK

## Generated Code Structure

Each platform generates a complete, runnable application with:
- Main application files
- Configuration files (package.json, build files, etc.)
- README with platform-specific setup instructions
- All necessary dependencies and build scripts

## API Endpoints

### POST `/api/generate-app`
Generate applications for specified platforms.

**Request Body:**
```json
{
  "description": "App description",
  "appName": "MyApp",
  "platforms": ["web", "windows", "ios"],
  "features": ["user authentication", "data persistence"]
}
```

**Response:** ZIP file download

### GET `/api/health`
Health check endpoint.

## Development

### Project Structure
```
app-generator/
├── frontend/                 # React TypeScript frontend
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── App.tsx          # Main App component
│   │   └── App.css          # Global styles
│   └── package.json
├── backend/                 # Node.js Express backend
│   ├── server.js           # Main server file
│   ├── .env.example        # Environment variables template
│   └── package.json
├── package.json            # Root package.json with scripts
└── README.md
```

### Available Scripts

From project root:
- `npm run dev` - Start both frontend and backend in development mode
- `npm run install-all` - Install dependencies for all packages
- `npm run build` - Build frontend for production
- `npm start` - Start backend in production mode

### Component Overview

- **Header**: Navigation and branding
- **AppGenerator**: Main form and generation logic
- **Footer**: Links and company information

## Customization

### Adding New Platforms

1. Add platform definition to `platforms` array in `AppGenerator.tsx`
2. Add generation logic in `generatePrompt()` function in `server.js`
3. Add file parsing logic in `parseGeneratedCode()` function

### Styling

The application uses a modern dark theme with:
- CSS custom properties for theming
- Responsive grid and flexbox layouts
- Smooth animations and transitions
- Cursor-inspired design elements

## Security

- CORS enabled for cross-origin requests
- Helmet.js for security headers
- Input validation and sanitization
- Environment variable protection for API keys

## Error Handling

- Graceful API error handling
- User-friendly error messages
- Loading states and progress indicators
- Network failure recovery

## Browser Support

- Chrome/Edge 88+
- Firefox 85+
- Safari 14+
- Mobile browsers (iOS Safari, Chrome Mobile)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

For issues and questions:
- Check the documentation
- Review platform-specific setup guides
- Submit issues on GitHub

## Roadmap

- [ ] Additional platform support (Flutter, React Native)
- [ ] Code preview before download
- [ ] Project templates and examples
- [ ] User accounts and project history
- [ ] Advanced AI model options
- [ ] Custom deployment options