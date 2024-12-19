import POST_query from "./queries/POST_query";

const sendAddAddress = async (new_address, id) => {
    const url = `/v1/AddressesForUser/add_address/${id}`;
    const retries = 4
    const delay = 5

    const filteredAddress = {
        ...new_address,
        properties: Object.fromEntries(
            Object.entries(new_address.properties).filter(([key, value]) => value !== null)
        )
    };

    return await POST_query(url, filteredAddress, {}, retries, delay)


}

export default sendAddAddress;