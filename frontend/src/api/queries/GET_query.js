/**
 * Функция для выполнения HTTP-запроса с использованием Fetch API.
 * Возвращает объект с полями `error` (логическое значение) и `data` (данные или сообщение об ошибке).
 * 
 * @param {string} url - URL для выполнения запроса.
 * @param {Object} options - Опции для Fetch API (например, метод, заголовки, тело запроса).
 * @param {number} retries - Количество повторных попыток в случае ошибки.
 * @param {number} delay - Задержка в миллисекундах между повторными попытками.
 * @param {Array} retryOnErrors - Список кодов ошибок, при которых следует повторить запрос. Если не указан, повторные попытки будут выполняться при любой ошибке.
 * @returns {Promise<{error: boolean, data: any}>} - Объект с результатом запроса.
 */

async function fetchWithRetry(url, options = {}, retries = 3, delay = 1000, retryOnErrors = []) {
    // Устанавливаем метод GET, если он не указан
    if (!options.method) {
        options.method = 'GET';
    }

    let attempt = 0;

    while (attempt < retries) {
        try {
            const response = await fetch(url, options);

            if (response.ok) {
                const data = await response.json();
                return { error: false, data };
            } else {
                const errorCode = response.status;
                console.error(`Ошибка при запросе ${url}: Код ошибки ${errorCode}`);

                if (retryOnErrors.length === 0 || retryOnErrors.includes(errorCode)) {
                    attempt++;
                    if (attempt < retries) {
                        console.log(`Повторная попытка ${attempt + 1} через ${delay} мс...`);
                        await new Promise(resolve => setTimeout(resolve, delay));
                    } else {
                        return { error: true, data: `Ошибка: ${errorCode}` };
                    }
                } else {
                    return { error: true, data: `Ошибка: ${errorCode}` };
                }
            }
        } catch (error) {
            console.error(`Ошибка при запросе ${url}: ${error.message}`);
            attempt++;
            if (attempt < retries) {
                console.log(`Повторная попытка ${attempt + 1} через ${delay} мс...`);
                await new Promise(resolve => setTimeout(resolve, delay));
            } else {
                return { error: true, data: error.message };
            }
        }
    }

    return { error: true, data: 'Превышено количество попыток' };
}

export default fetchWithRetry;