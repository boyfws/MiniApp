import React from "react";
import "./ProfileAvatar.css";
import { Button } from "@telegram-apps/telegram-ui";
import Icon24Profile from "../../icons/Icon24Profile";


const ProfileAvatar = ({ onClick }) => {
    return (
        <Button 
            size="s" 
            mode="bezeled" 
            onClick={onClick}
            className='profile-avatar' >
            <Icon24Profile  className='icon'/>
        </Button>
    );
}

export default ProfileAvatar;
