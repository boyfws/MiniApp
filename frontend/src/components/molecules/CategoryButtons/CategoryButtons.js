// Css
import './CategoryButtons.css';

// Ext lib
import React, {useState, useContext, useEffect} from 'react';

// States
import RestStore from "../../../state_management/stores/RestStore";
import { CategoriesContext } from "../../../state_management/context/Contexts/CategoriesContext";

// Handlers
import GetHandleCategorySelect from "./utils/handleCategorySelect";

// Webhook
import GetSortByCategory from "./utils/SortByCategory";

// Components
import CategoryButton from "../../atoms/CategoryButton/CategoryButton"

const CategoryButtons = ({}) => {
  const [selectedCategories, setSelectedCategories] = useState(new Set())
  const { setFilteredRestaurants, restaurants} = RestStore()
  const { categories } = useContext(CategoriesContext);

  const onCategorySelect = GetHandleCategorySelect(setSelectedCategories)

  const SortByCategory = GetSortByCategory(
      setFilteredRestaurants,
      selectedCategories,
      restaurants
  );

  useEffect(SortByCategory, [selectedCategories, restaurants]);

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
