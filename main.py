from CountyLoader import CountyLoader
from InterpellationLoader import InterpellationLoader
import config
from VoivodeshipLoader import VoivodeshipLoader


def main_func():
    print('Salve Mundo!')

    # load interpellations and deputies
    loader = InterpellationLoader(
        database_path=config.database['path'],
        parsed_interpellation_file=config.interpellations['file_path'])
    loader.load_to_database()

    # load county and voivodeship info from Teryt
    voivodeship_parser = VoivodeshipLoader(database_file=config.database['path'],
                                           voivodeship_file_path=config.voivodeship['path'])
    voivodeship_parser.load_to_database()
    county_parser = CountyLoader(database_file=config.database['path'], county_file_path=config.county['path'])
    county_parser.load_to_database()


if __name__ == '__main__':
    main_func()
