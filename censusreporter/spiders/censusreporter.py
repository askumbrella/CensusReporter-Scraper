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
            self.regions = []
            for region in regions:
                self.regions.append(region.strip())

    def start_requests(self):
        # Loop over each region specified above
        for region in self.regions:
            region_url = str(
                'https://censusreporter.org/profiles/86000US'
                + region + '-' + region
            )

            request = scrapy.Request(url=region_url, callback=self.parse)

            # Pass variables to next callback
            request.meta['region_name'] = region
            request.meta['region_url'] = region_url

            yield request

    def parse(self, response):
        self.driver.get(response.meta['region_url'])
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

        yield {
            'Region Name': response.meta['region_name'],
            'Region Url': response.meta['region_url'],
            'Density': density,
            'Income Per Capita': income_per_capita,
            'Household Income': household_income,
            'Population': population,
            'Senior Percentage': senior_percentage,
        }

        # self.driver.close() # acting funky bc we're using selenium + scrappy
