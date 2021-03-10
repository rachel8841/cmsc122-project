import bs4
import requests

def scrape(var_list):
    '''
    returns tuple with three strings
    '''
    x,y,bub = var_list

    return (get_description(x), get_description(y), get_description(bub))


def get_description(variable):
    '''
    Gets the description of one variable
    '''
    url = "https://ourworldindata.org/grapher/" + variable
    soup = get_soup(url)
    description_tag = soup.find("meta", attrs={'name':"description"})
    description = description_tag["content"]
    
    return description
    

def get_soup(url):
    '''
    Converts a url into a BeautifulSoup object.

    Input: 
        url(string): the url we want to turn into a bs object

    Returns: BeautifulSoup
    '''

    html = requests.get(url).text
    soup = bs4.BeautifulSoup(html, "html5lib")
    return soup