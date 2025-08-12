import React, { useState } from 'react';
import Header from './components/Header';
import ReviewForm from './components/ReviewForm';
import FeaturesSection from './components/FeaturesSection';
import Footer from './components/Footer';
import CodeReviewApp from './pages/CodeReviewApp';

const App = () => {
  const [loading, setLoading] = useState(false);
  const [showCodeReview, setShowCodeReview] = useState(false);
  // Removed codeReviewData state, as it's no longer used.  A real implementation would fetch this data.
  const [formData, setFormData] = useState({
    repoUrl: ''
  });
  
  const [errors, setErrors] = useState({});
  const [urlHistory, setUrlHistory] = useState([]);
  const [showSuggestions, setShowSuggestions] = useState(false);

  const handleReviewSubmit = async (formData) => {
    setLoading(true);

    // Simulate API call for code review
    try {
      const response = await fetch('/api/code-review', { // Replace with actual API endpoint
        method: 'POST',
        body: JSON.stringify(formData),
        headers: {
          'Content-Type': 'application/json'
        }
      });
      const reviewResults = await response.json();
      setLoading(false);
    } catch (error) {
      console.error("Error during code review submission:", error);
      // Handle the error appropriately (e.g., display an error message to the user)
      setLoading(false);
    }
  };

  const handleBackToForm = () => {
    setShowCodeReview(false);
    setCodeReviewData(null);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-200 font-sans">
      <Header />

      <ReviewForm onSubmit={handleReviewSubmit} loading={loading} />
      <FeaturesSection />
      <Footer />
    </div>
  );
};

export default App;