from dataclasses import dataclass


@dataclass(frozen=True)
class SinglePropInCallBack_INH:
    """
    Свойства, которые могут быть унаследованы и сущ в ед. числе
    """
    description: str = "DESC"
    website: str = "WBST"
    ext_serv_1: str = "EXT1"
    ext_serv_2: str = "EXT2"
    ext_serv_3: str = "EXT3"
    tg_link: str = "TGLINK"
    inst_link: str = "INSTLINK"
    vk_link: str = "VKLINK"
    orig_phone: str = "ORGPHN"
    wapp_phone: str = "WAPHN"
    menu: str = "MNU"


@dataclass(frozen=True)
class SevPropInCallBack_INH:
    """
    Свойства которые могут быть унаследованы и сущ в множ. числе
    """
    categories: str = "CAT"


@dataclass(frozen=True)
class SevPropInCallBack:
    """
    Свойства которые не могут быть унаследованы и сущ в множ числе
    """
    photos: str = "PHTS"


@dataclass(frozen=True)
class SinglePropInCallBack:
    """
    Свойства, которые не могут быть унаследованы и сущ в ед. числе

    """
    main_photo: str = "MPHTO"


@dataclass(frozen=True)
class PropInCallBack_INH(SevPropInCallBack_INH,
                         SinglePropInCallBack_INH):
    pass


@dataclass(frozen=True)
class PropInCallBacks(SevPropInCallBack,
                      SinglePropInCallBack):
    pass



@dataclass(frozen=True)
class NamesForCallback(PropInCallBacks,
                       PropInCallBack_INH):
    switch_to_rest_management: str = "STRM"
    create_new_rest: str = "CNR"
    show_rest_info: str = "SRI"
    stop_rest_adding: str = "SRA"
    inheritance_property_of_rest: str = "IPOR"
    switch_from_inheritance: str = "SFI"
    start: str = "START"
    CONFIRM: str = "CONFIRM"
    SHOW: str = "SHOW"
    adding_rest_conv_mark: str = "ARCV"
    show_prop_for_inh: str = "SPFI"




"""
Колбэки передаются в формате {conv_mark + _}{callback}:{extra_arg},{extra_arg}
conv_mark позволяет отделить нажатия кнопок в рамках одного conversation от других, conv_mark - опциональный аргумент
"""


