import React, { useState } from 'react';
import './App.css';
import Header from './components/Header';
import AppGenerator from './components/AppGenerator';
import Footer from './components/Footer';

function App() {
  return (
    <div className="App">
      <Header />
      <main className="main-content">
        <AppGenerator />
      </main>
      <Footer />
    </div>
  );
}

export default App;
