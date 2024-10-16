""" This script defines a class `CompanyScraper` that fetches company ratings and reviews from the AmbitionBox website
    using web scraping techniques. It retrieves details such as company names, ratings, highly rated attributes,
    and review counts. Initially, web scraping is performed to gather this data, which is then exported to an Excel file
    for storage. To optimize performance, the script reads from the Excel file in chunks, allowing for efficient data
    analysis. A bar graph is generated using Matplotlib to visualize the ratings of the companies.
"""


import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
from matplotlib import pyplot as plt

class CompanyScraper:
    def __init__(self, output_file = None, base_url=None, headers=None, panda_seperate_by=','):
        self.base_url = base_url
        self.headers = headers
        self.output_file = output_file
        self.total_rating_count = 0.0
        self.seperate_by = panda_seperate_by
        self.data_list = []

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

            self.data_list.append({
                'Name': name,
                'Rating': rating,
                'Highly Rated For': rated_for,
                'No. of Reviews': rating_count
            })




# Initialize and use the scraper
if __name__ == "__main__":

    def barGraph_analysis(df):
        plt.figure(figsize=(15, 10))
        plt.bar(df['Name'], df['Rating'])  # Create the bar graph
        plt.xticks(rotation=90)  # Rotate x-axis labels to 90 degrees

        plt.show()


    # data_frame = pd.DataFrame()

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

    # PAGE_NO = 1
    # total_reviews_count = 0.0
    # while PAGE_NO <= 503:
    #     BASE_URL = f'https://www.ambitionbox.com/list-of-companies?campaign=desktop_nav&page={PAGE_NO}'
    #     print(f"Data Extracting from Page no: {PAGE_NO}")
    #     scraper = CompanyScraper(base_url=BASE_URL, headers=headers)
    #     webpage = scraper.fetch_webpage()
    #     companies = scraper.get_company_details(webpage)
    #     scraper.process_companies(companies)
    #     data_frame = pd.concat([data_frame, pd.DataFrame(scraper.data_list)], ignore_index=True) # Load diretcly to Panda.DataFrame()
    #     PAGE_NO += 1
    #     total_reviews_count += scraper.total_rating_count
    # data_frame_export = data_frame[['Name', 'Rating', 'No. of Reviews']]
    # data_frame = pd.read_excel('C:\\Users\\deval\\OneDrive\\Desktop\\Programing\\data handling\\Data Gathering Projects\\Company.xlsx')
    file_path = 'C:\\Users\\deval\\OneDrive\\Desktop\\Programing\\data handling\\Data Gathering Projects\\Company.xlsx'

    # Load the Excel file into a DataFrame
    data_frame = pd.read_excel(file_path)

    # Define chunk size
    chunk_size = 1000  # Adjust based on your memory limits

    # Process the DataFrame in chunks
    for start in range(0, len(data_frame), chunk_size):
        # Get the chunk of the DataFrame
        chunk = data_frame.iloc[start:start + chunk_size]

        # Call your analysis function for the sorted chunk
        barGraph_analysis(chunk)
