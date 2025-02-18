import os

# Get the current directory where the script is located
current_dir = os.path.dirname(os.path.abspath(__file__))

# Path to the navbar.html file (same folder as the script)
navbar_file = os.path.join(current_dir, "nav.html")

# Read the contents of the navbar file
with open(navbar_file, 'r', encoding='utf-8') as f:
    navbar_content = f.read()

# Loop through each file in the current directory
for filename in os.listdir(current_dir):
    # Skip the navbar.html file
    if filename == "nav.html":
        continue

    # Check if the file is an HTML file
    if filename.endswith(".html"):
        file_path = os.path.join(current_dir, filename)

        # Read the content of the current HTML file
        with open(file_path, 'r', encoding='utf-8') as f:
            file_content = f.read()

        # Replace the entire <nav> section with the new navbar content
        # Look for the <nav> tag and replace everything inside it
        new_content = file_content
        start_nav = new_content.find('<nav>')
        end_nav = new_content.find('</nav>') + len('</nav>')

        if start_nav != -1 and end_nav != -1:
            # Replace the <nav> content between the tags
            new_content = new_content[:start_nav] + "<nav>" + navbar_content + "</nav>" + new_content[end_nav:]
        

        # Write the updated content back to the file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

        print(f"Updated navbar in: {filename}")
