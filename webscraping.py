import bs4
import util

def scrape(var_list):
    '''
    returns tuple with three strings
    '''

def get_description(variable):
    url = "https://ourworldindata.org/grapher/" + variable

def get_soup(absolute_url):
    '''
    Converts a url into a BeautifulSoup object.

    Input: 
        absolute_url(string): the url we want to turn into a bs object

    Returns: BeautifulSoup
    '''

    r = util.get_request(absolute_url)
    if r is None:
        return None
    html_string = util.read_request(r)
    if html_string is None:
        return None
    soup = bs4.BeautifulSoup(html_string, "html5lib")
    return soup, r
