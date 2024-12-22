// Css
import './ProfilePage.css'

// Ext lib
import React, {useEffect} from 'react';
import { useHistory } from 'react-router-dom';

import ProfilePageTemp from "../../components/templates/ProfilePageTemp/ProfilePageTemp";

// Utils
import GetHandleGoBackProfilePage from "./utils/handleGoBackProfilePage";


const ProfilePage = () => {
    const history = useHistory();


    const handleGoBack = GetHandleGoBackProfilePage(history);


    useEffect(() => {

        window.Telegram.WebApp.BackButton.onClick(handleGoBack);
        window.Telegram.WebApp.BackButton.show()

    }, [])

  return (
    <div className="ProfilePage">
        <ProfilePageTemp/>
    </div>
  );
};

export default ProfilePage;