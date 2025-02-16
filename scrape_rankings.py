import requests
import csv
from bs4 import BeautifulSoup
import os

# Define the list of event, sex, year, and agegroup combinations as strings
combinations = [
    "HT7.26K M 2024 ALL",
    "HT7.26K M 2023 ALL",
    "HT7.26K M 2022 ALL",
    "HT7.26K M 2021 ALL",
    "HT7.26K M 2020 ALL",
    "HT7.26K M 2019 ALL",
    "HT7.26K M 2018 ALL",
    "HT7.26K M 2017 ALL",
    "HT7.26K M 2016 ALL",
    "HT7.26K M 2015 ALL",
    "HT7.26K M 2014 ALL",
    "HT7.26K M 2013 ALL",
    "HT7.26K M 2012 ALL",
    "HT7.26K M 2011 ALL",
    "HT7.26K M 2010 ALL",
    "HT4K W 2024 ALL",
    "HT4K W 2023 ALL",
    "HT4K W 2022 ALL",
    "HT4K W 2021 ALL",
    "HT4K W 2020 ALL",
    "HT4K W 2019 ALL",
    "HT4K W 2019 ALL",
    "HT4K W 2018 ALL",
    "HT4K W 2017 ALL",
    "HT4K W 2016 ALL",
    "HT4K W 2015 ALL",
    "HT4K W 2014 ALL",
    "HT4K W 2013 ALL",
    "HT4K W 2012 ALL",
    "HT4K W 2011 ALL",
    "HT4K W 2010 ALL",
    "HT6K M 2024 U20",
    "HT6K M 2023 U20",
    "HT6K M 2022 U20",
    "HT6K M 2021 U20",
    "HT6K M 2020 U20",
    "HT6K M 2019 U20",
    "HT6K M 2018 U20",
    "HT6K M 2017 U20",
    "HT6K M 2016 U20",
    "HT6K M 2015 U20",
    "HT6K M 2014 U20",
    "HT6K M 2013 U20",
    "HT6K M 2012 U20",
    "HT6K M 2011 U20",
    "HT6K M 2010 U20",
    "HT4K W 2024 U20",
    "HT4K W 2023 U20",
    "HT4K W 2022 U20",
    "HT4K W 2021 U20",
    "HT4K W 2020 U20",
    "HT4K W 2019 U20",
    "HT4K W 2019 U20",
    "HT4K W 2018 U20",
    "HT4K W 2017 U20",
    "HT4K W 2016 U20",
    "HT4K W 2015 U20",
    "HT4K W 2014 U20",
    "HT4K W 2013 U20",
    "HT4K W 2012 U20",
    "HT4K W 2011 U20",
    "HT4K W 2010 U20",
    # Add more combinations as needed
]

# Create the subfolder 'rankings_csv' if it doesn't exist
if not os.path.exists('rankings_csv'):
    os.makedirs('rankings_csv')

# Headers for the request
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

# Loop through each combination of event, sex, year, and agegroup from the list
for combo in combinations:
    # Split the string into its components: event, sex, year, agegroup
    event, sex, year, agegroup = combo.split()

    # Construct the URL for the current combination of parameters
    url = f"https://www.thepowerof10.info/rankings/rankinglist.aspx?event={event}&agegroup={agegroup}&sex={sex}&year={year}"

    # Fetch the page content
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # This will raise an error if the request fails

    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the span with the rankings table
    rankings_span = soup.find("span", {"id": "cphBody_lblCachedRankingList"})

    # Find the table inside the span
    table = rankings_span.find("table")

    # Generate the CSV filename based on event, sex, year, and agegroup
    csv_filename = f'rankings_csv/{event}_{sex}_{year}_{agegroup}_rankings.csv'

    # Prepare the CSV file for writing
    csv_columns = ['Rank', 'Performance', 'Name', 'Year', 'Coach', 'Club', 'Venue', 'Date']
    
    # Open the CSV file in write mode
    with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(csv_columns)  # Write the header row

        # Now extract the rows
        if table:
            for row in table.find_all("tr")[1:]:  # Skip header row
                columns = row.find_all("td")

                if len(columns) >= 13:  # Ensure there are at least 13 columns
                    rank = columns[0].text.strip()
                    performance = columns[1].text.strip()
                    name = columns[6].text.strip()
                    year = columns[8].text.strip()
                    coach = columns[9].text.strip()
                    club = columns[10].text.strip()
                    venue = columns[11].text.strip()
                    date = columns[12].text.strip()

                    # Remove the comma between venue and country, if it exists
                    # Example: "Kladno, CZE" -> "Kladno CZE"
                    if "," in venue:
                        venue = venue.replace(",", "")  # Remove comma

                    # Write the data row to the CSV
                    writer.writerow([rank, performance, name, year, coach, club, venue, date])
                else:
                    print(f"Skipping row for {event} {sex} {year} {agegroup} due to insufficient columns.")
        else:
            print(f"Table not found for {event} {sex} {year} {agegroup}.")
    
    print(f"Data saved to {csv_filename}")
