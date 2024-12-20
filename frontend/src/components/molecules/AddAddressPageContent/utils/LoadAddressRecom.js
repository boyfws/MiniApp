import fetchAddressRec from "../../../../api/fetchAddressRec";

const GetLoadAddressRecom = (SetRecommendations,
                             searchString,
                             DefAddress) => () => {

    async function fetchData() {
        let coords = DefAddress.geometry.coordinates
        const rec_query = await fetchAddressRec(searchString, coords[0], coords[1])
        if (!rec_query.error) {
            SetRecommendations(rec_query.data)
        }
    }
    if (searchString !== "") {
        fetchData();
    }
    else {
        SetRecommendations([])
    }
}


export default GetLoadAddressRecom;