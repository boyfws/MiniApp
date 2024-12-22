import DELETE_query from "./queries/DELETE_query";

const deleteAllFavUserRest = async(id) =>  {
    const url = `/api/v1/FavouriteRestaurant/drop_all_user_fav_restaurants/${id}`
    return await DELETE_query(url, {}, 3, 5)

}

export default deleteAllFavUserRest;