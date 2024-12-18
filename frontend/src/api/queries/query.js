import refreshTokens from './refreshTokens';

async function query(url,
                     options = {},
                     retries = 3,
                     delay = 1000,
                     retryOnErrors = []) {


    let attempt = 0;

    while (attempt < retries) {
        try {
            const accessToken = sessionStorage.getItem('accessToken');
            options.headers = {
                ...options.headers,
                'Authorization': `Bearer ${accessToken}`,
            };


            const response = await fetch(url, options);

            if (response.ok) {
                const data = await response.json();
                return { "error": false, "data": data };

            } else {

                // Если ошибка связана с невалидным или истекшим токеном, обновляем токен
                if (response.status === 401) {
                    const newTokensQuery = await refreshTokens()
                    if (newTokensQuery.error) {
                        attempt++; // Чтобы в случае ошибок не попадать в inf loop
                    }
                    continue;
                }

                if (retryOnErrors.length === 0 || retryOnErrors.includes(response.status)) {
                    attempt++;
                    if (attempt < retries) {
                        await new Promise(resolve => setTimeout(resolve, delay));
                    }
                }
            }
        } catch (error) {
            attempt++;
            if (attempt < retries) {
                await new Promise(resolve => setTimeout(resolve, delay));
            }
        }
    }

    return { "error": true, "data": null };
}

export default query;