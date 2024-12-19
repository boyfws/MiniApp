// Css
import './CategoryButton.css'

// Ext lib
import React, {useState} from "react";
import { Button } from "@telegram-apps/telegram-ui";


const CategoryButton = ({ category, onClick }) => {
    const [isPressed, setIsPressed] = useState(false); // Локальное состояние кнопки

    const handleClick = () => {
        setIsPressed(!isPressed); // Мгновенное изменение состояния
        window.Telegram.WebApp.HapticFeedback.impactOccurred("light");
        setTimeout(() => {
            onClick(category);
        }, 0);
    };


    return (
        <Button
            className='category-button'
            size="s"
            mode={isPressed ? "bezeled" : "gray"}
            onClick={handleClick}
        >
            {category}
        </Button>
    );
};


export default CategoryButton;