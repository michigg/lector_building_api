import datetime
import json

from flask import Flask, jsonify
from flask_restplus import Api, Resource, reqparse, inputs
from shapely.geometry import Point

from config import API_V1_ROOT
from parser import buildings_parser
from utils.config_controller import BuildingConfigController
from utils.controller import BuildingController
from utils.models import Room

app = Flask(__name__)
api = Api(app=app, doc='/docs', version='1.0', title='Lector Building API',
          description='Lecture Navigator Building API')


@api.route(f'{API_V1_ROOT}/building/')
class ApiBuildings(Resource):

    @api.doc(parser=buildings_parser)
    def get(self):
        """
        Returns list of known buildings
        """

        args = buildings_parser.parse_args()

        coord = [float("".join(arg)) for arg in args.get('coord', [])] if args.get('coord', []) else None
        # TODO: init config controller on server start
        building_c = BuildingConfigController()

        if coord:
            print(coord)

            start_point = Point(*coord)
            building_distances = []
            # TODO: extract methods
            for building in building_c.buildings:
                staircase_distances = []
                for staircase in building.staircases:
                    end_point = Point(staircase.coord)
                    distance = start_point.distance(end_point)
                    staircase_distances.append(distance)
                mean_distance = sum(staircase_distances) / len(staircase_distances)
                building_distances.append({"distance": mean_distance, "building_key": building.key})
                building_distances.sort(key=lambda building_wrapper: building_wrapper["distance"])
            return jsonify([building["building_key"] for building in building_distances])
        else:
            building_keys = building_c.get_building_keys()
            building_keys.sort()
            return jsonify(building_keys)


@api.route(f'{API_V1_ROOT}/building/<building_id>/')
class ApiBuilding(Resource):

    def get(self, building_id):
        """
        Returns the full config of the building specified by id
        """
        building_c = BuildingConfigController()
        building = building_c.get_building_by_key(building_id)
        if building:
            building_json = json.loads(
                json.dumps(building.__dict__, default=lambda o: o.__dict__ if not isinstance(o, (
                    datetime.date, datetime.datetime)) else o.isoformat(), indent=4))
            return jsonify(building_json)
        return jsonify(status_code=400)


@api.route(f'{API_V1_ROOT}/<building_key>/<level>/<number>/')
class ApiRoomsBuilding(Resource):

    def get(self, building_key, level, number):
        """
        Returns the rooms building
        """
        building_c = BuildingController()
        building = building_c.get_rooms_building(Room(building_key, level, number))
        if building:
            building_json = json.loads(
                json.dumps(building.__dict__, default=lambda o: o.__dict__ if not isinstance(o, (
                    datetime.date, datetime.datetime)) else o.isoformat(), indent=4))
            return jsonify(building_json)
        return jsonify(status_code=400)


@api.route(f'{API_V1_ROOT}/<building_key>/staircase/<level>/<number>/')
class ApiRoomsStaircase(Resource):

    def get(self, building_key, level, number):
        """
        Returns the rooms staircase
        """
        building_c = BuildingController()
        staircase = building_c.get_rooms_staircase(Room(building_key, level, number))
        if staircase:
            staircase_json = json.loads(
                json.dumps(staircase.__dict__, default=lambda o: o.__dict__ if not isinstance(o, (
                    datetime.date, datetime.datetime)) else o.isoformat(), indent=4))
            return jsonify(staircase_json)
        return jsonify(status_code=400)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555)
