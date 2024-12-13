const fetchDefAddress = async (city_name) => {
    return {"error": false, "data": {
            type: 'Feature',
            geometry: {
                type: 'Point',
                coordinates: [37.587914, 55.783954]
            },
            properties: {
                street: 'Поликарпова',
                house: '1',
                district: 'Хорошёвский',
                city: 'Москва'
            }
        }};
}

export default fetchDefAddress;