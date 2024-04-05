import React from 'react';
import { LoadingContainer, Spinner, LoadingMessage } from './LoadingSpinner.styles';

const LoadingSpinner = () => {
  return (
    <LoadingContainer>
      <Spinner />
      <LoadingMessage>Loading...</LoadingMessage>
    </LoadingContainer>
  );
};

export default LoadingSpinner;