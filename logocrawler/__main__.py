import csv
import sys
from .crawler import find_logo, WebsiteInfo

# A simple CLI interface. In the real world, I would use proper argument parsing.
# As this is just a test assignment, though, just indexing into sys.argv will do.

# It accepts any filepath.
# If none is given, it defaults to reading a './website.csv' in the current directory.

def read_websites(csv_filepath: str) -> list[str]:
    """Read list of websites from a CSV file."""
    websites: list[str] = []
    with open(csv_filepath, newline='') as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            # We only care about the first item in each row.
            # ... Because the included 'websites.csv' only has one item per row.
            if not row: continue
            websites.append(row[0])
    return websites

def write_logo_data(websites: list[WebsiteInfo]):
    """Write each website's logo and favicon to stdout as CSV rows."""
    writer = csv.writer(sys.stdout)
    for website in websites:
        writer.writerow([
            website.url,
            website.logo or '',
            website.favicon or ''
        ])

input_file   = sys.argv[1] if len(sys.argv) > 1 else './websites.csv'
website_list = read_websites(input_file)

websites: list[WebsiteInfo] = []
for website in website_list:
    info = find_logo(website)
    websites.append(info)
write_logo_data(websites)
