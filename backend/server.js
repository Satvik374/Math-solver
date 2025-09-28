const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const dotenv = require('dotenv');
const { GoogleGenerativeAI } = require('@google/generative-ai');
const JSZip = require('jszip');
const path = require('path');

dotenv.config();

const app = express();
const PORT = process.env.PORT || 5000;

// Middleware
app.use(helmet());
app.use(cors());
app.use(express.json({ limit: '50mb' }));
app.use(express.urlencoded({ extended: true, limit: '50mb' }));

// Initialize Gemini AI
const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);

// Platform-specific templates
const platformTemplates = {
  web: {
    files: {
      'index.html': '',
      'script.js': '',
      'style.css': '',
      'package.json': '',
      'README.md': ''
    }
  },
  desktop: {
    windows: {
      files: {
        'main.py': '',
        'requirements.txt': '',
        'setup.py': '',
        'README.md': ''
      }
    },
    mac: {
      files: {
        'main.swift': '',
        'Package.swift': '',
        'README.md': ''
      }
    },
    linux: {
      files: {
        'main.cpp': '',
        'CMakeLists.txt': '',
        'README.md': ''
      }
    }
  },
  mobile: {
    ios: {
      files: {
        'ContentView.swift': '',
        'App.swift': '',
        'Info.plist': '',
        'README.md': ''
      }
    },
    android: {
      files: {
        'MainActivity.java': '',
        'activity_main.xml': '',
        'AndroidManifest.xml': '',
        'build.gradle': '',
        'README.md': ''
      }
    }
  }
};

// Generate app endpoint
app.post('/api/generate-app', async (req, res) => {
  try {
    const { description, platforms, appName, features } = req.body;

    if (!description || !platforms || platforms.length === 0) {
      return res.status(400).json({ 
        error: 'Description and at least one platform are required' 
      });
    }

    if (!process.env.GEMINI_API_KEY) {
      return res.status(500).json({ 
        error: 'Gemini API key not configured' 
      });
    }

    const model = genAI.getGenerativeModel({ model: 'gemini-pro' });

    const zip = new JSZip();
    const generatedFiles = {};

    // Generate code for each platform
    for (const platform of platforms) {
      const platformFolder = zip.folder(platform);
      
      let prompt = generatePrompt(description, platform, appName, features);
      
      try {
        const result = await model.generateContent(prompt);
        const response = await result.response;
        const generatedCode = response.text();
        
        // Parse the generated code and organize into files
        const files = parseGeneratedCode(generatedCode, platform);
        
        // Add files to ZIP
        Object.entries(files).forEach(([filename, content]) => {
          platformFolder.file(filename, content);
        });
        
        generatedFiles[platform] = files;
        
        // Add a delay to avoid rate limiting
        await new Promise(resolve => setTimeout(resolve, 1000));
        
      } catch (apiError) {
        console.error(`Error generating code for ${platform}:`, apiError);
        // Add error file instead of failing completely
        platformFolder.file('ERROR.txt', `Failed to generate code for ${platform}: ${apiError.message}`);
      }
    }

    // Generate ZIP file
    const zipBuffer = await zip.generateAsync({ type: 'nodebuffer' });
    
    // Set headers for file download
    res.setHeader('Content-Type', 'application/zip');
    res.setHeader('Content-Disposition', `attachment; filename="${appName || 'generated-app'}.zip"`);
    res.setHeader('Content-Length', zipBuffer.length);
    
    res.send(zipBuffer);

  } catch (error) {
    console.error('Error generating app:', error);
    res.status(500).json({ 
      error: 'Failed to generate app. Please try again.',
      details: error.message 
    });
  }
});

// Health check endpoint
app.get('/api/health', (req, res) => {
  res.json({ status: 'OK', timestamp: new Date().toISOString() });
});

// Generate platform-specific prompts
function generatePrompt(description, platform, appName = 'MyApp', features = []) {
  const basePrompt = `Create a complete, functional ${platform} application based on this description: "${description}"`;
  
  let platformSpecific = '';
  
  switch (platform) {
    case 'web':
      platformSpecific = `
        Generate a complete web application with:
        - HTML file with proper structure and meta tags
        - CSS file with modern, responsive styling
        - JavaScript file with all functionality
        - package.json for dependencies
        - README.md with setup instructions
        
        Make it responsive and modern. Use vanilla JavaScript or include popular CDN libraries.
      `;
      break;
      
    case 'windows':
      platformSpecific = `
        Generate a Windows desktop application using Python and tkinter:
        - main.py with complete GUI application
        - requirements.txt with necessary dependencies
        - setup.py for distribution
        - README.md with installation and usage instructions
      `;
      break;
      
    case 'mac':
      platformSpecific = `
        Generate a macOS application using Swift and SwiftUI:
        - main.swift with complete application code
        - Package.swift for Swift Package Manager
        - README.md with build and run instructions
      `;
      break;
      
    case 'linux':
      platformSpecific = `
        Generate a Linux application using C++ and GTK:
        - main.cpp with complete application code
        - CMakeLists.txt for building
        - README.md with compilation and installation instructions
      `;
      break;
      
    case 'ios':
      platformSpecific = `
        Generate an iOS application using SwiftUI:
        - ContentView.swift with main UI
        - App.swift with app structure
        - Info.plist with app configuration
        - README.md with Xcode setup instructions
      `;
      break;
      
    case 'android':
      platformSpecific = `
        Generate an Android application using Java:
        - MainActivity.java with complete activity code
        - activity_main.xml with layout
        - AndroidManifest.xml with permissions and configuration
        - build.gradle with dependencies
        - README.md with Android Studio setup instructions
      `;
      break;
  }
  
  return `${basePrompt}

${platformSpecific}

Application Name: ${appName}
${features.length > 0 ? `Key Features: ${features.join(', ')}` : ''}

Please provide complete, working code for each file. Separate each file with a comment header like:
=== FILENAME: [filename] ===

Make sure the code is production-ready, well-commented, and follows best practices for the platform.`;
}

