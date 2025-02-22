# Basic Git Scraper Template

For my changes, I scraped for the news, sports and opinions top headlines. This web scraping code first sends a request to The Daily Pennsylvanian website using the requests library, mimicking a real browser with custom headers. If the request is successful, it parses the HTML content using BeautifulSoup, allowing the script to search for specific sections. It then looks for the News section by identifying a div with the class "col-sm-6 section-news" and extracts the first article’s headline. For Sports and Opinion, it scans all div elements with the class "col-sm-6", identifies section titles based on an h3 tag ("frontpage-section"), and extracts the first article headline from each category. Finally, it logs the extracted headlines and returns them in a dictionary for further use.

## Scheduling

