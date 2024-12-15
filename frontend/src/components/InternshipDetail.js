import React from 'react';
import { X } from 'lucide-react';

const InternshipDetail = ({ internship, onClose }) => {
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm">
      <div className="relative w-full max-w-md mx-4 bg-white rounded-xl shadow-2xl overflow-hidden">
        {/* Close Button */}
        <button 
          onClick={onClose} 
          className="absolute top-4 right-4 text-white hover:text-gray-200 transition-colors"
        >
          <X className="w-6 h-6" />
        </button>

        {/* Internship Header */}
        <div className="bg-gradient-to-r from-blue-500 to-purple-600 p-6">
          <h2 className="text-2xl font-bold text-white">{internship.title}</h2>
        </div>

        {/* Internship Content */}
        <div className="p-6">
          <p className="text-gray-700 mb-6">{internship.description}</p>
          <p className="text-gray-700 mb-6">
            <strong>Requirements:</strong> {internship.requirements}
          </p>
          <p className="text-gray-700 mb-6">
            <strong>Deadline:</strong> {internship.deadline}
          </p>
          
          <a 
            href={internship.application_link} 
            target="_blank" 
            rel="noopener noreferrer"
            className="block w-full text-center bg-blue-600 text-white py-3 rounded-lg hover:bg-blue-700 transition-colors"
          >
            Apply Now
          </a>
        </div>
      </div>
    </div>
  );
};

export default InternshipDetail;