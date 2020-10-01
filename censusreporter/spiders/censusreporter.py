import requests
from bs4 import BeautifulSoup
import time
import scrapy
from selenium import webdriver


class CensusReporterSpider(scrapy.Spider):
    name = 'censusreporter'
    allowed_domains = ['censusreporter.com']

    def __init__(self):
        self.driver = webdriver.Remote(
            command_executor='http://0.0.0.0:4444/wd/hub',
            desired_capabilities=webdriver.DesiredCapabilities.FIREFOX
        )

        with open('regions.csv', 'r') as regions:
            self.zip_codes = {}
            for region in regions:
                county_state = region.strip().split(',')
                pg = 1
                has_more = True
                url = 'https://www.zip-codes.com/search.asp'

                self.zip_codes[region] = []
                while has_more:
                    response = requests.get(
                        f'{url}?fld-state={county_state[1]}&'
                        f'fld-county={county_state[0]}&pg={pg}'
                    )

                    soup = BeautifulSoup(response.text)
                    table = soup.find('table', class_='statTable')
                    rows = table.find_all('tr')

                    url_encoded_county = county_state[0] \
                        .replace(" ", "+") \
                        .replace("-", "%2D")

                    href = (
                        f'search.asp?pad=1&fld-state={county_state[1]}&'
                        f'fld-county={url_encoded_county}&'
                        f'pg=1'
                    )

                    for tr in rows[1:]:
                        if not tr.find('td').find('a') or (pg > 1 and
                           not soup.find('a', attrs={'href': href})):
                            has_more = False
                            break

                        self.zip_codes[region].append(
                            tr.find('td').find('a').text
                        )

                    pg += 1

    def start_requests(self):
        # Loop over each region specified above
        for region, zip_codes in self.zip_codes.items():
            for zip_code in zip_codes:
                zip_code_url = str(
                    'https://censusreporter.org/profiles/86000US'
                    + zip_code + '-' + zip_code
                )

                request = scrapy.Request(url=zip_code_url, callback=self.parse)

                # Pass variables to next callback
                request.meta['region'] = region
                request.meta['zip_code'] = zip_code
                request.meta['zip_code_url'] = zip_code_url

                yield request

            time.sleep(1)

    def parse(self, response):
        self.driver.get(response.meta['zip_code_url'])
        senior_percentage_button = self.driver.find_element_by_xpath(
            '//*[@id="chart-pie-demographics-age-distribution_by_category"]\
            /div/div[3]/a[1]'
        )
        senior_percentage_button.click()
        senior_percentage = self.driver.find_element_by_xpath(
            '//*[@id="data-table"]/tbody/tr[3]/td[2]'
        ).text.strip()
        population = self.driver.find_element_by_xpath(
            '//*[@id="cover-profile"]/article/div[1]/div/span/span[1]'
        ).text.strip()

        density = self.driver.find_element_by_xpath(
            '//*[@id="cover-profile"]/article/div[2]/div/span[2]/span[1]'
        ).text.strip()
        income_per_capita = self.driver.find_element_by_xpath(
            '//*[@id="economics"]/div/section[1]/div[1]/a/span/span[1]'
        ).text.strip()
        household_income = self.driver.find_element_by_xpath(
            '//*[@id="economics"]/div/section[1]/div[2]/a/span/span[1]'
        ).text.strip()
        percent_single_family = self.driver.find_element_by_xpath(
            '//*[@id="housing"]/div/section[2]/div[1]/div[1]/div[2]/\
            div[1]/span[2]'
        ).text.strip()

        yield {
            'Region': response.meta['region'].strip(),
            'Zip Code': response.meta['zip_code'],
            'Zip Code Url': response.meta['zip_code_url'],
            'Density': density,
            'Income Per Capita': income_per_capita,
            'Household Income': household_income,
            'Population': population,
            'Senior Percentage': senior_percentage,
            'Percent Single Family Homes': percent_single_family
        }

        # self.driver.close() # acting funky bc we're using selenium + scrappy
