import React from 'react';
import './Header.css';

const Header: React.FC = () => {
  return (
    <header className="header">
      <div className="header-content">
        <div className="logo">
          <div className="logo-icon">
            <svg width="32" height="32" viewBox="0 0 32 32" fill="none">
              <rect width="32" height="32" rx="6" fill="url(#gradient)"/>
              <path d="M8 16L12 20L24 8" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              <defs>
                <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" stopColor="#4c1d95"/>
                  <stop offset="100%" stopColor="#1e40af"/>
                </linearGradient>
              </defs>
            </svg>
          </div>
          <span className="logo-text">AppForge</span>
        </div>
        
        <nav className="nav">
          <a href="#features" className="nav-link">Features</a>
          <a href="#pricing" className="nav-link">Pricing</a>
          <a href="#docs" className="nav-link">Docs</a>
        </nav>
        
        <div className="header-actions">
          <button className="btn-secondary">Sign In</button>
          <button className="btn-primary">Get Started</button>
        </div>
      </div>
    </header>
  );
};

export default Header;