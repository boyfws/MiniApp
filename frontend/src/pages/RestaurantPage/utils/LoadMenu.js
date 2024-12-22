import fetchMenuForRest from "../../../api/fetchMenuForRest";

const GetLoadMenu = (setMenuLoading, id, setMenu) => () => {
    async function fetchData() {
        const menu_query = await fetchMenuForRest(id);
        if (!menu_query.error) {
            setMenu(menu_query.data);
            setMenuLoading(false);

        }

    }
    fetchData()
}

export default GetLoadMenu;