import yaml, sys, requests, openai, time, pickle
from bs4 import BeautifulSoup
from alpaca.trading.client import TradingClient

# TODO: document functions

# FUNCTIONS
def configure():
    with open('config.yaml', 'r') as f:
        data = yaml.safe_load(f)

        # edit yaml here
        data["configured"] = 1

        data["alpacaAPIKey"] = input("alpaca api key: ")
        data["alpacaSecret"] = input("alpaca secret: ")
        data["openaiAPIKey"] = input("openai api key: ")
        data["value"] = int(input("Amount for put options: "))

    # write to yaml file
    with open('config.yaml', 'w') as file:
        yaml.dump(data,file,sort_keys=False)

def scrape(url):
    # "http://hindenburgresearch.com/block/"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    tag = soup.body

    textList = []
    # Print each string recursively
    for string in tag.strings:
        if string == "\n":
            continue
        textList.append(string)

    ret = ""
    for i in range(30):
        ret += textList[i]
    
    return ret

def get_ticker(scrape_input):
    a = scrape_input
    openai.api_key = config["openaiAPIKey"]

    # TODO: engineer prompt with scrape input
    # and extract ticker to be returned with
    # regex

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": 'Hi there!'}
        ]
    )

    return response

def check():
    url = "http://hindenburgresearch.com/"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    check = soup.find("div", class_="post-heading").findChildren("h1", recursive=False)[0].findChildren("a", recursive=False)[0].get("href")

    return check

# TODO: make alpaca short sell function
# https://alpaca.markets/docs/trading/getting_started/
def short(ticker_input):
    print("short placeholder")

    API_KEY = config["alpacaAPIKey"]
    SECRET_KEY = config["alpacaSecret"]

    trading_client = TradingClient(API_KEY, SECRET_KEY, paper=True)


# SETUP
with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

configured = config["configured"]

if (len(sys.argv) == 2) and (sys.argv[1] == "config"):
    configure()
    quit()

if configured == 0:
    configure()
    quit()

link_chache = {""}
ticker_cache = {""}

# TODO: check .pkl files to see if they're empty

with open('link_cache.pkl', 'rb') as fp:
    link_chache = pickle.load(fp)

with open('ticker_cache.pkl', 'rb') as fp:
    ticker_cache = pickle.load(fp)


# MAIN
if (len(sys.argv) == 2) and (sys.argv[1] == "start"):
    # scraped_text = scrape("http://hindenburgresearch.com/block/")
    # print(scraped_text)
    # print(get_ticker("test"))
    # print("___MAIN___")
    print(get_ticker("test"))
    loop = 0
    while loop < 4:
        # print("_____________")
        # print(link_chache)
        top_link = check()
        if top_link not in link_chache:
            link_chache.add(top_link)
            article_text = scrape(top_link)
            
            # TODO: pass article text to get_ticker()

            # TODO: ticker cache

            # TODO: pass ticker to alpaca function

        # print("_______sleeping_______")
        loop += 1
        time.sleep(5)


# TODO: make better exit system that still saves

# TODO: make python style correct main function

# TODO: better argument handling

# TODO: .gitignore for yaml and yaml builder

# TODO: proper application structure

# SAVE
with open('link_cache.pkl', 'wb') as fp:
    pickle.dump(link_chache, fp)

with open('ticker_cache.pkl', 'wb') as fp:
    pickle.dump(ticker_cache, fp)