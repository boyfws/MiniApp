// Css
import './ButtonForScrollToTop.css';

// Ext lib
import { Button } from "@telegram-apps/telegram-ui";
import React from "react";

// Icon
import Icon24ChevronUp from '../../_icons/Icon24ChevronUp'


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