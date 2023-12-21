using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Threading.Tasks;
using AngleSharp;
using PuppeteerSharp;

public class Product
{
    public string? Name { get; set; }
    public string? Price { get; set; }
}

class Program
{
    static async Task Main(string[] args)
    {
        var products = new List<Product>();

        var stopwatch = new Stopwatch();
        
        await new BrowserFetcher().DownloadAsync();

        var launchOptions = new LaunchOptions
        {
            Headless = true, 
        };

        using (var browser = await Puppeteer.LaunchAsync(launchOptions))
        using (var page = await browser.NewPageAsync())
        {
            stopwatch.Start();

            await page.GoToAsync("https://scrapingclub.com/exercise/list_infinite_scroll/");

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

            await page.WaitForTimeoutAsync(10000);

            var contentAfterRender = await page.GetContentAsync();

            var context = BrowsingContext.New(Configuration.Default);

            var document = await context.OpenAsync(req => req.Content(contentAfterRender));

            var productElements = document.QuerySelectorAll(".post");

            foreach (var productElement in productElements)
            {
                var nameElement = productElement.QuerySelector("h4");
                var priceElement = productElement.QuerySelector("h5");

                var name = nameElement?.TextContent ?? "";
                var price = priceElement?.TextContent ?? "";

                var product = new Product { Name = name, Price = price };
                products.Add(product);
            }

            stopwatch.Stop();

            Console.WriteLine($"Tiempo total de extracción: {stopwatch.ElapsedMilliseconds} ms");
            Console.WriteLine($"Número de productos extraídos: {products.Count}");
        }

        foreach (var product in products)
        {
            Console.WriteLine($"Name: {product.Name} | Price: {product.Price}");
        }
    }
}
