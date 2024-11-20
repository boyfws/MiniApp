from typing import Tuple


async def get_rest_properties(rest_id: int) -> Tuple[str, ...]:
    """
    Возможные выходные значения:
        description
        main_photo
        photos
        website
        ext_serv_1
        ext_serv_2
        ext_serv_3
        tg_link
        inst_link
        vk_link
        orig_phone
        wapp_phone
        menu
        categories
    """
    example_return = ("description", "main_photo", "photos", "website", "tg_link")
    return example_return