from src.models.dto.restaurant import RestaurantRequestFullModel, RestaurantGeoSearch, RestaurantRequestUpdateModel, \
    GeoSearchResult


def create() -> tuple[RestaurantRequestUpdateModel, RestaurantRequestUpdateModel]:
    rest1 = RestaurantRequestUpdateModel(
        owner_id=1,
        name='kfc',
        main_photo='photo.jpg',
        photos=['photo.jpg', 'pic.jpg', 'citty.jpg'],
        orig_phone='77777777777',
        wapp_phone='77777777777',
        location=f"SRID=4326;POINT(125.6 10.1)",
        address={"type": "Feature",
                 "geometry":
                     {"type": "Point",
                      "coordinates": [125.6, 10.1]},
                 "properties":
                     {"name": "Dinagat Islands"}},
        categories=[2, 3]
    )
    rest2 = RestaurantRequestUpdateModel(
        owner_id=1,
        name='burger_king',
        main_photo='photo.jpg',
        photos=['photo.jpg', 'pic.jpg', 'citty.jpg'],
        orig_phone='77777777777',
        wapp_phone='77777777777',
        location=f"SRID=4326;POINT(145.6 80.1)",
        address={"type": "Feature",
                 "geometry":
                     {"type": "Point",
                      "coordinates": [145.6, 80.1]},
                 "properties":
                     {"name": "Dinagat Islands"}},
        categories=[2]
    )
    return rest1, rest2

def restaurants() -> tuple[RestaurantRequestFullModel, RestaurantRequestFullModel]:
    rest1 = RestaurantRequestFullModel(
        owner_id=1,
        name='kfc',
        main_photo='photo.jpg',
        photos=['photo.jpg', 'pic.jpg', 'citty.jpg'],
        orig_phone='77777777777',
        wapp_phone='77777777777',
        location=f"SRID=4326;POINT(125.6 10.1)",
        address={"type": "Feature",
                 "geometry":
                     {"type": "Point",
                      "coordinates": [125.6, 10.1]},
                 "properties":
                     {"name": "Dinagat Islands"}},
        categories=["Суши", "Пицца"]
    )
    rest2 = RestaurantRequestFullModel(
        owner_id=1,
        name='burger_king',
        main_photo='photo.jpg',
        photos=['photo.jpg', 'pic.jpg', 'citty.jpg'],
        orig_phone='77777777777',
        wapp_phone='77777777777',
        location=f"SRID=4326;POINT(145.6 80.1)",
        address={"type": "Feature",
                 "geometry":
                     {"type": "Point",
                      "coordinates": [145.6, 80.1]},
                 "properties":
                     {"name": "Dinagat Islands"}},
        categories=["Суши"]
    )
    return rest1, rest2

def get_search_result_from_repo():
    return [
        GeoSearchResult(id=1, name='kfc', main_photo='photo.jpg', distance=0, category=[2, 3], rating=None),
        GeoSearchResult(id=2, name='kfc', main_photo='photo.jpg', distance=0, category=[2, 3], rating=None),
        GeoSearchResult(id=3, name='kfc', main_photo='photo.jpg', distance=0, category=[2, 3], rating=None)
    ]

def get_search_result():
    return [
        RestaurantGeoSearch(id=1, name='kfc', main_photo='photo.jpg', distance=0, category=["Суши", "Пицца"], favourite_flag=False, rating=None),
        RestaurantGeoSearch(id=2, name='kfc', main_photo='photo.jpg', distance=0, category=["Суши", "Пицца"], favourite_flag=False, rating=None),
        RestaurantGeoSearch(id=3, name='kfc', main_photo='photo.jpg', distance=0, category=["Суши", "Пицца"], favourite_flag=False, rating=None),
    ]