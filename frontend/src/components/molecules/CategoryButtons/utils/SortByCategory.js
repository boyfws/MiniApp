import intersection_checker from "./intersection_checker";


const GetSortByCategory = (setFilteredRestaurants, selectedCategories, restaurants) => () => {
    const filtered = selectedCategories.size === 0
        ? restaurants
        : restaurants.filter((restaurant) =>
            intersection_checker(selectedCategories, restaurant.category)
        );

    setFilteredRestaurants(filtered);
}

export default GetSortByCategory

