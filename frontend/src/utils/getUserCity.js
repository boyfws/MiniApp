import getUserIp from "./getUserIp";

function getUserCity() {
    return new Promise((resolve, reject) => {
        // Получаем IP-адрес пользователя
        getUserIp()
            .then((ip_query) => {
                if (ip_query.error) {
                    resolve({ error: true, data: null });
                    return;
                }

                const ip = ip_query.data;
                const url = `https://ipapi.co/${ip}/jsonp/?callback=jsonpCallback`; // Указываем имя функции обратного вызова

                window.jsonpCallback = function (response) {
                    delete window.jsonpCallback;

                    if (response && response.city) {
                        resolve({ error: false, data: response.city });
                    } else {
                        resolve({ error: true, data: null });
                    }
                };

                const script = document.createElement('script');
                script.src = url;
                script.onerror = () => {
                    resolve({ error: true, data: null });
                };
                document.body.appendChild(script);
            })
            .catch(() => {
                resolve({ error: true, data: null });
            });
    });
}

export default getUserCity;