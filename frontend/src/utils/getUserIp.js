function getUserIP() {
    return new Promise((resolve) => {
        let retries = 1; // Количество повторных попыток
        const callbackName = `jsonpCallback_${Date.now()}`;

        function makeRequest() {
            const script = document.createElement('script');
            script.src = `http://edns.ip-api.com/json/?callback=${callbackName}`;

            // Обработчик успешного ответа
            window[callbackName] = (response) => {
                // Удаляем созданный элемент и колбэк
                delete window[callbackName];
                document.body.removeChild(script);

                if (response) {
                    if (response.edns && response.edns.ip) {
                        resolve({"error": false, data: response.edns.ip});
                    } else if (response.dns && response.dns.ip) {
                        resolve({"error": false, data: response.dns.ip});
                    } else {
                        retryOrFail();
                    }
                }
            }
            // Обработчик ошибки загрузки
            script.onerror = () => {
                retryOrFail();
            };

            document.body.appendChild(script);
        }

        function retryOrFail() {
            if (retries === 0) {
                resolve({ "error": true, "data": null });
            } else {
                retries--;
                makeRequest();
            }
        }

        makeRequest();
    });
}

export default getUserIP;
