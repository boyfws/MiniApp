const prepare_address_for_display = (geojson) => {
    const address = geojson.properties
    const city = address.city
    const district = address?.district ?? '';
    const street = address?.street ?? '';
    const house = address?.house ?? '';


    if (street && house && (street !== 'None' && house !== 'None')) {
        return `${street} ${house}`;

    } else if (street && street !== 'None') {
        return `${street}`;
    }
    else if (district !== 'None') {
        return `${district}`
    }
    else {
        return `г. ${city}`
    }
}


export default prepare_address_for_display;