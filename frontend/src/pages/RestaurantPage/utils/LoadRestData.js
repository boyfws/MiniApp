import fetchRestaurnatInfo from "../../../api/fetchRestaurnatInfo";

const GetLoadRestData = (setLoading, id, setRestData) => () =>  {
    async function fetchData() {
        const user_id = sessionStorage.getItem("userId");
        const rest_data_query =  await fetchRestaurnatInfo(id, user_id)
        console.log(rest_data_query)
        if (!rest_data_query.error) {
            setRestData(rest_data_query.data);
            setLoading(false);
            console.log("Подняли флаг для рестов")
        }

    }
    fetchData()
}

export default GetLoadRestData;