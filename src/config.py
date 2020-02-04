import os

API_V1_ROOT = "/api/v1"
BUILDINGS_CONFIG_DIR = "../configs"

BUILDING_KEY_MAP = {"Erba": {'building_keys': ['WE5'], 'geojson_file': ''},
                    "Feki": {'building_keys': ["F21", "FG1", "FG2", "FMA"], 'geojson_file': ''},
                    "Markushaus": {'building_keys': ["M3N", "M3", "MG1", "MG2"], 'geojson_file': ''},
                    "Innenstadt": {'building_keys': ["U2", "U5", "U7"], 'geojson_file': ''}
                    }

UNIVIS_ROOMS_API = os.environ.get("UNIVIS_ROOM_API")
UNIVIS_ALLOCATION_API = os.environ.get("UNIVIS_ALLOCATION_API")
