from bs4 import BeautifulSoup
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())

# from webdriver_manager.firefox import GeckoDriverManager
# driver = webdriver.firefoxChrome(GeckoDriverManager().install())
# from webdriver_manager.microsoft import EdgeChromiumDriverManager
# driver = webdriver.Edge(EdgeChromiumDriverManager().install())

def html_getter(url):
    """
        Getting the HTML content of a twitter page.

        Args:
            url (string): the account url.

        Returns:
            string: the HTML content of the current page.
    """
    driver.get(url)  # url of page we want to scrap
    time.sleep(15)  # delay for 15 seconds to allow the page to fully load
    html = driver.page_source  # get the HTML content of the current page
    return html


def scrape_twitter_account(account, ticker):
    """
        scraps Twitter accounts for data.

        Args:
            account (string): List of Twitter Accounts.
            ticker (string): the ticker($ with a 4 or 3-letter word) to look for

        Returns:
            string: The number of times the stock symbol was mentioned in an account.
    """
    soup = BeautifulSoup(html_getter(account), 'html.parser')  # BeautifulSoup a BF4 object
    tweets = soup.find_all('div', {"data-testid": "tweetText"})

    mention_count = 0
    for tweet in tweets:
        tweet_text = tweet.text
        if ticker in tweet_text:
            mention_count += 1
    return mention_count


def main(accounts, ticker, interval_minutes):
    """
    Continuously monitors specified Twitter accounts for mentions of a given ticker symbol
     within a specified time interval.

        Args:
            accounts (list): A list of Twitter account.
            ticker (str): The ticker symbol (e.g., $SOFI) to search for in the Twitter accounts.
            interval_minutes (int): The time interval in minutes for which the mentions are monitored.

        Returns:
            None

        Notes:
            This function continuously monitors the specified Twitter accounts for mentions of the given ticker symbol.
            It prints the number of mentions found in each account and the total mentions found across all accounts,
            within the specified time interval. The function then waits for the specified interval before repeating
            the process.

        """
    while True:
        total_mentions = 0
        for i, account in enumerate(accounts):
            mentions = scrape_twitter_account(account, ticker)
            total_mentions += mentions
            print(
                f"'{ticker}' was mentioned '{mentions}' times in the account number '{i + 1}' in the last '{interval_minutes}' minutes.")
        print(f"'{ticker}' was mentioned {total_mentions} times in the last {interval_minutes} minutes.")
        time.sleep(interval_minutes * 60)


if __name__ == "__main__":
    accounts = ["https://twitter.com/Mr_Derivatives"
        , "https://twitter.com/warrior_0719"
        , "https://twitter.com/ChartingProdigy"
        , "https://twitter.com/allstarcharts"
        , "https://twitter.com/yuriymatso"
        , "https://twitter.com/TriggerTrades"
        , "https://twitter.com/AdamMancini4"
        , "https://twitter.com/CordovaTrades"
        , "https://twitter.com/Barchart"
        , "https://twitter.com/RoyLMattox"]  # List of Twitter accounts to scrape
    ticker = "$TSLA"  # Ticker symbol to look for
    interval_minutes = 10  # Time interval for scraping session

    main(accounts, ticker, interval_minutes)