// Parse generated code into separate files
function parseGeneratedCode(generatedCode, platform) {
  const files = {};
  
  // Split by file separators
  const filePattern = /===\s*FILENAME:\s*([^\s]+)\s*===/gi;
  const sections = generatedCode.split(filePattern);
  
  // Process sections (skip first section which is usually intro text)
  for (let i = 1; i < sections.length; i += 2) {
    if (i + 1 < sections.length) {
      const filename = sections[i].trim();
      let content = sections[i + 1].trim();
      
      // Clean up code blocks
      content = content.replace(/^```[\w]*\n?/gm, '').replace(/\n?```$/gm, '');
      
      files[filename] = content;
    }
  }
  
  // If no files were parsed, create default files with the content
  if (Object.keys(files).length === 0) {
    const template = platformTemplates.web; // Default fallback
    
    switch (platform) {
      case 'web':
        files['index.html'] = extractHTMLFromResponse(generatedCode);
        files['script.js'] = extractJavaScriptFromResponse(generatedCode);
        files['style.css'] = extractCSSFromResponse(generatedCode);
        files['README.md'] = generateReadme(platform, 'Web Application');
        break;
        
      default:
        files['main.txt'] = generatedCode;
        files['README.md'] = generateReadme(platform, 'Generated Application');
    }
  }
  
  return files;
}

// Helper functions to extract code sections
function extractHTMLFromResponse(text) {
  const htmlMatch = text.match(/```html\n([\s\S]*?)\n```/i) || 
                   text.match(/<html[\s\S]*<\/html>/i);
  return htmlMatch ? htmlMatch[1] || htmlMatch[0] : generateDefaultHTML();
}

function extractJavaScriptFromResponse(text) {
  const jsMatch = text.match(/```javascript\n([\s\S]*?)\n```/i) ||
                 text.match(/```js\n([\s\S]*?)\n```/i);
  return jsMatch ? jsMatch[1] : generateDefaultJS();
}

function extractCSSFromResponse(text) {
  const cssMatch = text.match(/```css\n([\s\S]*?)\n```/i);
  return cssMatch ? cssMatch[1] : generateDefaultCSS();
}

// Default file generators
function generateDefaultHTML() {
  return `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Generated App</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div id="app">
        <h1>Welcome to Your Generated App</h1>
        <p>This app was generated using AI. Customize it to fit your needs!</p>
    </div>
    <script src="script.js"></script>
</body>
</html>`;
}

function generateDefaultJS() {
  return `// Generated JavaScript Application
document.addEventListener('DOMContentLoaded', function() {
    console.log('App loaded successfully!');
    
    // Add your application logic here
    const app = document.getElementById('app');
    if (app) {
        app.addEventListener('click', function() {
            console.log('App clicked!');
        });
    }
});`;
}

function generateDefaultCSS() {
  return `/* Generated CSS Styles */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
    line-height: 1.6;
    color: #333;
    background-color: #f5f5f5;
}

#app {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
    background: white;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    margin-top: 50px;
}

h1 {
    color: #2c3e50;
    margin-bottom: 20px;
    text-align: center;
}

p {
    margin-bottom: 15px;
    text-align: center;
    color: #666;
}`;
}

function generateReadme(platform, appType) {
  return `# ${appType}

This ${platform} application was generated using AI.

## Setup Instructions

### Prerequisites
- Ensure you have the necessary development tools installed for ${platform}

### Installation
1. Extract the generated files
2. Follow platform-specific setup instructions below

### Platform-specific Instructions

${getPlatformInstructions(platform)}

## Features
- AI-generated code structure
- Ready-to-run application
- Customizable and extensible

## Support
For issues or questions, please refer to the platform documentation.
`;
}

function getPlatformInstructions(platform) {
  switch (platform) {
    case 'web':
      return `1. Open index.html in a web browser
2. For development server: use a local server like Live Server
3. Customize the CSS and JavaScript as needed`;
      
    case 'windows':
      return `1. Install Python 3.7+
2. Run: pip install -r requirements.txt
3. Run: python main.py`;
      
    case 'mac':
      return `1. Install Xcode
2. Open Terminal and navigate to project folder
3. Run: swift run`;
      
    case 'linux':
      return `1. Install build-essential and cmake
2. Run: mkdir build && cd build
3. Run: cmake .. && make
4. Run: ./main`;
      
    case 'ios':
      return `1. Install Xcode
2. Create new iOS project
3. Replace ContentView.swift and other files
4. Build and run in simulator`;
      
    case 'android':
      return `1. Install Android Studio
2. Create new Android project
3. Replace the generated files
4. Build and run on device/emulator`;
      
    default:
      return 'Follow standard development practices for this platform.';
  }
}

// Start server
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
  console.log(`Gemini API configured: ${!!process.env.GEMINI_API_KEY}`);
});