import requests
from bs4 import BeautifulSoup

def get_athlete_performances_over_70m(athlete_id):
    url = f"https://www.thepowerof10.info/athletes/profile.aspx?athleteid={athlete_id}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all tables with class 'alternatingrowspanel' (which contain performances)
    tables = soup.find_all("table", class_="alternatingrowspanel")

    if not tables:
        print("No performance tables found.")
        return

    performances_over_70m = []

    for table in tables:
        rows = table.find_all("tr")[2:]  # Skip the first two header rows

        for row in rows:
            cols = row.find_all("td")
            if len(cols) < 12:
                continue  # Skip rows without enough columns

            event = cols[0].text.strip()
            performance = cols[1].text.strip()
            position = cols[5].text.strip()
            venue = cols[9].text.strip()
            meeting = cols[10].text.strip()
            date = cols[11].text.strip()

            # Clean up potential issues where Performance or Venue data is concatenated
            if "," in venue:  # Remove any commas within the venue name
                venue = venue.split(",")[0]

            # Ensure Performance is a valid number and remove any trailing characters
            try:
                performance_value = float(performance)
            except ValueError:
                continue  # Skip this row if the performance isn't a valid number

            # Only consider HT7.26K performances over 70m
            if event == "HT7.26K" and performance_value > 70:
                performances_over_70m.append({
                    "Event": event,
                    "Performance": performance_value,
                    "Position": position,
                    "Venue": venue,
                    "Meeting": meeting,
                    "Date": date
                })

    # Print results
    if performances_over_70m:
        print(f"Found {len(performances_over_70m)} performances over 70m:")
        for p in performances_over_70m:
            print(f"{p['Date']}: {p['Event']} - {p['Performance']}m at {p['Venue']} ({p['Meeting']})")
        
        # Print the count of performances over 70m
        print(f"\nTotal count of HT7.26K performances over 70m: {len(performances_over_70m)}")
    else:
        print("No HT7.26K performances over 70m found.")

# Run the function for the example athlete
get_athlete_performances_over_70m("783760")




