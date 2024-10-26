import { Button } from "@telegram-apps/telegram-ui";
import React from "react";
import './Button.css';

const Icon24ChevronUp = ({ ...restProps }) => (
    <svg width="24" height="24" fill="none" xmlns="http://www.w3.org/2000/svg" {...restProps}>
      <path fillRule="evenodd" clipRule="evenodd"
        d="M19.7 16.46a1 1 0 0 1-1.4 0l-6.8-6.8-6.8 6.8a1 1 0 1 1-1.4-1.42l7.5-7.5a1 1 0 0 1 1.4 0l7.5 7.5a1 1 0 0 1 0 1.42Z"
        fill="currentColor" />
    </svg>
  );


const ButtonForScrollToTop = ({ onClick }) => {
    return (
        <Button
            size="s"
            mode="filled"
            onClick={onClick}
            className="scroll-to-top-button"
        >
        <Icon24ChevronUp className="icon"/>
        </Button>
    )
}

export default ButtonForScrollToTop