/**
 * Функция для выполнения HTTP POST-запроса с использованием Fetch API и повторными попытками в случае ошибки.
 * Возвращает объект с полями `error` (логическое значение) и `message` (сообщение об ошибке или данные ответа).
 * 
 * @param {string} url - URL для выполнения запроса.
 * @param {Object} body - Тело запроса, которое будет отправлено в формате JSON.
 * @param {Object} options - Опции для Fetch API (например, заголовки). Метод запроса будет автоматически установлен как POST.
 * @param {number} retries - Количество повторных попыток в случае ошибки (по умолчанию 3).
 * @param {number} delay - Задержка в миллисекундах между повторными попытками (по умолчанию 1000 мс).
 * @param {Array} retryOnErrors - Список кодов ошибок, при которых следует повторить запрос. Если не указан, повторные попытки будут выполняться при любой ошибке.
 * @returns {Promise<{error: boolean, message: any}>} - Объект с результатом запроса.
 */
async function postWithRetry(url, body, options = {}, retries = 3, delay = 1000, retryOnErrors = []) {
    // Устанавливаем метод POST и добавляем тело запроса
    options.method = 'POST';
    options.headers = {
        'Content-Type': 'application/json',
        ...options.headers
    };
    options.body = JSON.stringify(body);

    let attempt = 0;

    while (attempt < retries) {
        try {
            const response = await fetch(url, options);

            if (response.ok) {
                const data = await response.json();
                return { error: false, message: data };
            } else {
                const errorCode = response.status;
                console.error(`Ошибка при запросе ${url}: Код ошибки ${errorCode}`);

                if (retryOnErrors.length === 0 || retryOnErrors.includes(errorCode)) {
                    attempt++;
                    if (attempt < retries) {
                        console.log(`Повторная попытка ${attempt + 1} через ${delay} мс...`);
                        await new Promise(resolve => setTimeout(resolve, delay));
                    } else {
                        return { error: true, message: `Ошибка: ${errorCode}` };
                    }
                } else {
                    return { error: true, message: `Ошибка: ${errorCode}` };
                }
            }
        } catch (error) {
            console.error(`Ошибка при запросе ${url}: ${error.message}`);
            attempt++;
            if (attempt < retries) {
                console.log(`Повторная попытка ${attempt + 1} через ${delay} мс...`);
                await new Promise(resolve => setTimeout(resolve, delay));
            } else {
                return { error: true, message: error.message };
            }
        }
    }

    return { error: true, message: 'Превышено количество попыток' };
}

export default postWithRetry;