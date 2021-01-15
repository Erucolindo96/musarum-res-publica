import logging

database = {
    'path': '/home/krzysztof/PycharmProjects/musarum-res-publicae/data/senatores.db'
}
interpellations = {
    'file_path': '/home/krzysztof/PycharmProjects/musarum-res-publicae/data/interpelacje-processed.csv'
}
logs = {
    'level': logging.DEBUG
}

voivodeship = {
    'path': '/home/krzysztof/PycharmProjects/musarum-res-publicae/data/wojewodztwa.csv'
}

county = {
    'path': '/home/krzysztof/PycharmProjects/musarum-res-publicae/data/powiaty.csv'
}

settles = {
    'dir_path': '/Users/michal/STUDIA/TASS/projekt 2/musarum-res-publica/data/settles',
    'files': ['dolnoslaskie.csv', 'krakowskie.csv', 'kujawskie.csv', 'lubelskie.csv', 'lubuskie.csv', 'ludzkie.csv',
              'mazowieckie.csv', 'opolskie.csv', 'podkarpackie.csv', 'podlaskie.csv', 'pomorskie.csv', 'slaskie.csv',
              'swiatokrzyskie.csv', 'vorpommern.csv', 'warminskie.csv', 'wielkopanskie.csv']
}

election_districts = {
    'path': '/home/krzysztof/PycharmProjects/musarum-res-publicae/data/okregi_wyborcze.csv'
}


def create_config():
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logs['level'])


create_config()
