"""
This script defines a class `CompanyScraper` that fetches company ratings and reviews from the AmbitionBox website
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
    def __init__(self, output_file=None, base_url=None, headers=None, panda_seperate_by=','):
        # Initialize the scraper with optional output file, base URL, headers, and pandas separator
        self.base_url = base_url
        self.headers = headers
        self.output_file = output_file
        self.total_rating_count = 0.0  # Initialize the total rating count
        self.seperate_by = panda_seperate_by  # Separator for pandas DataFrame
        self.data_list = []  # List to store scraped company data

    def write_in_textfile(self, content, mode='a'):
        # Write content to the output text file in the specified mode
        with open(file=self.output_file, mode=mode, encoding='UTF-8') as file:
            file.write(content)

    def fetch_webpage(self):
        # Send GET request to fetch the webpage content
        response = requests.get(url=self.base_url, headers=self.headers)
        return response.text  # Return the HTML content of the page

    def get_company_details(self, webpage):
        # Parse the webpage HTML and extract company details
        soup = bs(webpage, 'lxml')  # Use BeautifulSoup to parse the HTML
        return soup.find_all('div', class_='companyCardWrapper')  # Find all company cards

    def process_companies(self, companies):
        # Process each company card to extract required details
        for company in companies:
            name = company.find('h2').text.strip()  # Extract company name
            rating = company.find('span', class_='companyCardWrapper__companyRatingValue').text.strip()  # Extract rating
            element_rated_for = company.find('span', class_='companyCardWrapper__ratingValues')  # Extract highly rated for
            rated_for = element_rated_for.text.strip() if element_rated_for else 'not Mentioned'  # Handle missing data
            rating_count = company.find('span', class_='companyCardWrapper__ActionCount').text.strip()  # Extract review count

            rating_count = float(rating_count[:-1]) * 1000  # Convert rating count to numerical value (assuming it's in thousands)
            self.total_rating_count += rating_count  # Accumulate the total rating count

            # Append extracted company details to the data list
            self.data_list.append({
                'Name': name,
                'Rating': rating,
                'Highly Rated For': rated_for,
                'No. of Reviews': rating_count
            })

# Initialize and use the scraper
if __name__ == "__main__":

    def barGraph_analysis(df):
        # Function to generate a bar graph of company ratings
        plt.figure(figsize=(15, 10))
        plt.bar(df['Name'], df['Rating'])  # Create the bar graph using company names and ratings
        plt.xticks(rotation=90)  # Rotate x-axis labels to 90 degrees for better readability

        plt.show()  # Display the graph

    data_frame = pd.DataFrame()  # Initialize an empty DataFrame for storing company data

    # Define the headers for the HTTP requests
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

    PAGE_NO = 1  # Start from the first page
    total_reviews_count = 0.0  # Initialize the total reviews count
    while PAGE_NO <= 503:  # Loop through pages 1 to 503
        BASE_URL = f'https://www.ambitionbox.com/list-of-companies?campaign=desktop_nav&page={PAGE_NO}'  # Construct the page URL
        print(f"Data Extracting from Page no: {PAGE_NO}")  # Print the page number being processed
        scraper = CompanyScraper(base_url=BASE_URL, headers=headers)  # Create a scraper object
        webpage = scraper.fetch_webpage()  # Fetch the webpage content
        companies = scraper.get_company_details(webpage)  # Get company details from the webpage
        scraper.process_companies(companies)  # Process the company details
        data_frame = pd.concat([data_frame, pd.DataFrame(scraper.data_list)], ignore_index=True)  # Append data to DataFrame
        PAGE_NO += 1  # Move to the next page
        total_reviews_count += scraper.total_rating_count  # Accumulate the total reviews count

    # Export the relevant columns to a new DataFrame for analysis
    data_frame_export = data_frame[['Name', 'Rating', 'No. of Reviews']]
    data_frame = pd.read_excel('C:\\Users\\deval\\OneDrive\\Desktop\\Programing\\data handling\\Data Gathering Projects\\Company Data_example.xlsx')  # Read existing data from Excel
    file_path = '/Company Data_example.xlsx'  # File path for output

    # Define chunk size for processing large DataFrames
    chunk_size = 1000  # Adjust based on your memory limits

    # Process the DataFrame in chunks to avoid memory overload
    for start in range(0, len(data_frame), chunk_size):
        chunk = data_frame.iloc[start:start + chunk_size]  # Get the chunk of the DataFrame
        barGraph_analysis(chunk)  # Call the bar graph analysis function for the current chunk
