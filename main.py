# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from zeep import Client
from requests.auth import HTTPBasicAuth, HTTPDigestAuth  # or HTTPDigestAuth, or OAuth1, etc.
from requests import Session
from zeep import Client
from zeep.transports import Transport
from requests_ntlm import HttpNtlmAuth
from InterpellationLoader import InterpellationLoader

def main_func():
    # Use a breakpoint in the code line below to debug your script.
    print('Salve Mundo!')  # Press Ctrl+8 to toggle the breakpoint.

    # session = Session()
    # session.auth = HttpNtlmAuth('TestPubliczny', '1234abcd')
    # session.verify = False
    # client = Client('https://uslugaterytws1test.stat.gov.pl/terytws1.svc?singleWsdl', transport=Transport(session=session))
    # result = client.service.CzyZalogowany()

    loader = InterpellationLoader(database_path='', parsed_interpellation_file='/home/krzysztof/PycharmProjects/musarum-res-publicae/data/interpelacje-processed.csv')
    loader.load_to_database()
    print('dupa123')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main_func()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
