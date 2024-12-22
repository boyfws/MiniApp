
// Post запрос к серверу
const verificateInitData = async (initData) => {
    const url = `/api/v1/jwt/login/?data_check_string=${initData}`
    try {
       const data = await fetch(url, {method: 'POST'})
       const ret = await data.json()


       return {error: false, data: ret}

    }
    catch (error) {
        return {error: true, data: null}
    }
}


export default verificateInitData