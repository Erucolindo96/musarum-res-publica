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


def create_config():
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logs['level'])


create_config()
