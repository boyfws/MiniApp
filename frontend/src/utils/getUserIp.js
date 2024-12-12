async function getUserIP() {
    let retries = 1; // Количество повторных попыток

    while (retries >= 0) {
        try {
            const response = await fetch('http://www.geoplugin.net/json.gp');

            const data = await response.json();
            return {"error": false, data: data.geoplugin_request} // Возвращаем IP-адрес
        } catch (error) {
            if (retries === 0) {
                return {"error": true, "data": null};
            }
            retries--;
        }
    }
}

export default getUserIP;