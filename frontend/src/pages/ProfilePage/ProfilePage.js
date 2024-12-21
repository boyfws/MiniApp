// Css
import './ProfilePage.css'

// Ext lib
import React, {useEffect} from 'react';
import { useHistory } from 'react-router-dom';

// Comp
import GetHandleGoBackProfilePage from "../RestaurantPage/utils/handleGoBack";


const ProfilePage = () => {
    const history = useHistory();


    const handleGoBack = GetHandleGoBackProfilePage(history);


    useEffect(() => {

        window.Telegram.WebApp.BackButton.onClick(handleGoBack);
        window.Telegram.WebApp.BackButton.show()

    }, [])

  return (
    <div className="ProfilePage">

    </div>
  );
};

export default ProfilePage;