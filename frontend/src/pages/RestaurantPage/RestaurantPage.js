import React from 'react';
import { useHistory, useParams } from 'react-router-dom';

import SearchForm from '../../components/atoms/SearchForm/SearchForm';

const RestaurantPage = () => {
  const history = useHistory();
  const id = useParams().id;

  const handleGoBack = () => {
    history.push(`/main`);
  };

  return (
    <div 
    style={
      {backgroundColor: 'var(--tgui--bg_color)',
      padding: 'var(--padding-for-pages)', 
      height: '100vh', 
      width: '100vw'}}>
      <h1 style={{ color: 'red', textAlign: 'center' }}>Restaurant Page {id}</h1>
      <button onClick={handleGoBack}>Go Back</button>
    </div>
  );
};

export default RestaurantPage;