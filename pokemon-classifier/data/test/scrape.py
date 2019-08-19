from urllib.request import Request, urlopen
from selenium import webdriver
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException

test_path = '/Users/tanya/PycharmProjects/Webscraping/pokemon-classifier/data/test/'

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument("--test-type")
options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
chrome_driver_binary = "/usr/local/bin/chromedriver"


def check_xpath(xpath):
    """
    Returns True if xpath exists, and false otherwise.
    :param xpath: Xpath whose existence has to be checked.
    :return: True or False.
    """
    try:
        driver_.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True


def file_name(image_url):
    """
    Returns the filename of the image
    :param image_url: url of the image
    :return: file name on the basis of pokemon name
    """
    url_split = image_url.split("/")
    fname = url_split[-1]
    if '.jpg' in fname:
        fname = fname[:-4]
    return fname


if __name__ == "__main__":
    driver_ = webdriver.Chrome(chrome_driver_binary, chrome_options=options)
    driver_.get('https://pokemondb.net/pokedex/national')

    delay = 3  # seconds
    try:
        driver_.set_page_load_timeout(100)
        myElem = WebDriverWait(driver_, delay).until(EC.presence_of_element_located((By.XPATH, '/html/body/main/div[9]/div[88]/span[1]/a/img')))
        print("Page is ready!")
    except TimeoutException:
        print("Loading took too much time!")

    href_links = driver_.find_elements_by_class_name('ent-name')
    print(len(href_links))

    links = []
    for href in href_links:
        links.append(href.get_attribute('href'))

    Name_elem = []
    Primary_type_elem = []
    Secondary_type_elem = []
    Generation_elem = []
    aka_elem = []
    image = []
    Name = []
    Primary_type = []
    Secondary_type = []
    Generation = []
    aka = []
    urls = []

    for link in links:
        driver_.get(link)
        delay = 3  # seconds
        try:
            driver_.set_page_load_timeout(200)
            myElem = WebDriverWait(driver_, delay).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/main/nav[2]')))
            print("Page is ready!")
        except TimeoutException:
            print("Loading took too much time!")

        Name_elem.append(driver_.find_element_by_xpath('/html/body/main/div[1]/div[1]/p/em'))
        Name.append(Name_elem[-1].text)

        Primary_type_elem.append(driver_.find_element_by_xpath('/html/body/main/div[1]/div[1]/p/a[1]'))
        Primary_type.append(Primary_type_elem[-1].text)
        if check_xpath('/html/body/main/div[1]/div[1]/p[1]/a[2]'):
            Secondary_type_elem.append(driver_.find_element_by_xpath('/html/body/main/div[1]/div[1]/p[1]/a[2]'))
            Secondary_type.append(Secondary_type_elem[-1].text)
        else:
            Secondary_type_elem.append('None')
            Secondary_type.append('None')

        Generation_elem.append(driver_.find_element_by_xpath('/html/body/main/div[1]/div[1]/p/abbr'))
        Generation.append(Generation_elem[-1].text)

        aka_elem.append(driver_.find_element_by_xpath('/html/body/main/div[1]/div[1]/p/q'))
        aka.append(aka_elem[-1].text)

        if check_xpath('//*[@class="tabs-panel-list"]/div[1]/div[1]/div[1]/p[1]/a'):
            image.append(driver_.find_element_by_xpath('//*[@class="tabs-panel-list"]/div[1]/div[1]/div[1]/p[1]/a'))
            urls.append(image[-1].get_attribute('href'))
        elif check_xpath('//*[@class="tabs-panel-list"]/div[1]/div[1]/div[1]/p[1]/img'):
            image.append(driver_.find_elements_by_xpath('//*[@class="tabs-panel-list"]/div[1]/div[1]/div[1]/p[1]/img'))
            urls.append(image[-1][0].get_attribute('src'))

    print("\n#################################\n")

    driver_.close()

    for url in urls:
        req = Request(url, headers={'User-Agent': 'Chrome/41.0.2228.0'})
        resource = urlopen(req)
        output = open(file_name(url) + ".png", "wb")
        output.write(resource.read())
        output.close()

    print("@@@@@@@@@@@@@@@@@")

    poke_dict = {'Name': Name, 'Primary Type': Primary_type, 'Secondary Type': Secondary_type, 'Generation': Generation,
                 'Other name': aka}
    poke_df = pd.DataFrame.from_dict(poke_dict)
    poke_df.insert(1, 'id', range(1, len(poke_df)+1))
    poke_df.to_csv(test_path + 'pokemondb.csv')

    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print(poke_df)
