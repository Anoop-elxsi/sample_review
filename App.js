import React, { useState } from 'react';
import Header from './components/Header';
import ReviewForm from './components/ReviewForm';
import FeaturesSection from './components/FeaturesSection';
import Footer from './components/Footer';
import CodeReviewApp from './pages/CodeReviewApp';

const App = () => {
  const [loading, setLoading] = useState(false);
  const [codeReviewVisible, setCodeReviewVisible] = useState(false);
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [formData, setFormData] = useState({
    repoUrl: ''
  });
  const [errors, setErrors] = useState({});
  const [urlHistory, setUrlHistory] = useState([]);

  const handleReviewSubmit = async (formData) => {
    setLoading(true);

    try {
      const response = await fetch('/api/code-review', {
        method: 'POST',
        body: JSON.stringify(formData),
        headers: {
          'Content-Type': 'application/json'
        }
      });

      if (!response.ok) {
        // Handle non-200 responses (e.g., 400, 500)
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
      const reviewResults = await response.json();
      setLoading(false);
      // Handle successful response (e.g., update state with results)
    } catch (error) {
      console.error("Error during code review submission:", error);
      // Handle the error appropriately (e.g., display an error message to the user)
      setLoading(false);
      //Consider displaying a user-friendly error message
      setErrors({ [error.message]: 'An error occurred during the review process.' });
    }
  };

  const handleBackToForm = () => {
    setCodeReviewVisible(false);
    setFormData(null);
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