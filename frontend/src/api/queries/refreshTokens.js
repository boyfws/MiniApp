async function refreshTokens() {
    const refreshToken = sessionStorage.getItem('refresh_token');

    try {
        const refreshResponse = await fetch('/api/v1/jwt/refresh/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({"data_check_string": refreshToken}),
            }
        );
        if (refreshResponse.status !== 200) {
            return {"error": true}
        }
        const new_tokens_query = await refreshResponse.json();

        sessionStorage.setItem('access_token', new_tokens_query.access_token)
        sessionStorage.setItem('refresh_token', new_tokens_query.refresh_token)
        return {"error": false}

    }
    catch (error) {
        return {"error": true}

    }
}

export default refreshTokens;