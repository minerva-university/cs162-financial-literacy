import React, { useState, useEffect } from 'react';
import { getScholarships, postScholarship } from '../services/api';
import ScholarshipCard from '../components/ScholarshipCard';
import ScholarshipDetail from '../components/ScholarshipDetail';
import ScholarshipForm from '../components/ScholarshipForm';
import { Search, Filter, Plus } from 'lucide-react';

const ScholarshipsPage = () => {
  const [scholarships, setScholarships] = useState([]);
  const [filteredScholarships, setFilteredScholarships] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedScholarship, setSelectedScholarship] = useState(null);
  const [isAdding, setIsAdding] = useState(false);
  const [sortCriteria, setSortCriteria] = useState('null');

  useEffect(() => {
    const fetchScholarships = async () => {
      try {
        const scholarshipData = await getScholarships();

        console.log({scholarshipData});

        setScholarships(scholarshipData.scholarships);
        setFilteredScholarships(scholarshipData.scholarships);
      } catch (error) {
        console.error("Failed to fetch scholarships", error);
      }
    };
    fetchScholarships();
  }, []);

  const handleSearch = (e) => {
    const value = e.target.value;
    setSearchTerm(value);
    const filtered = scholarships.filter((scholarship) =>
      scholarship.title.toLowerCase().includes(value.toLowerCase())
    );
    setFilteredScholarships(filtered);
  };

  const handleSort = (e) => {
    const criteria = e.target.value;
    setSortCriteria(criteria);
    const sorted = [...filteredScholarships].sort((a, b) => {
      if (criteria === 'null') return new Date(a.date) - new Date(b.date);
      if (criteria === 'title') return a.title.localeCompare(b.title);
      if (criteria === 'deadline') return new Date(a.deadline) - new Date(b.deadline);
      return 0;
    });
    setFilteredScholarships(sorted);
  };

  const handlePostScholarship = async (newScholarship) => {
    try {
      await postScholarship(newScholarship);
      setIsAdding(false);
      const updatedScholarships = await getScholarships();
      setScholarships(updatedScholarships);
      setFilteredScholarships(updatedScholarships);
    } catch (error) {
      console.error("Failed to post scholarship", error);
    }
  };

  const resetFilters = () => {
    setFilteredScholarships(scholarships);
    setSearchTerm('');
    setSortCriteria('null');
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-800 mb-6">Scholarships</h1>
        
        <div className="flex flex-col md:flex-row gap-4 mb-6">
          <div className="relative flex-grow">
            <input
              type="text"
              placeholder="Search scholarships..."
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
            <Plus size={20} /> Add Scholarship
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
        {filteredScholarships.length > 0 ? (
          filteredScholarships.map((scholarship) => (
            <ScholarshipCard
              key={scholarship.id}
              scholarship={scholarship}
              onClick={() => setSelectedScholarship(scholarship)}
            />
          ))
        ) : (
          <div className="col-span-full text-center text-gray-500 py-8">
            <p className="text-lg">No scholarships available at the moment.</p>
          </div>
        )}
      </div>

      {selectedScholarship && (
        <ScholarshipDetail
          scholarship={selectedScholarship}
          onClose={() => setSelectedScholarship(null)}
        />
      )}

      {isAdding && (
        <ScholarshipForm
          onSubmit={handlePostScholarship}
          onClose={() => setIsAdding(false)}
        />
      )}
    </div>
  );
};

export default ScholarshipsPage;