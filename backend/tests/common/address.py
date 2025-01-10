from src.models.dto.address import AddressDTO, GeoJson


def get_addresses() -> tuple[AddressDTO, AddressDTO, AddressDTO, AddressDTO, AddressDTO, AddressDTO]:
    address_1= AddressDTO(
        region="Республика Чечня",
        city="Москва",
        district="Измайловский",
        street="улица Вернадского",
        house='11',
        location="SRID=4326;POINT(37.617 55.755)"
    )
    address_2 = AddressDTO(
        region="Республика Чечня",
        city="Санкт-Петербург",
        district="Красноярск",
        street="улица Аникутина",
        house='12',
        location="SRID=4326;POINT(37.617 55.755)"
    )

    address_3 = AddressDTO(
        region="Республика Чечня",
        city="Москва",
        district="Измайловский",
        street="улица Вернадского",
        house='50',
        location="SRID=4326;POINT(37.617 55.755)"
    )

    address_4 = AddressDTO(
        region="Республика Чечня",
        city="Москва",
        district="Калининский",
        street="улица Аникутина",
        house='13',
        location="SRID=4326;POINT(37.617 55.755)"
    )

    address_5 = AddressDTO(
        region="Республика Чечня",
        city="Москва",
        district="Измайловский",
        street="улица Вернадского",
        house='50',
        location="SRID=4326;POINT(37.617 55.755)"
    )

    address_6 = AddressDTO(
        region="Республика Чечня",
        city="Москва",
        district="Измайловский",
        street="улица Аникутина",
        house='13',
        location="SRID=4326;POINT(37.617 55.755)"
    )
    return address_1, address_2, address_3, address_4, address_5, address_6


def geojson() -> list[GeoJson, GeoJson]:
    model1 = {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [
                37.552687,
                55.777013
            ]
        },
        "properties": {
            "city": "Москва",
            "region": None,
            "street": "улица Поликарпова",
            "district": None,
            "house": "8"
        }
    }

    model2 = {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [
                37.552687,
                55.687013
            ]
        },
        "properties": {
            "city": "Москва",
            "region": None,
            "street": "проспект Вернадского",
            "district": None,
            "house": "12"
        }
    }

    return [
        GeoJson.model_validate(model1, from_attributes=True),
        GeoJson.model_validate(model2, from_attributes=True),
    ]

def get_dicts():
    model1 =  {
        'geometry': {
            'coordinates': [
                37.617,
                 55.755,             ],
             'type': 'Point',
        },
        'properties': {
             'city': 'Санкт-Петербург',
            'district': 'Красноярск',
            'house': '12',
            'region': 'Республика Чечня',
            'street': 'улица Аникутина',
        },
        'type': 'Feature',
    }
    model2 = {
        'geometry': {
            'coordinates': [
                37.617,
                55.755,
            ],
            'type': 'Point',
        },
        'properties': {
            'city': 'Москва',
            'district': 'Измайловский',
            'house': '50',
            'region': 'Республика Чечня',
            'street': 'улица Вернадского',
        },
        'type': 'Feature',
    }
    return [model1, model2]
