import React, { useState } from 'react';
import { Container, Heading } from './ParentComponent.styles';

import SearchComponent from '../SearchComponent/SearchComponent';
import ResultComponent from '../ResultComponent/ResultComponent';

const ParentComponent = () => {
  const [movieListData, setMovieListData] = useState([]);

  const handleSearch = (data) => {
    setMovieListData(data);
  };

  return (
    <Container>
      <Heading>Director's Movies Search</Heading>
      <SearchComponent onSearch={handleSearch} />
      {movieListData.length > 0 && <ResultComponent movieData={movieListData} />}
    </Container>
  );
};

export default ParentComponent;