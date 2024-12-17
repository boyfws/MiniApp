import GET_query from "./queries/GET_query";

const fetchDefAddress = async (city_name) => {
    const path = `/api/v1/YandexApi/get_city_translation/${city_name}`
    const retries = 2
    const delay = 20
    return await GET_query(path, {}, retries, delay);
}

export default fetchDefAddress;