import GET_query from "./queries/GET_query";

const FetchAddressFromRec = async (full_name, city, region, street, district, house) => {
    const params = {};

    if (full_name !== null) params.full_name = encodeURIComponent(full_name);
    if (city !== null) params.city = encodeURIComponent(city);
    if (region !== null) params.region = encodeURIComponent(region);
    if (street !== null) params.street = encodeURIComponent(street);
    if (district !== null) params.district = encodeURIComponent(district);
    if (house !== null) params.house = encodeURIComponent(house);

    const queryString = Object.entries(params)
        .map(([key, value]) => `${key}=${value}`)
        .join('&');

    const base_url = "/api/v1/YandexApi/get_geojson_from_address_recommendation/"
    const url = `${base_url}?${queryString}`
    const retries = 4
    const delay = 5
    return await GET_query(url, {}, retries, delay)

}

export default FetchAddressFromRec;