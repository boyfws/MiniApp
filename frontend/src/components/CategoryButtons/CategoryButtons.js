import React, { useState, useContext } from 'react';
import { Button } from '@telegram-apps/telegram-ui';
import './CategoryButtons.css';
import GetHandleCategorySelect from "../../handlers/handleCategorySelect";

import { CategoriesContext } from "../../Contexts/CategoriesContext";

const CategoryButton = ({ category, onClick }) => {
  const [isPressed, setIsPressed] = useState(false); // Локальное состояние кнопки

  const handleClick = () => {
    setIsPressed(!isPressed); // Мгновенное изменение состояния
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

const CategoryButtons = ({ setSelectedCategories }) => {
  const { categories } = useContext(CategoriesContext);
  const onCategorySelect = GetHandleCategorySelect(setSelectedCategories)

  return (
    <div className="category-buttons-wrapper">
      <div className="category-buttons">
        {categories.map((category, index) => (
          <CategoryButton
            key={index}
            category={category}
            onClick={onCategorySelect} // Передаем функцию для обработки выбора категории
          />
        ))}
      </div>
    </div>
  );
};

export default CategoryButtons;
