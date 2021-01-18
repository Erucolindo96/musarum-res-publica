from InterpellationTextProcessor import InterpellationTextProcessor
from src import config
from src.ElectionDistrictsLoader import ElectionDistrictsLoader
from src.InterpellationLoader import InterpellationLoader
from src.DeputyDetailsLoader import DeputyDetailsLoader
from src.VoivodeshipLoader import VoivodeshipLoader
from src.CountyLoader import CountyLoader
from src.SettleLoader import SettleLoader


def main_func():
    print('Salve Mundo!')

    # load interpellations and deputies
    loader = InterpellationLoader(
        database_path=config.database['path'],
        parsed_interpellation_file=config.interpellations['path'])
    loader.load_to_database()

    # load election districts
    districts_loader = ElectionDistrictsLoader(database_file=config.database['path'],
                                               districts_file_path=config.election_districts['path'])
    districts_loader.load()
    districts_loader.save_to_database()
    county_to_district = districts_loader.get_county_to_district_map()

    # load deputy details (party and election district)
    deputy_details_loader = DeputyDetailsLoader(database_file=config.database['path'],
                                                deputy_file_path=config.deputy['path'])
    deputy_details_loader.load_to_database()

    # load county and voivodeship info from Teryt
    voivodeship_parser = VoivodeshipLoader(database_file=config.database['path'],
                                           voivodeship_file_path=config.voivodeship['path'])
    voivodeship_parser.load_to_database()
    county_parser = CountyLoader(database_file=config.database['path'], county_file_path=config.county['path'],
                                 county_to_district=county_to_district)
    county_parser.load_to_database()

    # load settles info
    for file in config.settles['files']:
        settle_path = '{}/{}'.format(config.settles['dir_path'], file)
        settle_parser = SettleLoader(database_file=config.database['path'], settle_file_path=settle_path)
        settle_parser.load_to_database()

    interpellation_processor = InterpellationTextProcessor(database_path=config.database['path'],
                                                           interpellation_batch=config.interpellations['batch_size'])
    interpellation_processor.process_interpellation_content()


if __name__ == '__main__':
    main_func()
