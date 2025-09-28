#!/usr/bin/env node

/**
 * Simple API test script for AppForge
 * Tests the Gemini API integration without the frontend
 */

const fs = require('fs');
const path = require('path');

// Test configuration
const API_URL = 'http://localhost:5000';
const TEST_REQUEST = {
  description: 'Create a simple calculator app with basic arithmetic operations (add, subtract, multiply, divide). It should have a clean interface with number buttons and operation buttons.',
  appName: 'SimpleCalculator',
  platforms: ['web'],
  features: ['responsive design', 'keyboard support']
};

async function testAPI() {
  console.log('🧪 Testing AppForge API...\n');

  try {
    // Test health endpoint
    console.log('1. Testing health endpoint...');
    const healthResponse = await fetch(`${API_URL}/api/health`);
    
    if (!healthResponse.ok) {
      throw new Error(`Health check failed: ${healthResponse.status}`);
    }
    
    const healthData = await healthResponse.json();
    console.log('✅ Health check passed:', healthData);

    // Test app generation
    console.log('\n2. Testing app generation...');
    console.log('Request:', JSON.stringify(TEST_REQUEST, null, 2));
    
    const generateResponse = await fetch(`${API_URL}/api/generate-app`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(TEST_REQUEST),
    });

    if (!generateResponse.ok) {
      const errorData = await generateResponse.json();
      throw new Error(`Generation failed: ${errorData.error || generateResponse.status}`);
    }

    // Save the ZIP file
    const arrayBuffer = await generateResponse.arrayBuffer();
    const buffer = Buffer.from(arrayBuffer);
    
    const filename = `${TEST_REQUEST.appName}-test.zip`;
    const filepath = path.join(__dirname, filename);
    
    fs.writeFileSync(filepath, buffer);
    
    console.log('✅ App generated successfully!');
    console.log(`📁 ZIP file saved: ${filepath}`);
    console.log(`📊 File size: ${(buffer.length / 1024).toFixed(2)} KB`);

  } catch (error) {
    console.error('❌ Test failed:', error.message);
    
    if (error.message.includes('ECONNREFUSED')) {
      console.log('\n💡 Make sure the backend server is running:');
      console.log('   cd backend && npm start');
    } else if (error.message.includes('API key')) {
      console.log('\n💡 Make sure you have configured your Gemini API key:');
      console.log('   Edit backend/.env and add GEMINI_API_KEY=your_key_here');
    }
    
    process.exit(1);
  }
}

// Add fetch polyfill for older Node.js versions
if (!global.fetch) {
  console.log('Installing fetch polyfill...');
  global.fetch = require('node-fetch');
}

console.log('AppForge API Test Script');
console.log('========================\n');

testAPI();