import GET_query from "./queries/GET_query";

const fetchCategories = async (id) => {
  const path = `/api/v1/Category/get_all_categories/${id}`;
  const retries = 3;
  const delay = 5;
  const cat_query = await GET_query(path, {}, retries, delay);

  if (cat_query.error) {
    return {error: true, data: null};
  }
  else {
    return {error: false, data: cat_query.data.map(item => item.name)};
  }

}

export default fetchCategories