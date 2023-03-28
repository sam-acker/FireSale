import yaml, sys, requests, openai
from bs4 import BeautifulSoup

def configure():
    with open('config.yaml', 'r') as f:
        data = yaml.safe_load(f)

        # edit yaml here
        data["configured"] = 1

        data["robinhoodAPIKey"] = input("robinhood api key: ")
        data["openaiAPIKey"] = input("openai api key: ")
        data["value"] = int(input("Amount for put options: "))

    # write to yaml file
    with open('config.yaml', 'w') as file:
        yaml.dump(data,file,sort_keys=False)

def scrape():
    page = requests.get("http://hindenburgresearch.com/block/")
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


with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

configured = config["configured"]

if (len(sys.argv) == 2) and (sys.argv[1] == "config"):
    configure()
    quit()

if configured == 0:
    configure()
    quit()

if (len(sys.argv) == 2) and (sys.argv[1] == "start"):
    scrapedText = scrape()

    openai.api_key = config["openaiAPIKey"]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": 'Hi there!'}
        ]
    )
    
    print(response)
