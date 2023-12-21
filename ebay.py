from parsel import Selector
import httpx

def parse_product(response: httpx.Response) -> dict:
    """Parse Ebay's product listing page for core product data"""
    sel = Selector(response.text)
    css_join = lambda css: "".join(sel.css(css).getall()).strip()  
    css = lambda css: sel.css(css).get("").strip() 

    item = {}
    item["url"] = css('link[rel="canonical"]::attr(href)')
    item["id"] = item["url"].split("/itm/")[1].split("?")[0] 
    item["price"] = css('.x-price-primary>span::text')
    item["name"] = css_join("h1 span::text")
    item["seller_name"] = css_join("[data-testid=str-title] a ::text")
    item["seller_url"] = css("[data-testid=str-title] a::attr(href)").split("?")[0]
    item["photos"] = sel.css('.ux-image-filmstrip-carousel-item.image img::attr("src")').getall()  
    item["photos"].extend(sel.css('.ux-image-carousel-item.image img::attr("src")').getall())  
   
    item["description_url"] = css("div.d-item-description iframe::attr(src)")
    if not item["description_url"]:
        item["description_url"] = css("div#desc_div iframe::attr(src)")
    feature_table = sel.css("div.ux-layout-section--features")
    features = {}
    for ft_label in feature_table.css(".ux-labels-values__labels"):
        label = "".join(ft_label.css(".ux-textspans::text").getall()).strip(":\n ")
        ft_value = ft_label.xpath("following-sibling::div[1]")
        value = "".join(ft_value.css(".ux-textspans::text").getall()).strip()
        features[label] = value
    item["features"] = features
    return item

session = httpx.Client(
    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.35",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
    },
    http2=True,
    follow_redirects=True
)


response = session.get("https://www.ebay.com/itm/332562282948")
item = parse_product(response)
import json
print(json.dumps(item, indent=2))