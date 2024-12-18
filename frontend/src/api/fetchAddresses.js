import GET_query from "./queries/GET_query";


const fetchAddresses = async (id) => {
    const url = `api/v1/AddressesForUser/get_all_addresses/${id}`
    const retries = 2
    const delay = 20;

    return await GET_query(url, {}, retries, delay);

}

export default fetchAddresses



