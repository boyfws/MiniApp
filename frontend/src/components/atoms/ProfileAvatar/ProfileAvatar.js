import React from "react";
import "./ProfileAvatar.css";
import { Button } from "@telegram-apps/telegram-ui";
import Icon24Profile from "../../../icons/Icon24Profile";
import GetHandleProfileClick from '../../../handlers/hadleProfileClick';


const ProfileAvatar = ({ setScrollPositionY, history }) => {
    
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
