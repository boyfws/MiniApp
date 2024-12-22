
// Post запрос к серверу
const verificateInitData = async (initData) => {
    const url = `/api/v1/jwt/login/?data_check_string=${encodeURIComponent(initData)}`
    try {
       const data = await fetch(url, {method: 'POST'})


        if (!data.ok) {
            throw new Error("Ошибка валидации");
        }

       const ret = await data.json()
       return {error: false, data: ret}

    }
    catch (error) {
        return {error: true, data: null}
    }
};


export default verificateInitData;