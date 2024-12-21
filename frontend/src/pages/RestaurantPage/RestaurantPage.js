// Css
import './RestaurantPage.css'

// Ext lib
import React, {useEffect, useState} from 'react';
import { useHistory, useParams } from 'react-router-dom';

// Comp
import LoaderWrapperRestPage from "../../components/templates/LoaderWrapperRestPage/LoaderWrapperRestPage";

// Utils
import GetLoadRestData from "./utils/LoadRestData";
import GetHandleGoBack from "./utils/handleGoBack";


const RestaurantPage = () => {
  const history = useHistory();
  const id = useParams().id;

  const [RestData, SetRestData] = useState({});

  const [loading, setLoading] = useState(true);
  const [showContent, setShowContent] = useState(false);

  
  const LoadRestData = GetLoadRestData(
      setLoading,
      id,
      SetRestData
  );


  const handleGoBack = GetHandleGoBack(history);


  useEffect(() => {
      window.Telegram.WebApp.BackButton.onClick(handleGoBack);
      window.Telegram.WebApp.BackButton.show()
  }, [])


  useEffect(LoadRestData, [])


  if (!showContent) {
    return (
        <LoaderWrapperRestPage
            loading={loading}
            setShowContent={setShowContent}
        />
    )
  }

  return (
    <div className="RestaurantPage">


      <h1 style={{ color: 'red', textAlign: 'center' }}>Restaurant Page {id}</h1>


    </div>
  );
};

export default RestaurantPage;