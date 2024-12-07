const modificate_address_for_displ = (geojson) => {
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


export default modificate_address_for_displ;