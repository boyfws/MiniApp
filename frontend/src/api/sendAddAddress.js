import postWithRetry from "./queries/POST_query";

const sendAddAddress = async (new_address, id) => {
    const url = `/api/v1/AddressesForUser/add_address/${id}`;
    const retries = 4
    const delay = 5

    return await postWithRetry(url, new_address, {}, retries, delay)


}

export default sendAddAddress;