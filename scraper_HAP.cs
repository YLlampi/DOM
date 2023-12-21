using HtmlAgilityPack; 
using CsvHelper; 
using System.Globalization; 
 
namespace SimpleWebScraper 
{ 
	public class Program 
	{ 
		public class PokemonProduct 
		{ 
			public string? Url { get; set; } 
			public string? Image { get; set; } 
			public string? Name { get; set; } 
			public string? Price { get; set; } 
		} 
 
		public static void Main() 
		{ 
			var pokemonProducts = new List<PokemonProduct>(); 
 
			var web = new HtmlWeb(); 
 
			var document = web.Load("https://scrapeme.live/shop/"); 
 
			var productHTMLElements = document.DocumentNode.QuerySelectorAll("li.product"); 
			foreach (var productHTMLElement in productHTMLElements) 
			{ 
				var url = HtmlEntity.DeEntitize(productHTMLElement.QuerySelector("a").Attributes["href"].Value); 
				var image = HtmlEntity.DeEntitize(productHTMLElement.QuerySelector("img").Attributes["src"].Value); 
				var name = HtmlEntity.DeEntitize(productHTMLElement.QuerySelector("h2").InnerText); 
				var price = HtmlEntity.DeEntitize(productHTMLElement.QuerySelector(".price").InnerText); 
 
				var pokemonProduct = new PokemonProduct() { Url = url, Image = image, Name = name, Price = price }; 
				pokemonProducts.Add(pokemonProduct); 
			} 
 
			using (var writer = new StreamWriter("pokemon-products.csv")) 
			using (var csv = new CsvWriter(writer, CultureInfo.InvariantCulture)) 
			{ 
				csv.WriteRecords(pokemonProducts); 
			} 
		} 
	} 
}
