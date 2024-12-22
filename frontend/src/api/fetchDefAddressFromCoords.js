import GET_query from "./queries/GET_query";

const fetchDefAddressFromCoords = async (long, lat) => {
    const url = `/api/v1/YandexApi/get_address_from_coords/${long}/${lat}`
    return GET_query(url, {}, 3, 5)

}

export default fetchDefAddressFromCoords;