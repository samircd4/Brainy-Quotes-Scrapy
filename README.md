# Brainy-Quotes-Scrapy


## Installation 

Clone the project and open folder with vs code

```bash
  git clone https://github.com/samircd4/Scrapy.git
```
Go to terminal

```bash
  pip install -r requirements.txt
```
Go to Brainy-Quotes-Scrapy/quotes/spiders/config.py 

```python
  API = 'Your API KEY here' # Replace with your proxy api key
```

Run the script

```cmd
  scrapy crawl -o quotes.csv
```

Or

```cmd
  scrapy crawl -o quotes.json
```
Whatever output format you want either csv or json

### Thank you
#### ----Samir----
