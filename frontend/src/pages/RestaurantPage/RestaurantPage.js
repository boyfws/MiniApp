import React from 'react';
import { useHistory, useParams } from 'react-router-dom';

const RestaurantPage = () => {
  const history = useHistory();
  const id = useParams().id;

  const handleGoBack = () => {
    history.push(`/main`);
  };

  return (
    <div>
      <h1 style={{ color: 'red', textAlign: 'center' }}>Restaurant Page {id}</h1>
      <button onClick={handleGoBack}>Go Back</button>
    </div>
  );
};

export default RestaurantPage;