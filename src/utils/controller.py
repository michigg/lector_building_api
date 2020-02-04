import logging

from .config_controller import BuildingConfigController
from .models import StairCase, Building, Room

logger = logging.getLogger(__name__)


class BuildingController:
    """
    Offers Room dependend building options
    """

    def __init__(self):
        self.indoor_cc = BuildingConfigController()

    def get_rooms_staircase(self, room: Room, wheelchair=False) -> StairCase or None:
        """
        return the staircase that is used for the given room.
        :param room: room which staircase shall be found
        :param wheelchair:
        :return: the rooms staircase
        """
        building = self.get_rooms_building(room)
        return building.get_rooms_staircase(room) if building else None

    def get_rooms_building(self, room: Room, wheelchair=False) -> Building or None:
        """
        return the building that includes the given room
        :param room: room which building shall be found
        :param wheelchair:
        :return: the rooms building
        """
        for building in self.indoor_cc.buildings:
            if str(building.key).lower() == str(room.building_key).lower():
                return building
        return None
