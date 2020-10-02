# CensusReporter-Scraper

Extract senior population, income per capita, median household income, and density from a list of counties

## Requirements

### Docker
[install docker](https://docs.docker.com/install/)

### jq

    brew install jq

### Python 3.7

    pip install selenium
    pip install Scrapy 

## Input

Create a regions.csv file where each line contains the county followed by it's corresponding state separated by a comma. You can search for counties [here](https://www.zip-codes.com/search.asp)

regions.csv

    Nassau,NY
    Suffolk,NY
    Queens,NY

## Run

Run the below command.

    ./run.sh

## Output

report.csv

    region_name,region_url,density,income_per_capita,household_income,population,senior_percentage
    01431,https://censusreporter.org/profiles/86000US01431-01431,135,"$36,900","$95,833","3,195",13.9%
    01463,https://censusreporter.org/profiles/86000US01463-01463,533.7,"$40,919","$90,029","12,049",13.1%
    01434,https://censusreporter.org/profiles/86000US01434-01434,324.4,"$17,126","$50,547","1,712",15%
    .
    .
    .
    23176,https://censusreporter.org/profiles/86000US23176-23176,111.4,"$28,334","$38,301",482,33%
    23175,https://censusreporter.org/profiles/86000US23175-23175,100.8,"$30,822","$51,250","1,641",35.3%
    23180,https://censusreporter.org/profiles/86000US23180-23180,45.4,"$38,160","$70,417",461,6.7%
