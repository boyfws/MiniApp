function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}


const fetchRestaurnatInfo = async (id) => {
    const data = {
        "owner_id": 1,
        "name": "string",
        "main_photo": "string",
        "photos": [
            "string"
        ],
        "ext_serv_link_1": "string",
        "ext_serv_link_2": "string",
        "ext_serv_link_3": "string",
        "ext_serv_rank_1": 10,
        "ext_serv_rank_2": 10,
        "ext_serv_rank_3": 10,
        "ext_serv_reviews_1": 0,
        "ext_serv_reviews_2": 0,
        "ext_serv_reviews_3": 0,
        "tg_link": "string",
        "inst_link": "string",
        "vk_link": "string",
        "orig_phone": "stringstrin",
        "wapp_phone": "stringstrin",
        "location": "string",
        "address": {},
        "categories": [
            0
        ]
    }

    await sleep(500);
    return {error: false, data: data}

}


export default fetchRestaurnatInfo;