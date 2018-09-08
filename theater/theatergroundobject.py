import typing

from dcs.mapping import Point

NAME_BY_CATEGORY = {
    "power": "Power plant",
    "ammo": "Ammo depot",
    "fuel": "Fuel depot",
    "defense": "AA Defense Site",
    "warehouse": "Warehouse",
}

ABBREV_NAME = {
    "power": "PLANT",
    "ammo": "AMMO",
    "fuel": "FUEL",
    "defense": "AA",
    "warehouse": "WARE",
}


class TheaterGroundObject:
    object_id = 0
    cp_id = 0
    group_id = 0
    heading = 0
    location = None  # type: typing.Collection[int]
    category = None  # type: str

    def __init__(self, category, cp_id, group_id, object_id, location, heading):
        self.category = category
        self.cp_id = cp_id
        self.group_id = group_id
        self.object_id = object_id
        self.location = location
        self.heading = heading

    @property
    def string_identifier(self):
        return "{}|{}|{}|{}".format(self.category, self.cp_id, self.group_id, self.object_id)

    @property
    def position(self) -> Point:
        return Point(*self.location)

    @property
    def name_abbrev(self) -> str:
        return ABBREV_NAME[self.category]

    def __str__(self):
        return NAME_BY_CATEGORY[self.category]

    def matches_string_identifier(self, id):
        return self.string_identifier == id