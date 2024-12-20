// Css
import './RestaurantPage.css'

// Ext lib
import React, {useEffect} from 'react';
import { useHistory, useParams } from 'react-router-dom';


const RestaurantPage = () => {
  const history = useHistory();
  const id = useParams().id;

  const handleGoBack = () => {
    history.push(`/main`);
  };

  useEffect(() => {

      window.Telegram.WebApp.BackButton.onClick(handleGoBack);
      window.Telegram.WebApp.BackButton.show()

  }, [])

  return (
    <div className="RestaurantPage">


      <h1 style={{ color: 'red', textAlign: 'center' }}>Restaurant Page {id}</h1>


    </div>
  );
};

export default RestaurantPage;