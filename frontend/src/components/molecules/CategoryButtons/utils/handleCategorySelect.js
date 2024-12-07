const GetHandleCategorySelect = (setSelectedCategories) => (category) => {
    // Сначала обновляем выбранные категории
    setSelectedCategories((prevSelectedCategories) => {
      const updatedSelectedCategories = new Set(prevSelectedCategories);
  
      if (updatedSelectedCategories.has(category)) {
        updatedSelectedCategories.delete(category); 
        console.log(`Убрана категория: ${category}`);
      } else {
        updatedSelectedCategories.add(category);
        console.log(`Добавлена категория: ${category}`);
      }
  
      return updatedSelectedCategories;
    });
  };
  
export default GetHandleCategorySelect;