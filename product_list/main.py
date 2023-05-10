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

# variable declare
product_name = []
product_link = []

# setup driver
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options, )
driver.get(prepareQuery(query_str))

# find number of pages
page_info = WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.CLASS_NAME, 's-pagination-item'))
)
print('pagination: ', page_info[-2].text)
total_page = int(page_info[-2].text)


# scrapping
for i in range(1, total_page):
    driver.get(prepareQuery(query_str))
    items = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@data-component-type, "s-search-result")]'))
    )
    for item in items:
        product_link = item.find_element(By.XPATH, './/a[@class="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"]').get_attribute("href")
        product_name = item.find_element(By.XPATH, './/a[@class="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"]//span')

        prod_name = product_name.text.replace("'", "'\'")
        curs.execute(f"insert into product_list(product_title, product_link) values('{prod_name}', '{product_link}')")
        conn.commit()

driver.quit()