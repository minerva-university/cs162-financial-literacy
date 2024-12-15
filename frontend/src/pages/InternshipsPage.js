import React, { useState, useEffect } from 'react';
import { getInternships, postInternship } from '../services/api';
import InternshipCard from '../components/InternshipCard';
import InternshipDetail from '../components/InternshipDetail';
import InternshipForm from '../components/InternshipForm';
import { Search, Filter, Plus } from 'lucide-react';

const InternshipsPage = () => {
  const [internships, setInternships] = useState([]);
  const [filteredInternships, setFilteredInternships] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedInternship, setSelectedInternship] = useState(null);
  const [isAdding, setIsAdding] = useState(false);
  const [sortCriteria, setSortCriteria] = useState('null');

  useEffect(() => {
    const fetchInternships = async () => {
      try {
        const internshipData = await getInternships();

        console.log({internshipData});

        setInternships(internshipData.internships);
        setFilteredInternships(internshipData.internships);
      } catch (error) {
        console.error("Failed to fetch internships", error);
      }
    };
    fetchInternships();
  }, []);

  const handleSearch = (e) => {
    const value = e.target.value;
    setSearchTerm(value);
    const filtered = internships.filter((internship) =>
      internship.title.toLowerCase().includes(value.toLowerCase())
    );
    setFilteredInternships(filtered);
  };

  const handleSort = (e) => {
    const criteria = e.target.value;
    setSortCriteria(criteria);
    const sorted = [...filteredInternships].sort((a, b) => {
      if (criteria === 'null') return new Date(a.date) - new Date(b.date);
      if (criteria === 'title') return a.title.localeCompare(b.title);
      if (criteria === 'deadline') return new Date(a.deadline) - new Date(b.deadline);
      return 0;
    });
    setFilteredInternships(sorted);
  };

  const handlePostInternship = async (newInternship) => {
    try {
      await postInternship(newInternship);
      setIsAdding(false);
      const updatedInternships = await getInternships();
      setInternships(updatedInternships);
      setFilteredInternships(updatedInternships);
    } catch (error) {
      console.error("Failed to post internship", error);
    }
  };

  const resetFilters = () => {
    setFilteredInternships(internships);
    setSearchTerm('');
    setSortCriteria('null');
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-800 mb-6">Internships</h1>
        
        <div className="flex flex-col md:flex-row gap-4 mb-6">
          <div className="relative flex-grow">
            <input
              type="text"
              placeholder="Search internships..."
              value={searchTerm}
              onChange={handleSearch}
              className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
          </div>

          <select 
            onChange={handleSort} 
            value={sortCriteria}
            className="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value='null'>Sort</option>
            <option value="title">Sort by Title</option>
            <option value="deadline">Sort by Deadline</option>
          </select>

          <button 
            onClick={resetFilters}
            className="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition-colors"
          >
            Reset Filters
          </button>
        </div>

        <div className="flex gap-4 mb-6">
          <button 
            onClick={() => setIsAdding(true)}
            className="ml-auto px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600 transition-colors flex items-center gap-2"
          >
            <Plus size={20} /> Add Internship
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
        {filteredInternships.length > 0 ? (
          filteredInternships.map((internship) => (
            <InternshipCard
              key={internship.id}
              internship={internship}
              onClick={() => setSelectedInternship(internship)}
            />
          ))
        ) : (
          <div className="col-span-full text-center text-gray-500 py-8">
            <p className="text-lg">No internships available at the moment.</p>
          </div>
        )}
      </div>

      {selectedInternship && (
        <InternshipDetail
          internship={selectedInternship}
          onClose={() => setSelectedInternship(null)}
        />
      )}

      {isAdding && (
        <InternshipForm
          onSubmit={handlePostInternship}
          onClose={() => setIsAdding(false)}
        />
      )}
    </div>
  );
};

export default InternshipsPage;