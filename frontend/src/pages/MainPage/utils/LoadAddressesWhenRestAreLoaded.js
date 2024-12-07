import fetchAdress from "../../../api/fetchAdress";

// Загружает адреса пользователя, если рестораны загружены
const GetLoadAddressesWhenRestAreLoaded = (RestLoaded, setAddressesLoaded, SetAddresses) => () => {
    const fetchData = async () => {
        const user_id = sessionStorage.getItem("user_id");
        const addresses_query = await fetchAdress(user_id);
        if (!addresses_query.error) {
            SetAddresses(addresses_query.data);
            setAddressesLoaded(true);
        }

    }
    if (RestLoaded) {
        fetchData();
        console.log("Загружены адреса")
    }

}

export default GetLoadAddressesWhenRestAreLoaded