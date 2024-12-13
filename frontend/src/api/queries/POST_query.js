import query from "./query";

async function postWithRetry(url,
                             body,
                             options = {},
                             retries = 3,
                             delay = 1000,
                             retryOnErrors = []) {
    // Устанавливаем метод POST и добавляем тело запроса
    options.method = 'POST';
    options.headers = {
        'Content-Type': 'application/json',
        ...options.headers
    };
    options.body = JSON.stringify(body);
    return await query(url, options, retries, delay, retryOnErrors);
}

export default postWithRetry;