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
      // Mock code review response data in the format expected by CodeReviewDetails
      const reviewResults = {
        "UserService.js": {
          "Logic Errors & Potential Bugs": [
            "Null pointer exception possible in getUserById() when user ID is invalid",
            "Race condition in updateUserStatus() method when multiple threads access simultaneously",
            "Missing validation for email format in createUser() function"
          ],
          "Security Vulnerabilities": [
            "SQL injection vulnerability in raw query execution",
            "Password stored in plain text without encryption",
            "Missing authentication check in sensitive user operations"
          ],
          "Code Quality & Maintainability": [
            "Large method violating single responsibility principle",
            "Hardcoded configuration values should be externalized",
            "Missing error handling and logging mechanisms"
          ]
        },
        "PaymentProcessor.js": {
          "Potential Bugs": [
            "Integer overflow in amount calculation for large transactions",
            "Memory leak in payment validation due to unclosed resources"
          ],
          "Security Vulnerabilities": [
            "Credit card numbers logged in plain text",
            "Missing input sanitization for payment amounts",
            "API keys exposed in configuration files"
          ],
          "Code Quality & Maintainability": [
            "Duplicate code in payment validation methods",
            "Complex nested if-else statements reducing readability",
            "Missing unit tests for critical payment flows"
          ]
        }
      };
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
    </div
  );
};

export default App;