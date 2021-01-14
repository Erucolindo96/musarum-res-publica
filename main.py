from InterpellationLoader import InterpellationLoader
import config


def main_func():
    print('Salve Mundo!')

    loader = InterpellationLoader(
        database_path=config.database['path'],
        parsed_interpellation_file=config.interpellations['file_path'])
    loader.load_to_database()


if __name__ == '__main__':
    main_func()
