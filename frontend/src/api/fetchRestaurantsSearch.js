import GET_query from "./queries/GET_query";


const fetchRestaurantsSearch = async (id, coordinates, searchQuery) => {
    const searchString = encodeURIComponent(searchQuery)
    const url = `/api/v1/Restaurant/get_by_geo_and_name/${coordinates[0]}/${coordinates[1]}/${searchString}/${id}`


    return await GET_query(url, {}, 2, 5)
}

export default fetchRestaurantsSearch