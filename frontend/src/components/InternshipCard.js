import React from 'react';
import { BookOpenIcon, ArrowRightIcon } from 'lucide-react';

const InternshipCard = ({ internship, onClick }) => {
  return (
    <div 
      className="bg-white shadow-lg rounded-xl overflow-hidden transition-all duration-300 
                 hover:shadow-xl hover:scale-105 cursor-pointer border border-gray-100 
                 group max-w-sm w-full"
      onClick={onClick}
    >
      <div className="p-6">
        <div className="flex items-center mb-4">
          <BookOpenIcon 
            className="w-8 h-8 text-blue-500 mr-4 group-hover:text-blue-600 
                       transition-colors duration-300"
          />
          <h3 className="text-xl font-semibold text-gray-800 group-hover:text-blue-700 
                         transition-colors duration-300">
            {internship.title}
          </h3>
        </div>
      
        
        <div className="flex items-center justify-between">
          <button 
            className="flex items-center text-blue-500 font-medium 
                       hover:text-blue-700 transition-colors duration-300 
                       group-hover:underline"
          >
            View Details
            <ArrowRightIcon 
              className="ml-2 w-5 h-5 group-hover:translate-x-1 
                         transition-transform duration-300"
            />
          </button>
        </div>
      </div>
    </div>
  );
};

export default InternshipCard;