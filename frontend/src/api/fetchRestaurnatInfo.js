import GET_query from "./queries/GET_query";


const fetchRestaurnatInfo = async (rest_id, user_id) => {
    const url = `/api/v1/Restaurant/get_by_id/${rest_id}/${user_id}`
    return await GET_query(url, {}, 2, 10)
}


export default fetchRestaurnatInfo;