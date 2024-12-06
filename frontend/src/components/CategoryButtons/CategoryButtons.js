import React, {useState, useContext, useEffect} from 'react';
import { Button } from '@telegram-apps/telegram-ui';
import './CategoryButtons.css';
import GetHandleCategorySelect from "../../handlers/handleCategorySelect";

import { CategoriesContext } from "../../Contexts/CategoriesContext";

import GetSortByCategory from "../../webhooks/SortByCategory";


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

const CategoryButtons = ({ setFilteredRestaurants, restaurants }) => {
  const [selectedCategories, setSelectedCategories] = useState(new Set())

  const SortByCategory = GetSortByCategory(
      setFilteredRestaurants,
      selectedCategories,
      restaurants
  );


  useEffect(SortByCategory, [selectedCategories, restaurants]);

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
