# roofis_parser = reqparse.RequestParser()
# roofis_parser.add_argument('start_date', required=True,
#                            type=inputs.regex('^([12]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01]))$'),
#                            help='date from which free rooms are to be searched for')
# roofis_parser.add_argument('start_time', required=True,
#                            type=inputs.regex('^(?:[01]\d|2[0123]):(?:[012345]\d)$'),
#                            help='time from which free rooms are to be searched for')
# roofis_parser.add_argument('min_size', type=int, help='filter room by minumum room size')
# roofis_parser.add_argument('location', type=str, help='filter rooms by location')
# roofis_parser.add_argument('building_key', type=str, help='filter rooms by building key')
from flask_restplus import reqparse, inputs

buildings_parser = reqparse.RequestParser()
buildings_parser.add_argument('coord',
                              type=list,
                              action='split',
                              help='lat,lon coordinates')
