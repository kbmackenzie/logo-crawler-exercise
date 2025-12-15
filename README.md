### This repository contains a take-home interview assignment.
#### It is not intended to represent production-quality or maintained code.
<hr>

A simple logo crawler that tries to select the best logo candidate for a given website.
It also scrapes favicons when available.

The crawler operates on static HTML only and does not render the DOM. This means it will not find logos that are injected dynamically into the DOM via JavaScript. In a more serious project, a browser-based approach using a package like Playwright and waiting on a specific selector may yield better results.

This project also does handle inline SVG logos, which introduce another layer of complexity to the task.

## API

I haeve included a minimal API for extracting the logo + favicon from a website.
The code should be self-explanatory.

```python3
import logocrawler

logo = logocrawler.find_logo('facebook.com')
print(logo)
```

## Running the Project

I've included a minimal CLI interface for convenience.
It accepts an optional path to a CSV file. If none is provided, it reads `./websites.csv` by default.

The output is written to stdout as CSV, with three columns: website url, logo url, favicon url.

```shell
python3 -m logocrawler
```
