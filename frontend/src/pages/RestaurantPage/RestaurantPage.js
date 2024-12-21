// Css
import './RestaurantPage.css'

// Ext lib
import React, {useEffect, useState} from 'react';
import { useHistory, useParams } from 'react-router-dom';


const RestaurantPage = () => {
  const history = useHistory();
  const id = useParams().id;

  const [RestData, SetRestData] = useState({});

  const [loading, setLoading] = useState(true);
  const [showContent, setShowContent] = useState(false);


  const handleGoBack = () => {
    history.push(`/main`);
    window.Telegram.WebApp.BackButton.hide()
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