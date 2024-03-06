from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By

def scrape_edm():
  options = Options()
  #options.add_argument("--headless")
  driver = webdriver.Firefox(options=options)
  print("scraping edm")