const prepare_address_for_display = (geojson) => {
    const address = geojson.properties
    const district = address?.district ?? '';
    const street = address?.street ?? '';
    const house = address?.house ?? '';


    if (street) {
        return `${street} ${house}`;
    }
    else {
        return `${district}`
    }
}


export default prepare_address_for_display;