document.addEventListener("DOMContentLoaded", function() {
    // List of available years
    const availableYears = [2024, 2023, 2022, 2021, 2020, 2019, 2018, 2017, 2016, 2015, 2014, 2013, 2012, 2011, 2010];  // Adjust this list as necessary
    let currentYearIndex = 0; // Start with 2024

    // Function to load the rankings for the selected year
    function loadRankings(year) {
        // Define the CSV files based on the current year
        const csvFiles = [
            { event: 'HT7.26K', sex: 'M', year: year, agegroup: 'ALL', tableId: 'mensHT7_26K' },
            { event: 'HT4K', sex: 'W', year: year, agegroup: 'ALL', tableId: 'womensHT4K' }
        ];

        // Update the heading dynamically based on the agegroup
        csvFiles.forEach(file => {
            if (file.agegroup === 'ALL') {
                document.getElementById("rankings-heading").innerText = `Senior Rankings: ${year}`;
            } else {
                document.getElementById("rankings-heading").innerText = `${file.agegroup} Rankings: ${year}`;
            }
        });

        document.getElementById("current-year").innerText = year;

        // Loop through each CSV file and fetch the data
        csvFiles.forEach(file => {
            const url = `rankings_csv/${file.event}_${file.sex}_${file.year}_${file.agegroup}_rankings.csv`;

            fetch(url)
                .then(response => response.text())
                .then(data => {
                    generateTable(data, file.tableId); // Generate the table for each event
                })
                .catch(error => console.error(`Error loading ${url}:`, error));
        });
    }

    // Function to generate the table from CSV data
    function generateTable(csvData, tableId) {
        // Split data by newline and clean up any extra spaces or empty lines
        let rows = csvData.split("\n").filter(row => row.trim() !== ''); // Remove empty rows
        
        // Remove the repeated headers (assumes headers are on row 1 and 2)
        rows = rows.slice(2); // Skip the first two rows (which are headers)
        
        // Limit to the top 20 rows
        rows = rows.slice(0, 20);

        let tableBody = document.querySelector(`#${tableId}`);

        // Add header to the table
        tableBody.innerHTML = `
            <thead>
                <tr>
                    <th>Rank</th>
                    <th>Distance</th>
                    <th>Athlete (Coach)</th>
                    <th>Venue (Date)</th>
                </tr>
            </thead>
            <tbody>
        `;

        // Process each row and append to the table body
        rows.forEach(row => {
            let cols = row.split(",").map(col => col.trim()); // Clean the columns

            if (cols.length >= 8) { // Ensure there are enough columns (we expect 8)
                let tr = document.createElement("tr");

                // Extract values from the CSV columns
                let rank = cols[0];
                let performance = cols[1];
                let name = cols[2];
                let coach = cols[4];  // Coach is in column 4
                let venue = cols[6];   // Venue is in column 6
                let date = cols[7];    // Date is in column 7

                // Handle the venue and date more carefully
                let actualVenue = venue.replace(/"/g, '').replace(/,/g, '-'); // Replace commas inside venue with a hyphen
                let formattedDate = date.trim().replace(/"/g, ''); // Remove quotes around date

                // If there is no coach, don't include parentheses
                let athleteCoach = coach ? `${name}<br>(${coach})` : name; // Add a line break before coach

                // Combine Venue and Date in one column with a line break before the date
                let venueDate = `${actualVenue}<br>(${formattedDate})`;

                // Construct the table row
                tr.innerHTML = `
                    <td>${rank}</td>
                    <td>${performance}</td>
                    <td>${athleteCoach}</td>
                    <td>${venueDate}</td>
                `;

                tableBody.appendChild(tr);
            }
        });

        // Close tbody tag
        tableBody.innerHTML += "</tbody>";
    }

    // Event listeners for year navigation buttons
    document.getElementById("prev-year").addEventListener("click", function() {
        if (currentYearIndex > 0) {
            currentYearIndex--;
            loadRankings(availableYears[currentYearIndex]);
        }
    });

    document.getElementById("next-year").addEventListener("click", function() {
        if (currentYearIndex < availableYears.length - 1) {
            currentYearIndex++;
            loadRankings(availableYears[currentYearIndex]);
        }
    });

    // Load rankings for the initial year (2024)
    loadRankings(availableYears[currentYearIndex]);
});
