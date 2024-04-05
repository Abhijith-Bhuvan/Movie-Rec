import React, { useState } from 'react';
import { SearchForm, SearchInput, SearchButton } from './SearchComponent.styles';
import LoadingSpinner from './LoadingSpinner';

const SearchComponent = ({ onSearch }) => {
  const [directorName, setDirectorName] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e) => {
    setIsLoading(true);
    e.preventDefault();
    try {
      const response = await fetch(`/search_director/${directorName}`);
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      const data = await response.json();
      onSearch(data);
    } catch (error) {
      console.error('Error fetching data:', error);
    }
    setIsLoading(false);
  };

  return (
    <>
      <SearchForm onSubmit={handleSubmit}>
        <SearchInput
          type="text"
          value={directorName}
          onChange={(e) => setDirectorName(e.target.value)}
          placeholder="Enter director name"
        />
        <SearchButton type="submit">Search</SearchButton>
      </SearchForm>
      {isLoading && <LoadingSpinner />}
    </>
  );
};

export default SearchComponent;