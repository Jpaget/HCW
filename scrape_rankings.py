import requests
import csv
from bs4 import BeautifulSoup
import os
from itertools import product

# Define the list of event, sex, year, and agegroup combinations as strings
events = ["HT7.26K M", "HT4K W", "HT6K M", "HT4K W","HT5K M","HT4K M","HT3K W","HT3K W"]
age_groups = ["ALL", "ALL", "U20", "U20","U17","U15", "U17","U15"]
years = range(2025, 2024, -1)  # From 2024 to 2010

combinations = [f"{event} {year} {age}" for event, age in zip(events, age_groups) for year in years]

# print(combinations)  # To check the output

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
