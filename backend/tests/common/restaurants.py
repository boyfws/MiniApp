from src.models.dto.restaurant import RestaurantRequestFullModel, RestaurantGeoSearch


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
        categories=[1, 2]
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
        categories=[1]
    )
    return rest1, rest2

def get_search_result():
    return [
        RestaurantGeoSearch(id=1, name='kfc', main_photo='photo.jpg', distance=9350589.51547688),
        RestaurantGeoSearch(id=2, name='kfc', main_photo='photo.jpg', distance=9350589.51547688),
        RestaurantGeoSearch(id=3, name='kfc', main_photo='photo.jpg', distance=9350589.51547688),
    ]