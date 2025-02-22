"""
Scrapes a headline from The Daily Pennsylvanian website and saves it to a 
JSON file that tracks headlines over time.
"""

import os
import sys

import daily_event_monitor

import bs4
import requests
import loguru


def scrape_data_point():
    """
    Scrapes the main headline from The Daily Pennsylvanian home page.

    Returns:
        str: The headline text if found, otherwise an empty string.
    """
    headers = {
        "User-Agent": "cis3500-scraper"
    }
    req = requests.get("https://www.thedp.com", headers=headers)
    loguru.logger.info(f"Request URL: {req.url}")
    loguru.logger.info(f"Request status code: {req.status_code}")

    sections = {
        "News": None,
        "Sports": None,
        "Opinion": None,
    }

    if req.ok:
        soup = bs4.BeautifulSoup(req.text, "html.parser")

        # Extract News headline
        news_section = soup.find("div", class_="col-sm-6 section-news")
        if news_section:
            first_news_link = news_section.find("a", class_="frontpage-link medium-link newstop")
            if first_news_link and first_news_link.get("href"):
                sections["News"] = first_news_link.text.strip()

        # Extract Sports and Opinion headlines
        sports_opinion_divs = soup.find_all("div", class_="col-sm-6")

        for section_div in sports_opinion_divs:
            section_heading = section_div.find("h3", class_="frontpage-section")
            if section_heading:
                section_title = section_heading.text.strip().lower()

                if "sports" in section_title:
                    first_link = section_div.find("div", class_="article-summary").find("a")
                    if first_link:
                        sections["Sports"] = first_link.text.strip()

                elif "opinion" in section_title:
                    first_link = section_div.find("div", class_="article-summary").find("a")
                    if first_link:
                        sections["Opinion"] = first_link.text.strip()

        # Log extracted headlines
        for section, headline in sections.items():
            loguru.logger.info(f"{section} Headline: {headline if headline else 'Not Found'}")

    return sections


if __name__ == "__main__":

    # Setup logger to track runtime
    loguru.logger.add("scrape.log", rotation="1 day")

    # Create data dir if needed
    loguru.logger.info("Creating data directory if it does not exist")
    try:
        os.makedirs("data", exist_ok=True)
    except Exception as e:
        loguru.logger.error(f"Failed to create data directory: {e}")
        sys.exit(1)

    # Load daily event monitor
    loguru.logger.info("Loading daily event monitor")
    dem = daily_event_monitor.DailyEventMonitor(
        "data/daily_pennsylvanian_headlines.json"
    )

    # Run scrape
    loguru.logger.info("Starting scrape")
    try:
        data_point = scrape_data_point()
    except Exception as e:
        loguru.logger.error(f"Failed to scrape data point: {e}")
        data_point = None

    # Save data
    if data_point is not None:
        dem.add_today(data_point)
        dem.save()
        loguru.logger.info("Saved daily event monitor")

    def print_tree(directory, ignore_dirs=[".git", "__pycache__"]):
        loguru.logger.info(f"Printing tree of files/dirs at {directory}")
        for root, dirs, files in os.walk(directory):
            dirs[:] = [d for d in dirs if d not in ignore_dirs]
            level = root.replace(directory, "").count(os.sep)
            indent = " " * 4 * (level)
            loguru.logger.info(f"{indent}+--{os.path.basename(root)}/")
            sub_indent = " " * 4 * (level + 1)
            for file in files:
                loguru.logger.info(f"{sub_indent}+--{file}")

    print_tree(os.getcwd())

    loguru.logger.info("Printing contents of data file {}".format(dem.file_path))
    with open(dem.file_path, "r") as f:
        loguru.logger.info(f.read())

    # Finish
    loguru.logger.info("Scrape complete")
    loguru.logger.info("Exiting")
