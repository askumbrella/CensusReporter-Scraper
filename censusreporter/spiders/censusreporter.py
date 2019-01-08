import scrapy
from selenium import webdriver

class CensusReporterSpider(scrapy.Spider):
    name = 'censusreporter'
    allowed_domains = ['censusreporter.com']

    # regions = ["08002","08003","08004","08007","08009","08012","08021","08026","08029","08030","08031","08033","08034","08035","08043","08045","08049","08059","08078","08081","08083","08084","08089","08091","08102","08103","08104","08105","08106","08107","08108","08109","08110"]
    # bergen
    # regions = ["07010", 
    # "07020", 
    # "07022", 
    # "07024", 
    # "07026", 
    # "07031", 
    # "07057", 
    # "07070", 
    # "07071", 
    # "07072", 
    # "07073", 
    # "07074", 
    # "07075", 
    # "07401", 
    # "07407", 
    # "07410", 
    # "07417", 
    # "07423", 
    # "07430", 
    # "07432", 
    # "07436", 
    # "07446", 
    # "07450", 
    # "07452", 
    # "07458", 
    # "07463", 
    # "07481", 
    # "07495", 
    # "07601", 
    # "07603", 
    # "07604", 
    # "07605", 
    # "07606", 
    # "07607", 
    # "07608", 
    # "07621", 
    # "07624", 
    # "07626", 
    # "07627", 
    # "07628", 
    # "07630", 
    # "07631", 
    # "07632", 
    # "07640", 
    # "07641", 
    # "07642", 
    # "07643", 
    # "07644", 
    # "07645", 
    # "07646", 
    # "07647", 
    # "07648", 
    # "07649", 
    # "07650", 
    # "07652", 
    # "07656", 
    # "07657", 
    # "07660", 
    # "07661", 
    # "07662", 
    # "07663", 
    # "07666", 
    # "07670", 
    # "07675", 
    # "07676", 
    # "07677"]
    regions = ["15007", 
    "15014", 
    "15015", 
    "15017", 
    "15018", 
    "15024", 
    "15025", 
    "15030", 
    "15031", 
    "15034", 
    "15035", 
    "15037", 
    "15044", 
    "15045", 
    "15046", 
    "15049", 
    "15051", 
    "15056", 
    "15064", 
    "15065", 
    "15071", 
    "15076", 
    "15084", 
    "15086", 
    "15090", 
    "15101", 
    "15102", 
    "15104", 
    "15106", 
    "15108", 
    "15110", 
    "15112", 
    "15116", 
    "15120", 
    "15122", 
    "15126", 
    "15129", 
    "15131", 
    "15132", 
    "15133", 
    "15135", 
    "15136", 
    "15137", 
    "15139", 
    "15140", 
    "15142", 
    "15143", 
    "15144", 
    "15145", 
    "15146", 
    "15147", 
    "15148", 
    "15201", 
    "15202", 
    "15203", 
    "15204", 
    "15205", 
    "15206", 
    "15207", 
    "15208", 
    "15209", 
    "15210", 
    "15211", 
    "15212", 
    "15213", 
    "15214", 
    "15215", 
    "15216", 
    "15217", 
    "15218", 
    "15219", 
    "15220", 
    "15221", 
    "15222", 
    "15223", 
    "15224", 
    "15225", 
    "15226", 
    "15227", 
    "15228", 
    "15229", 
    "15232", 
    "15233", 
    "15234", 
    "15235", 
    "15236", 
    "15237", 
    "15238", 
    "15239", 
    "15241", 
    "15243"]

    def __init__(self):
        self.driver = webdriver.Firefox(executable_path=r"/Users/mac/Downloads/geckodriver")
        # Make sure to update path of geckodriver

    def start_requests(self):
        
        # Loop over each region specified above
        for region in self.regions:
            region_url = str('https://censusreporter.org/profiles/86000US' + region + '-' + region)
            
            request = scrapy.Request(url=region_url, callback=self.parse)

            # Pass variables to next callback
            request.meta['region_name'] = region
            request.meta['region_url'] = region_url

            yield request
            
    def parse(self, response):
        
        # Redundant now
        # density = response.xpath('//*[@id="cover-profile"]/article/div[2]/div/span[2]/span[1]').extract()
        # income = response.xpath('').extract()
        
        self.driver.get(response.meta['region_url'])
        senior_percentage_button = self.driver.find_element_by_xpath('//*[@id="chart-pie-demographics-age-distribution_by_category"]/div/div[3]/a[1]')
        senior_percentage_button.click()
        senior_percentage = self.driver.find_element_by_xpath('//*[@id="data-table"]/tbody/tr[3]/td[2]').text
        population = self.driver.find_element_by_xpath('//*[@id="cover-profile"]/article/div[1]/div/span/span[1]').text
        
        density = self.driver.find_element_by_xpath('//*[@id="cover-profile"]/article/div[2]/div/span[2]/span[1]').text
        income = self.driver.find_element_by_xpath('//*[@id="economics"]/div/section[1]/div[1]/a/span/span[1]').text

        yield {
            'region_name': response.meta['region_name'],
            'region_url': response.meta['region_url'],
            'density': density,
            'income': income,
            'population': population,
            'senior_percentage': senior_percentage,
        }

        # self.driver.close() # acting funky bc we're using selenium + scrappy