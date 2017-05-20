#import our libraries
import scraperwiki
import lxml.html

# create a new function, which gets passed a variable we're going to call 'url'
def scrape_ccg(url):
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    #line below selects all <div class="reveal-modal medium"> - note that because there is a space in the value of the div class, we need to use a space to indicate that
    rows = root.cssselect("background-color:#f8f8f8; width:30%; height:300px;display : inline-block;margin:10px 10px 0px 0px; vertical-align:top;") 
    for row in rows:
        # Set up our data record - we'll need it later
        record = {}
        imgs = row.cssselect("img")
        img = imgs[0].attrib.get("src")
        h2s = row.cssselect("h2") #grab all <h2> tags within our <div>
        membername = h2s[0].text
        #repeat process for <p class="lead"> 
        leads = row.cssselect("p.lead")
        membertitle = leads[0].text
        #repeat process for <p>
        ps = row.cssselect("p")
        #this line puts the contents of the last <p tag by using [-1]
        memberbiog = ps[-1].text_content()
        record["Image"] = img
        record['URL'] = url
        record['Name'] = membername
        record['Title'] = membertitle
        record['Description'] = memberbiog
        
        baseurl = url.replace("/about-us/our-governing-body.aspx","")
        record["FullImage"] = baseurl+img
        
        print record, '------------'
        # Finally, save the record to the datastore - 'Name' is our unique key
        scraperwiki.sqlite.save(["Name"], record)
        
#list of URLs with similar CMS compiled with this advanced search on Google: site:nhs.uk inurl:about-us/our-governing-body.aspx
ccglist = ['www.hounslowccg.nhs.uk/',  'www.centrallondonccg.nhs.uk/', 'www.hammersmithfulhamccg.nhs.uk/']
#'www.ealingccg.nhs.uk/' has similar page but at different URL: http://www.hammersmithfulhamccg.nhs.uk/about-us/our-governing-body.aspx
for ccg in ccglist:
    fullurl = 'http://'+ccg+'about-us/our-governing-body.aspx'
    print 'scraping ', fullurl
    scrape_ccg(fullurl)
