const prepare_address_for_display = (geojson) => {
    const address = geojson.properties
    const city = address.city
    const district = address?.district ?? '';
    const street = address?.street ?? '';
    const house = address?.house ?? '';


    if (street) {
        return `${street} ${house}`;
    }
    else if (district) {
        return `${district}`
    }
    else {
        return `г. ${city}`
    }
}


export default prepare_address_for_display;