// Css
import './ProfilePage.css'

// Ext lib
import React, {useEffect} from 'react';
import { useHistory } from 'react-router-dom';


const ProfilePage = () => {
    const history = useHistory();


    const handleGoBack = () => {
        history.push(`/main`);
    };


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