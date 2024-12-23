import GET_query from "./queries/GET_query";

const fetchMenuForRest = async (id) => {
    const url = `/api/v1/Menu/get_menu_by_rest_id/${id}`
    const ret = await GET_query(url, {}, 2, 10)

    console.log(ret)
    if (ret.error || ret.data === null) {
        return {error: true, data: null}
    } else {
        return ret
    }

}

export default fetchMenuForRest;