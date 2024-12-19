import GET_query from "./queries/GET_query";

const fetchAddressRec = async (text, lon, lat) => {
    const baseUrl = '/api/v1/YandexApi/get_address_suggestion/';
    const textParam = encodeURIComponent(text); // Кодируем текст для безопасности


    let queryString = `?text=${textParam}`;

    if (lon !== null && lat !== null) {
        queryString += `&lon=${lon}&lat=${lat}`;
    }

    const fullUrl = `${baseUrl}${queryString}`;
    return await GET_query(fullUrl, {}, 1, 2);
}


export default fetchAddressRec;