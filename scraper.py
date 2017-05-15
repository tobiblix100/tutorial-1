###############################################################################
# START HERE: Tutorial 3: More advanced scraping. Shows how to follow 'next' 
# links from page to page: use functions, so you can call the same code 
# repeatedly. SCROLL TO THE BOTTOM TO SEE THE START OF THE SCRAPER.
###############################################################################

import scraperwiki
import lxml.html

# scrape_table function: gets passed an individual page to scrape
    
        
# scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    print html
    root = lxml.html.fromstring(html)
    rows = root.cssselect("table#TrolleyTable tr")  # selects all <tr> blocks within <table class="data">
    for row in rows:
        # Set up our data record - we'll need it later
        record = {}
        table_cells = row.cssselect("td")
        if table_cells:
            table_cells_urls = table_cells[1].cssselect("a")
            record['Date'] = table_cells[0].text
            record['Ward total'] = table_cells[4].text
            record['Hospital'] = table_cells[1].text
            record['Region'] = table_cells[2].text
            record['Trolley total'] = table_cells[3].text
            record['HospitalURL'] = table_cells_urls[1].attrib.get('href')
            # Print out the data we've gathered
            print record, '------------'
            # Finally, save the record to the datastore - 'Artist' is our unique key
            scraperwiki.sqlite.save(["Hospital"], record)
# ---------------------------------------------------------------------------
# START HERE: define your starting URL - then 
# call a function to scrape it.
# ---------------------------------------------------------------------------
starting_url = 'http://inmo.ie/6022'
scrape_and_look_for_next_link(starting_url)
