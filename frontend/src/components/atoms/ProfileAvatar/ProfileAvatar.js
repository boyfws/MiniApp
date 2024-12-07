// Css
import "./ProfileAvatar.css";

// Ext lib
import React from "react";
import { Button } from "@telegram-apps/telegram-ui";
import { useHistory } from "react-router-dom";

// Handlers
import GetHandleProfileClick from './utils/hadleProfileClick';

// Icons
import Icon24Profile from "../../_icons/Icon24Profile";


const ProfileAvatar = ({ setScrollPositionY }) => {
    const history = useHistory();
    
    const handleProfileClick = GetHandleProfileClick(setScrollPositionY, history);


    return (
        <Button 
            size="s" 
            mode="bezeled" 
            onClick={handleProfileClick}
            className='profile-avatar' >
            <Icon24Profile  className='icon'/>
        </Button>
    );
}

export default ProfileAvatar;
