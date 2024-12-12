import getUserCity from "../../../utils/getUserCity";
import fetchDefAddress from "../../../api/fetchDefAddress";

const GetLoadDefAddress = (InitDataLoaded, setDefAddress) => () => {
    const fetchData = async () => {
        const tg_storage = window.Telegram.WebApp.CloudStorage
        tg_storage.getItem("last_address", async (err, data) => {
            if (!err) {
                setDefAddress(data)
            }
            else {
                const city_eng_query = await getUserCity()
                if (!city_eng_query.error) {
                    const def_address_query = await fetchDefAddress(city_eng_query.data)
                    if (!def_address_query.error) {
                        setDefAddress(def_address_query.data)

                    }
                }

            }

        })

    }
    if (InitDataLoaded) {
        fetchData()
    }
};


export default GetLoadDefAddress;
