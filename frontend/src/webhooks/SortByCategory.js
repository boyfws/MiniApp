import intersection_checker from "../utils/intersection_checker";


const GetSortByCategory = (setFilteredRestaurants, selectedCategories, restaurants) => () => {
    setFilteredRestaurants(() => {
      if (selectedCategories.size === 0) {
        return restaurants; 
        }
    
      console.log("Вызвана сортировка");
      return restaurants.filter((restaurant) =>
        intersection_checker(selectedCategories, restaurant.categories)
      );
    }); console.log("Вызвана сортировка");
  }


export default GetSortByCategory

