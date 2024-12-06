import fetchCategories from '../api/fetchCategories'

const GetLoadCategWhenRestAreAdded = (setCategories,
                                      setCategoriesLoaded,
                                      RestLoaded) => () =>  {
    const fetchData = async () => {
        const user_id = sessionStorage.getItem('user_id');
        // Адрес мы грузили уже зная id иначе не загрузили бы, след user_id точно определен
        const category_query = await fetchCategories(user_id)
        if (!category_query.error) {
            setCategories(category_query.data)
            setCategoriesLoaded(true)
        }
    }

    if (RestLoaded) {
        fetchData()
        console.log("Вызвано получение категорий")
    }

}


export default GetLoadCategWhenRestAreAdded