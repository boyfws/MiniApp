import query from "./query";


async function deleteWithRetry(url,
                              options = {},
                              retries = 3,
                              delay = 200,
                              retryOnErrors = []) {
    // Устанавливаем метод GET
    options.method = 'DELETE';

    return await query(url, options, retries, delay, retryOnErrors);

}

export default deleteWithRetry;