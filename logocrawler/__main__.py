import csv
import sys
from typing import TextIO
from .crawler import find_logo

# A simple CLI interface. In the real world, I would use proper argument parsing.
# As this is just a test assignment, though, just indexing into sys.argv will do.

# It accepts any filepath.
# If none is given, it defaults to reading a './websites.csv' in the current directory.

def read_websites(source: TextIO) -> list[str]:
    """Read list of websites from a TextIO source."""
    websites: list[str] = []
    reader = csv.reader(source)
    for row in reader:
        # We only care about the first item in each row.
        # ... Because the included 'websites.csv' only has one item per row.
        if not row: continue
        websites.append(row[0])
    return websites

def read_websites_from_file(filepath: str) -> list[str]:
    """Read list of websites from a CSV file."""
    with open(filepath, newline='') as csv_file:
        return read_websites(csv_file)

def write_logo_data(websites: list[str]):
    """Write each website's logo and favicon to stdout as CSV rows."""
    writer = csv.writer(sys.stdout)
    for website in websites:
        info = find_logo(website)
        writer.writerow([
            info.url,
            info.logo or '',
            info.favicon or ''
        ])

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        websites = read_websites_from_file('./websites.csv')
    elif sys.argv[1] == '-':
        websites = read_websites(sys.stdin)
    else:
        websites = read_websites_from_file(sys.argv[1])
    write_logo_data(websites)
