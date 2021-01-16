import logging
from os import path

current_file_dir = path.dirname(path.realpath(__file__))
root_dir = path.abspath(path.join(current_file_dir, ".."))

database = {
    'path': path.join(root_dir, 'data/senatores.db')
}
interpellations = {
    'path': path.join(root_dir, 'data/interpelacje-processed.csv')
}
logs = {
    'level': logging.DEBUG
}

voivodeship = {
    'path': path.join(root_dir, 'data/wojewodztwa.csv')
}

county = {
    'path': path.join(root_dir, 'data/powiaty.csv')
}

settles = {
    'dir_path': path.join(root_dir, 'data/settles'),
    'files': ['dolnoslaskie.csv', 'krakowskie.csv', 'kujawskie.csv', 'lubelskie.csv', 'lubuskie.csv', 'ludzkie.csv',
              'mazowieckie.csv', 'opolskie.csv', 'podkarpackie.csv', 'podlaskie.csv', 'pomorskie.csv', 'slaskie.csv',
              'swiatokrzyskie.csv', 'vorpommern.csv', 'warminskie.csv', 'wielkopanskie.csv']
}

election_districts = {
    'path': path.join(root_dir, 'data/okregi_wyborcze.csv')
}


def create_config():
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logs['level'])


create_config()
