import pandas as pd
import requests
from bs4 import BeautifulSoup as bs


class CompanyScraper:
    def __init__(self, output_file, base_url=None, headers=None, panda_seperate_by=','):
        self.base_url = base_url
        self.headers = headers
        self.output_file = output_file
        self.total_rating_count = 0.0
        self.seperate_by = panda_seperate_by

    def write_in_textfile(self, content, mode='a'):
        with open(file=self.output_file, mode=mode, encoding='UTF-8') as file:
            file.write(content)

    def fetch_webpage(self):
        response = requests.get(url=self.base_url, headers=self.headers)
        return response.text

    def get_company_details(self, webpage):
        soup = bs(webpage, 'lxml')
        return soup.find_all('div', class_='companyCardWrapper')

    def process_companies(self, companies):
        for company in companies:
            name = company.find('h2').text.strip()
            rating = company.find('span', class_='companyCardWrapper__companyRatingValue').text.strip()
            element_rated_for = company.find('span', class_='companyCardWrapper__ratingValues')
            rated_for = element_rated_for.text.strip() if element_rated_for else 'not Mentioned'
            rating_count = company.find('span', class_='companyCardWrapper__ActionCount').text.strip()

            rating_count = float(rating_count[:-1]) * 1000
            self.total_rating_count += rating_count

            text = f"{name}{self.seperate_by}{rating}{self.seperate_by}{rated_for}{self.seperate_by}{rating_count / 1000}k\n"
            self.write_in_textfile(text)


# Initialize and use the scraper
if __name__ == "__main__":
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-encoding': 'gzip, deflate, br, zstd',
        'accept-language': 'en-US,en;q=0.9,hi;q=0.8,gu;q=0.7',
        'cache-control': 'max-age=0',
        'referer': 'https://www.ambitionbox.com/list-of-companies',
        'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': "Windows",
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
    }
    seperate_key = '#&#'
    OUTPUT_FILE = 'C:/Users/deval/OneDrive/Desktop/Programing/data handling/Data Gathering Projects/textFile.txt'
    PAGE_NO = 1
    CompanyScraper(output_file=OUTPUT_FILE).write_in_textfile(f"Name{seperate_key}Rating{seperate_key}Highly Rated For{seperate_key}No. of Reviews\n", 'w')
    while PAGE_NO <= 503:
        BASE_URL = f'https://www.ambitionbox.com/list-of-companies?campaign=desktop_nav&page={PAGE_NO}'
        scraper = CompanyScraper(base_url=BASE_URL, headers=headers, output_file=OUTPUT_FILE,
                                 panda_seperate_by=seperate_key)
        webpage = scraper.fetch_webpage()
        companies = scraper.get_company_details(webpage)
        scraper.process_companies(companies)
        print(f"Data Extracted from {PAGE_NO}")
        PAGE_NO += 1