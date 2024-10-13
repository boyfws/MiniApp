import React from 'react';
import { Button } from '@telegram-apps/telegram-ui';
import './CategoryButtons.css'; // Подключение CSS

const CategoryButtons = ({ categories, onCategorySelect }) => {
  return (
    <div className="category-buttons-wrapper">
      <div className="category-buttons">
        {categories.map((category, index) => (
          <Button
            key={index}
            mode="filled" // Мера чисто для теста потом цвет подправим
            size="s"
            onClick={() => onCategorySelect(category)}
          >
            {category}
          </Button>
        ))}
      </div>
    </div>
  );
};

export default CategoryButtons;
