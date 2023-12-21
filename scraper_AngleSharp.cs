using PuppeteerSharp;
using AngleSharp;
 
 
public class Product
{
    public string? Name { get; set; }
    public string? Price { get; set; }
}
 
class Program
{
    static async Task Main(string[] args)
    {
        // To store the scraped data
        var products = new List<Product>();
 
        // Download the browser executable
        await new BrowserFetcher().DownloadAsync();
 
        // Browser execution configs
        var launchOptions = new LaunchOptions
        {
            Headless = true, // run browser in headless mode
        };
 
        // Open a new page in the controlled browser
        using (var browser = await Puppeteer.LaunchAsync(launchOptions))
        using (var page = await browser.NewPageAsync())
        {
            // Visit the target page
            await page.GoToAsync("https://scrapingclub.com/exercise/list_infinite_scroll/");
 
            // Deal with infinite scrolling
            var jsScrollScript = @"
                const scrolls = 10
                let scrollCount = 0
 
                // Scroll down and then wait for 0.5s
                const scrollInterval = setInterval(() => {
                  window.scrollTo(0, document.body.scrollHeight)
                  scrollCount++
                  if (scrollCount === scrolls) {
                      clearInterval(scrollInterval)
                  }
                }, 500)
            ";
            await page.EvaluateExpressionAsync(jsScrollScript);
 
            // Wait for 10 seconds for the products to load
            await page.WaitForTimeoutAsync(10000);
 
            // Get the fully rendered content after JavaScript rendering
            var contentAfterRender = await page.GetContentAsync();
 
            // Create a new browsing context with AngleSharp
            var context = BrowsingContext.New(Configuration.Default);
            
            // Open a document with the rendered HTML content
            var document = await context.OpenAsync(req => req.Content(contentAfterRender));
 
            // Select all product HTML elements
            var productElements = document.QuerySelectorAll(".post");
 
            // Iterate over them and extract the desired data
            foreach (var productElement in productElements)
            {
                // Select the name and price elements
                var nameElement = productElement.QuerySelector("h4");
                var priceElement = productElement.QuerySelector("h5");
 
                // Extract their text
                var name = nameElement?.TextContent ?? "";
                var price = priceElement?.TextContent ?? "";
 
                // Instantiate a new product and add it to the list
                var product = new Product { Name = name, Price = price };
                products.Add(product);
            }
        }
 
        // Display the scraped data
        foreach (var product in products)
        {
            Console.WriteLine($"Name: {product.Name} | Price: {product.Price}");
        }
    }
}
