import React, { useState } from 'react';
import axios from 'axios';
import { postScholarship } from '../services/api';

const ScholarshipForm = ({ onClose }) => {
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    amount: '',
    requirements: '',
    application_link: '',
    deadline: '',
  });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitMessage, setSubmitMessage] = useState('');
  const [submitError, setSubmitError] = useState('');

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    setSubmitMessage('');
    setSubmitError('');

    try {
      const response = await postScholarship(
        formData.title,
        formData.description,
        formData.amount,
        formData.requirements,
        formData.application_link,
        formData.deadline,
      );

      // Clear form and show success message
      setFormData({
        title: '',
        description: '',
        amount: '',
        requirements: '',
        application_link: '',
        deadline: '',
      });
      setSubmitMessage('Scholarship submitted successfully!');

    } catch (error) {
      console.error('Error submitting scholarship:', error);
      setSubmitError('Failed to submit scholarship. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-2">
      <div className="bg-white rounded-lg shadow-xl max-w-md w-full mx-auto overflow-hidden">
        <div className="bg-blue-500 text-white p-4 flex items-center justify-between">
          <h2 className="text-xl font-bold">Add Scholarship</h2>
          <button 
            onClick={onClose}
            className="text-white hover:bg-blue-600 rounded-full p-1 transition-colors"
            disabled={isSubmitting}
          >
            <svg 
              xmlns="http://www.w3.org/2000/svg" 
              width="20" 
              height="20" 
              viewBox="0 0 24 24" 
              fill="none" 
              stroke="currentColor" 
              strokeWidth="2" 
              strokeLinecap="round" 
              strokeLinejoin="round"
            >
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>
        
        {submitMessage && (
          <div className="bg-green-100 text-green-700 p-3 text-center">
            {submitMessage}
          </div>
        )}
        
        {submitError && (
          <div className="bg-red-100 text-red-700 p-3 text-center">
            {submitError}
          </div>
        )}
        
        <form 
          onSubmit={handleSubmit} 
          className="p-4 space-y-3"
        >
          <div>
            <label 
              htmlFor="title" 
              className="block text-xs font-medium text-gray-700 mb-1"
            >
              Scholarship Title
            </label>
            <input
              type="text"
              id="title"
              name="title"
              placeholder="Enter title"
              value={formData.title}
              onChange={handleChange}
              required
              disabled={isSubmitting}
              className="w-full px-2 py-1 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-blue-500 disabled:bg-gray-100"
            />
          </div>
          
          <div>
            <label 
              htmlFor="description" 
              className="block text-xs font-medium text-gray-700 mb-1"
            >
              Description
            </label>
            <textarea
              id="description"
              name="description"
              placeholder="Brief description"
              value={formData.description}
              onChange={handleChange}
              required
              rows="2"
              disabled={isSubmitting}
              className="w-full px-2 py-1 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-blue-500 resize-none disabled:bg-gray-100"
            />
          </div>
          
          <div className="grid grid-cols-2 gap-3">
            <div>
              <label 
                htmlFor="amount" 
                className="block text-xs font-medium text-gray-700 mb-1"
              >
                Amount
              </label>
              <textarea
                id="amount"
                name="amount"
                placeholder="$"
                value={formData.amount}
                onChange={handleChange}
                required
                rows="1"
                disabled={isSubmitting}
                className="w-full px-2 py-1 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-blue-500 resize-none disabled:bg-gray-100"
              />
            </div>
            
            <div>
              <label 
                htmlFor="deadline" 
                className="block text-xs font-medium text-gray-700 mb-1"
              >
                Deadline
              </label>
              <input
                type="date"
                id="deadline"
                name="deadline"
                value={formData.deadline}
                onChange={handleChange}
                required
                disabled={isSubmitting}
                className="w-full px-2 py-1 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-blue-500 disabled:bg-gray-100"
              />
            </div>
          </div>

          <div>
            <label 
              htmlFor="requirements" 
              className="block text-xs font-medium text-gray-700 mb-1"
            >
              Requirements
            </label>
            <textarea
              id="requirements"
              name="requirements"
              placeholder="Requirements to apply"
              value={formData.requirements}
              onChange={handleChange}
              required
              rows="2"
              disabled={isSubmitting}
              className="w-full px-2 py-1 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-blue-500 resize-none disabled:bg-gray-100"
            />
          </div>

            
          <div>
            <label 
              htmlFor="application_link" 
              className="block text-xs font-medium text-gray-700 mb-1"
            >
              Application Link
            </label>
            <input
              type="url"
              id="application_link"
              name="application_link"
              placeholder="https://example.com/apply"
              value={formData.application_link}
              onChange={handleChange}
              required
              disabled={isSubmitting}
              className="w-full px-2 py-1 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-blue-500 disabled:bg-gray-100"
            />
          </div>
          
          <div className="pt-2">
            <button 
              type="submit"
              disabled={isSubmitting}
              className="w-full bg-green-500 text-white py-2 rounded-md hover:bg-green-600 transition-colors text-sm font-semibold shadow-md focus:outline-none focus:ring-1 focus:ring-green-400 disabled:bg-green-300 disabled:cursor-not-allowed"
            >
              {isSubmitting ? 'Submitting...' : 'Submit Scholarship'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default ScholarshipForm;