from package.additionals import prepareQuery
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import psycopg2

# database connection
conn = psycopg2.connect(
    database="amazon_prod", user='amazon', password='amazon', host='localhost', port= '5432'
)
curs = conn.cursor()
query_str = "iphone x"
url = prepareQuery(query_str)

# variable declare
product_name = []
product_link = []

# setup driver
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options, )
driver.get(url)

# scrapping
items = WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@data-component-type, "s-search-result")]'))
)

driver.quit()