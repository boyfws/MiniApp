import getUserIp from "./getUserIp";

async function getUserCity() {
    const ip_query = await getUserIp();
    if (!ip_query.error) {
        const ip = ip_query.data;
        const field = 'city';
        const url = `https://ipapi.co/${ip}/${field}/`;
        let retries = 1;

        while (retries >= 0) {
            try {
                const response = await fetch(url);
                const city = await response.text();
                return {"error": false, "data": city};
            } catch (error) {
                if (retries === 0) {
                    return {"error": true, "data": null};
                }
                retries--;
            }
        }
    }
    else {
        return {"error": true, "data": null}
    }

}


export default getUserIp;