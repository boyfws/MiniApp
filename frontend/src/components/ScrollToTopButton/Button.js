import { Button } from "@telegram-apps/telegram-ui";
import React from "react";
import './Button.css';
import Icon24ChevronUp from '../../icons/Icon24ChevronUp'


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