import POST_query from "./queries/POST_query";

const sendAddAddress = async (new_address, id) => {
    const url = `/v1/AddressesForUser/add_address/${id}`;
    const options = {
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(new_address),
    }
    const retries = 4
    const delay = 5
    return await POST_query(url, options, retries, delay)


}

export default sendAddAddress;