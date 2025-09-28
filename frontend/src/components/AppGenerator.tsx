import React, { useState } from 'react';
import './AppGenerator.css';

interface Platform {
  id: string;
  name: string;
  description: string;
  icon: string;
  category: 'desktop' | 'mobile' | 'web';
}

const platforms: Platform[] = [
  { id: 'web', name: 'Web App', description: 'HTML, CSS, JavaScript', icon: '🌐', category: 'web' },
  { id: 'windows', name: 'Windows', description: 'Python with tkinter', icon: '🪟', category: 'desktop' },
  { id: 'mac', name: 'macOS', description: 'Swift with SwiftUI', icon: '🍎', category: 'desktop' },
  { id: 'linux', name: 'Linux', description: 'C++ with GTK', icon: '🐧', category: 'desktop' },
  { id: 'ios', name: 'iOS', description: 'SwiftUI for iPhone/iPad', icon: '📱', category: 'mobile' },
  { id: 'android', name: 'Android', description: 'Java with Android SDK', icon: '🤖', category: 'mobile' },
];

const AppGenerator: React.FC = () => {
  const [description, setDescription] = useState('');
  const [appName, setAppName] = useState('');
  const [selectedPlatforms, setSelectedPlatforms] = useState<string[]>([]);
  const [features, setFeatures] = useState<string[]>([]);
  const [isGenerating, setIsGenerating] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handlePlatformToggle = (platformId: string) => {
    setSelectedPlatforms(prev => 
      prev.includes(platformId) 
        ? prev.filter(id => id !== platformId)
        : [...prev, platformId]
    );
  };

  const handleFeatureAdd = (feature: string) => {
    if (feature.trim() && !features.includes(feature.trim())) {
      setFeatures(prev => [...prev, feature.trim()]);
    }
  };

  const handleFeatureRemove = (feature: string) => {
    setFeatures(prev => prev.filter(f => f !== feature));
  };

  const handleGenerate = async () => {
    if (!description.trim()) {
      setError('Please provide an app description');
      return;
    }

    if (selectedPlatforms.length === 0) {
      setError('Please select at least one platform');
      return;
    }

    setIsGenerating(true);
    setError(null);

    try {
      const response = await fetch('/api/generate-app', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          description,
          appName: appName || 'MyApp',
          platforms: selectedPlatforms,
          features,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to generate app');
      }

      // Handle file download
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `${appName || 'generated-app'}.zip`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);

    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setIsGenerating(false);
    }
  };

  const groupedPlatforms = platforms.reduce((acc, platform) => {
    if (!acc[platform.category]) {
      acc[platform.category] = [];
    }
    acc[platform.category].push(platform);
    return acc;
  }, {} as Record<string, Platform[]>);

  return (
    <div className="app-generator">
      <div className="hero-section">
        <h1 className="hero-title">
          Build Apps with <span className="gradient-text">AI</span>
        </h1>
        <p className="hero-subtitle">
          Describe your app idea and generate complete, ready-to-run applications for any platform
        </p>
      </div>

      <div className="generator-form">
        <div className="form-section">
          <label className="form-label">App Name</label>
          <input
            type="text"
            className="form-input"
            placeholder="My Awesome App"
            value={appName}
            onChange={(e) => setAppName(e.target.value)}
          />
        </div>

        <div className="form-section">
          <label className="form-label">Describe Your App</label>
          <textarea
            className="form-textarea"
            placeholder="I want to create a simple todo app with the ability to add, edit, and delete tasks. Users should be able to mark tasks as complete and filter by status."
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            rows={4}
          />
        </div>

        <div className="form-section">
          <label className="form-label">Target Platforms</label>
          <div className="platforms-grid">
            {Object.entries(groupedPlatforms).map(([category, platformList]) => (
              <div key={category} className="platform-category">
                <h3 className="category-title">{category.charAt(0).toUpperCase() + category.slice(1)}</h3>
                <div className="platform-list">
                  {platformList.map((platform) => (
                    <div
                      key={platform.id}
                      className={`platform-card ${selectedPlatforms.includes(platform.id) ? 'selected' : ''}`}
                      onClick={() => handlePlatformToggle(platform.id)}
                    >
                      <div className="platform-icon">{platform.icon}</div>
                      <div className="platform-info">
                        <h4 className="platform-name">{platform.name}</h4>
                        <p className="platform-description">{platform.description}</p>
                      </div>
                      <div className="platform-checkbox">
                        {selectedPlatforms.includes(platform.id) && (
                          <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                            <path d="M3 8L6 11L13 4" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                          </svg>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="form-section">
          <label className="form-label">Key Features (Optional)</label>
          <div className="features-input">
            <input
              type="text"
              className="form-input"
              placeholder="Add a feature and press Enter"
              onKeyPress={(e) => {
                if (e.key === 'Enter') {
                  handleFeatureAdd(e.currentTarget.value);
                  e.currentTarget.value = '';
                }
              }}
            />
          </div>
          {features.length > 0 && (
            <div className="features-list">
              {features.map((feature) => (
                <span key={feature} className="feature-tag">
                  {feature}
                  <button
                    className="feature-remove"
                    onClick={() => handleFeatureRemove(feature)}
                  >
                    ×
                  </button>
                </span>
              ))}
            </div>
          )}
        </div>

        {error && (
          <div className="error-message">
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
              <circle cx="8" cy="8" r="7" stroke="currentColor" strokeWidth="2"/>
              <path d="M8 4v4M8 10h.01" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
            </svg>
            {error}
          </div>
        )}

        <button
          className="generate-button"
          onClick={handleGenerate}
          disabled={isGenerating}
        >
          {isGenerating ? (
            <>
              <div className="spinner"></div>
              Generating App...
            </>
          ) : (
            <>
              <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                <path d="M4 10h12M10 4l6 6-6 6" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
              Generate App
            </>
          )}
        </button>
      </div>
    </div>
  );
};

export default AppGenerator;