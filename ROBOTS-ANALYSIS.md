# Robots Analysis for the Daily Pennsylvanian

The Daily Pennsylvanian's `robots.txt` file is available at
[https://www.thedp.com/robots.txt](https://www.thedp.com/robots.txt).

## Contents of the `robots.txt` file on [2/22/2025]

User-agent: *
Crawl-delay: 10
Allow: /

User-agent: SemrushBot
Disallow: /

## Explanation

This robots.txt file provides instructions to web crawlers that index web pages for search engines.

The first section (User-agent: *) applies to all web crawlers, indicating that they are allowed to access all pages on the website (Allow: /).
The Crawl-delay: 10 directive tells these crawlers to wait 10 seconds between each request to prevent excessive load on the server.
The second section (User-agent: SemrushBot) specifically targets SemrushBot, instructing it not to crawl any pages on the website (Disallow: /).
This setup helps control how different bots interact with the site, balancing accessibility with server performance.
