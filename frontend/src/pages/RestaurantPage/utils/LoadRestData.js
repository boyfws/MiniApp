import fetchRestaurnatInfo from "../../../api/fetchRestaurnatInfo";

const GetLoadRestData = (setLoading, id, setRestData) => () =>  {
    async function fetchData() {
        const rest_data_query =  await fetchRestaurnatInfo(id)

        if (!rest_data_query.error) {
            setRestData(rest_data_query.error);
            setLoading(false);
        }

    }
    fetchData()
}

export default GetLoadRestData;