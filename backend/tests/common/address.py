from src.models.dto.address import AddressDTO


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
