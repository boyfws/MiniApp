import query from "./query";

async function fetchWithRetry(url,
                              options = {},
                              retries = 3,
                              delay = 200,
                              retryOnErrors = []) {
    // Устанавливаем метод GET
    options.method = 'GET';

    return await query(url, options, retries, delay, retryOnErrors);

}

export default fetchWithRetry;