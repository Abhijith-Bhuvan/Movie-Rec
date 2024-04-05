import React from 'react';
import { ResultContainer, Title, Table, TableHead, TableRow, TableHeader, TableData } from './ResultComponent.styles';

const ResultComponent = ({ movieData: movieListData }) => {
  if (!movieListData || movieListData.length === 0) {
    return <div>No movies found.</div>;
  }

  const { director } = movieListData[0];

  return (
    <ResultContainer>
      <Title>Movies directed by {director}</Title>
      <Table>
        <TableHead>
          <TableRow>
            <TableHeader>Title</TableHeader>
            <TableHeader>Year</TableHeader>
            <TableHeader>Genres</TableHeader>
            <TableHeader>IMDb Rating</TableHeader>
          </TableRow>
        </TableHead>
        <tbody>
          {movieListData.map((movie) => (
            <TableRow key={movie.title}>
              <TableData>{movie.title}</TableData>
              <TableData>{movie.year}</TableData>
              <TableData>{movie.genres.join(', ')}</TableData>
              <TableData>{movie.imdbRating}</TableData>
            </TableRow>
          ))}
        </tbody>
      </Table>
    </ResultContainer>
  );
};

export default ResultComponent;