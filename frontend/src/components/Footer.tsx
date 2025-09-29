import React from 'react';
import './Footer.css';

const Footer: React.FC = () => {
  return (
    <footer className="footer">
      <div className="footer-content">
        <div className="footer-section">
          <div className="footer-logo">
            <div className="logo-icon">
              <svg width="24" height="24" viewBox="0 0 32 32" fill="none">
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
          <p className="footer-description">
            AI-powered app generation for every platform. Build faster, ship sooner.
          </p>
        </div>

        <div className="footer-links">
          <div className="link-group">
            <h4>Product</h4>
            <a href="#features">Features</a>
            <a href="#pricing">Pricing</a>
            <a href="#changelog">Changelog</a>
            <a href="#roadmap">Roadmap</a>
          </div>
          
          <div className="link-group">
            <h4>Resources</h4>
            <a href="#docs">Documentation</a>
            <a href="#tutorials">Tutorials</a>
            <a href="#examples">Examples</a>
            <a href="#community">Community</a>
          </div>
          
          <div className="link-group">
            <h4>Support</h4>
            <a href="#help">Help Center</a>
            <a href="#contact">Contact</a>
            <a href="#status">Status</a>
            <a href="#security">Security</a>
          </div>
        </div>
      </div>

      <div className="footer-bottom">
        <div className="footer-bottom-content">
          <p className="copyright">
            © 2024 AppForge. All rights reserved.
          </p>
          <div className="footer-bottom-links">
            <a href="#privacy">Privacy Policy</a>
            <a href="#terms">Terms of Service</a>
            <a href="#cookies">Cookie Policy</a>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;