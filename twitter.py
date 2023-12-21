import requests
from lxml import html

def scrape_twitter_xpath(username):
    url = f'https://twitter.com/{username}'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        tree = html.fromstring(response.text)

        tweet_texts = tree.xpath('//div[@data-testid="tweet"]//div[@class="css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0"]/text()')

        return tweet_texts
    else:
        print(f'Error al hacer la solicitud. Código de estado: {response.status_code}')
        return None

twitter_username = 'yllampi'
tweets_xpath = scrape_twitter_xpath(twitter_username)

if tweets_xpath:
    print(f'Últimos tweets de @{twitter_username} (usando XPath):')
    for idx, tweet in enumerate(tweets_xpath, start=1):
        print(f'{idx}. {tweet}')
