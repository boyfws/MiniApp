import React from "react";
import "./ProfileAvatar.css";
import { Button } from "@telegram-apps/telegram-ui";


const Icon24Profile = ({ ...restProps }) => (
    <svg
      width="24"
      height="24"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      {...restProps}
    >
      <circle cx="12" cy="8" r="3" fill="currentColor" />
      <path
        fillRule="evenodd"
        clipRule="evenodd"
        d="M12 14c-3.333 0-6 2.667-6 6h12c0-3.333-2.667-6-6-6Z"
        fill="currentColor"
      />
    </svg>
  );

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
