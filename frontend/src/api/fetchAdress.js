import fetchWithRetry from "../queries/GET_query";


const fetchAdress = async (id) => {
    console.log("Вызвано api адреса")
    return {data: {street: 'Поликарпова', house: '1', district: 'Хорошёвский', city: 'Москва'}, error: false}
}

export default fetchAdress