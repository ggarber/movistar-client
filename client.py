import sys, re, logging
import urllib, mechanize
from BeautifulSoup import BeautifulSoup

TIMEOUT = 60
logger = logging.getLogger('MovistarClient')

class MovistarClient:
    def __init__(self):
        self.__create_opener()

    def __create_opener(self):
        logger.debug('__create_opener')

        br = mechanize.Browser()
        br.set_handle_robots(False)

        #Log information about HTTP redirects and Refreshes.
        #br.set_debug_redirects(True)
        #Log HTTP response bodies (ie. the HTML, most of the time).
        #br.set_debug_responses(True)
        #Print HTTP headers.
        #br.set_debug_http(True)

        self.opener = br

    def login(self, login, password):
        logger.debug('login', login)

        values = {
            'AUTHMETHOD': 'UserPassword',
            'pageGenTime': '9999999999999',
            'usr_password': 'KjhG3Tv51',
            'usr_name': login,
            'pgeac': password,
            'HiddenURI': 'https://www.canalcliente.movistar.es/fwk/cda/controller/CCLI_CW_privado/0,2217,259_0_2326_0_0,00.html'
        }
        data = urllib.urlencode(values)
        self.opener.open('https://sslwb.movistar.es/auth/Login', data, TIMEOUT)

    def status(self):
        logger.debug('status')

        response = self.opener.open('https://www.canalcliente.movistar.es/fwk/cda/controller/CCLI_CW_privado/0,2217,259_34641405_18171___340416085,00.html');
        html = response.read()

        return MovistarClient.parse_status(html)

    def bills(self):
        logger.debug('bills')

        return []

    def services(self):
        logger.debug('services')

        return {}

    @staticmethod
    def parse_status(content):
        soup = BeautifulSoup(content);
        table = soup.find('td', text=re.compile("^[ \t\r\n]+Llamadas[ \t\r\n]+$")).parent.parent.parent

        return {
            'calls': __parse_float(__cell(table, 1, 2).string),
            'calls_cost': __parse_float(__cell(table, 1, 1).string),
            'traffic': __parse_traffic(__cell(table, 2, 3).string)
        }


def __cell(table, row, col):
    """ Extracts a cell from a beautifulsoup table """
    rows = table.findAll('tr')
    cols = rows[row].findAll('td')
    return cols[col]

def __parse_float(str):
    """ Parse float in movistar format
    
    >>> __parse_float("12,2")
    12.2
    """
    return float(str.strip().replace(',','.'))

def __parse_traffic(str):
    """ Parse data traffic in movistar format
    
    >>> __parse_traffic("158.232,3906Kb")
    158232.0
    """
    return float(str.strip().split(",")[0].replace('.',''))

if __name__ == "__main__":
    import doctest
    doctest.testmod()
