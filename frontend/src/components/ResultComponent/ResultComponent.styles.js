import styled from 'styled-components';

export const ResultContainer = styled.div`
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
`;

export const Title = styled.h2`
  font-size: 2rem;
  font-weight: 600;
  color: #333;
  margin-bottom: 1.5rem;
`;

export const Table = styled.table`
  width: 100%;
  border-collapse: collapse;
  font-family: sans-serif;
  font-size: 0.9rem;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
`;

export const TableHead = styled.thead`
  background-color: #f8f8f8;
`;

export const TableRow = styled.tr`
  &:nth-child(even) {
    background-color: #f2f2f2;
  }
`;

export const TableHeader = styled.th`
  padding: 1rem;
  text-align: left;
  font-weight: 600;
  color: #555;
`;

export const TableData = styled.td`
  padding: 1rem;
  color: #666;
`;