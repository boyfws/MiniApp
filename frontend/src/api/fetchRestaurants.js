import GET_query from "./queries/GET_query";

const fetchRestaurants = async (id, coordinates) => {
    const url = `/api/v1/Restaurant/get_by_geo/${coordinates[0]}/${coordinates[1]}/${id}`
    const delay = 10
    const retries = 5

    return await GET_query(url, {}, retries, delay);
  }

export default fetchRestaurants