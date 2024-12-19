import fetchCategories from '../../api/fetchCategories'

const GetLoadCateg = (setCategories,
                      setCategoriesLoaded,
                      InitDataLoaded) => () =>  {
    const fetchData = async () => {
        const user_id = sessionStorage.getItem('userId');
        // Init Data точно есть следовательно все окс
        const category_query = await fetchCategories(user_id)
        if (!category_query.error) {
            setCategories(category_query.data)
            setCategoriesLoaded(true)
        }
    }

    if (InitDataLoaded) {
        fetchData()
        console.log("Вызвано получение категорий")
    }

}


export default GetLoadCateg