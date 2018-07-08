import os
import sys
import time
import tkMessageBox
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import glob
import csv

'''
NOTES
ARNC, DXC, KMI, MAR, MOS, PLD do not have P/E ratio data on Wolfram
'''

'''
GLOBAL CONSTANTS AND VARIABLES
'''
# where all the CSV files will go
STOCK_DIR = '/Users/liezl/Downloads'

# should be a file that has one stock symbol per line
STOCK_LIST_FILENAME = './stocklist.txt'

# should be a file that has one stock symbol per line
RETRY_LIST_FILENAME = './retryList.txt'

# file for the output csv
FIVE_YEAR_FUNDAMENTALS_FNAME = './five_year_fundamentals.csv'

# the names of the fundamentals we want to scrape
# we can calculate:
#   PE Ratio * Net Income = Market Cap
#   revenue/employee
#   net income / shares outstanding = annual earnings / share
# FUNDAMENTAL_CATEGORIES = ['revenue', 'employees', 'net income', 'shares outstanding', 'P%2FE ratio']
FUNDAMENTAL_CATEGORIES = ['P%2FE ratio']

# as we retry more times, we sleep longer and longer before attempting to click around the page (to allow loading)
SLEEP_TIME_INC = 5

# list of files to never download in downloadOneFundamentalCSV
BAD_DOWNLOAD_STOCK_LIST = ['ARNC', 'DXC', 'KMI', 'MAR', 'MOS', 'PLD']

# global stock symbol list that should be read in from ./stocklist.txt
stockSymbols = []

# global fundamentalData dict that should be read in from the rawCSV files
# {symbol1: {fundamental1: [], fundamental2: [], ....}, symbol2: {fundamental1: [], fundamental2: [], ...}}
fundamentalData = {}

# global list of dates
dateLabels = []

# see README for chromedriver instructions
chromedriver = "/Users/liezl/Desktop/Code/chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver
driver = None # initialize in main code below

'''
FUNCTIONS
'''
# makes a new directory if it doesn't exist
def makeDir(directory):
  if not os.path.exists(directory):
    os.makedirs(directory)

# read every line into a list of lines from fname, then return the list
def readListFromFile(fname):
  with open(fname) as f:
    lines = f.readlines()
    lineList = [x.strip() for x in lines]
    return lineList

# file should have username on first line then password on second line
def readUserInfoFromFile(fname):
  with open(fname) as f:
    lines = f.readlines()
    lineList = [x.strip() for x in lines]
    return lineList[0], lineList[1]

def signIntoWolfram(userInfoFilename):
  # get user's login info
  username, password = readUserInfoFromFile(userInfoFilename)

  # input login info into the login form
  driver.get('https://account.wolfram.com/auth/sign-in')
  userField = driver.find_element_by_xpath('//*[@id="email"]/input')
  userField.send_keys(username)
  passwordField = driver.find_element_by_xpath('//*[@id="password"]/input')
  passwordField.send_keys(password)
  signInBtn = driver.find_element_by_xpath('//*[@id="sign-in-btn"]')
  signInBtn.click()

# usage: downloadOneFundamentalCSV('GOOG', 'P%2FE')
def downloadOneFundamentalCSV(symbol, fundamental, sleepTime=15):
  if symbol in BAD_DOWNLOAD_STOCK_LIST:
    return

  # get URL with corresponding symbol + desired fundamental query
  driver.get('https://www.wolframalpha.com/input/?i=' + symbol + '+' + fundamental)
  try:
    # have to click the Sign In button anytime we use driver.get() because Wolfram is bad at cookies
    signInBtn2 = driver.find_element_by_xpath('//*[@id="wa-user-menu"]/button[1]')
    signInBtn2.click()
  except:
    pass
  time.sleep(sleepTime) # wait 20 seconds for queried page to render
  driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
  footer = driver.find_element_by_xpath('//*[contains(@id, "HistoryQuarterly")]')
  hover = ActionChains(driver).move_to_element(footer)
  hover.perform()

  dldata = driver.find_elements_by_xpath('//*[contains(text(), "Data")]') # last element found in the list is the true Download Data button
  for dl in dldata:
    try:
      dl.click()
    except:
      pass
      # print 'failed clicking on element ', dl # uncomment for debugging only

  selectCSV = driver.find_element_by_xpath('//*[@id="exportpod-pricing"]/div[1]/select/option[4]')
  selectCSV.click()

  finalDownload = driver.find_element_by_xpath('//*[@id="signin-dl"]')
  finalDownload.click()
  time.sleep(sleepTime)

def downloadFundamentalCSVs(stockSymbols):
  for symbol in stockSymbols:
    for fundamental in FUNDAMENTAL_CATEGORIES:
      try:
        downloadOneFundamentalCSV(symbol, fundamental)
      except:
        print 'failed to download ', symbol, fundamental
    print 'finished downloading ' + symbol

def getCSVFilename(symbol, fundamental):
  fundamentalFileName = fundamental.replace('%2F', '_').replace(' ', '_')
  CSVfilenames = glob.glob(STOCK_DIR + '/*.csv')
  for filename in CSVfilenames:
    if fundamentalFileName.lower() in filename.lower() and symbol.replace('.', '_').lower() + '_' in filename.lower():
      return filename
  return None

def CSVExists(symbol, fundamental):
  return getCSVFilename(symbol, fundamental) != None

def retryDownloads(retrySymbols, trynum):
  successful = True
  for symbol in retrySymbols:
    for fundamental in FUNDAMENTAL_CATEGORIES:
      try:
        if not CSVExists(symbol, fundamental):
          downloadOneFundamentalCSV('NASDAQ:' + symbol, fundamental, sleepTime = 5 + trynum * SLEEP_TIME_INC)
          print 'successful download retry of ', symbol, fundamental
      except:
        successful = False
        print 'failed to download ', symbol, fundamental
  # return successful

  # the rest of the code in this function only works if the STOCK_DIR is the same as the user's Downloads folder
  if not successful:
    return False
  # we have to double-check if we REALLY successfully downloaded everything, because Wolfram could have
  # errored out even if we successfully clicked all the buttons we needed to
  for symbol in retrySymbols:
    for fundamental in FUNDAMENTAL_CATEGORIES:
      if not CSVExists(symbol, fundamental):
        return False
  return True

# reads and returns the date column from one stock CSV
# requires that stockSymbols is populated and that we have all stock CSVs downloaded
# sample usage:
#    dates = readDateColumn()
#    print dates
#    print len(dates)
def readDateColumn():
  DATE_COLUMN_INDEX = 0
  with open(getCSVFilename(stockSymbols[3], FUNDAMENTAL_CATEGORIES[0]), 'rb') as csvfile: # doesn't matter which stock, just read the date column
    dates = []
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
      dates.append(row[DATE_COLUMN_INDEX])
    return dates[1:]

def retryLoop(retrySymbols):
  trynum = 2
  while not retryDownloads(retrySymbols, trynum) and trynum < 10: # try 10 times
    print 'Retrying all downloads --- try # ' + str(trynum)
    trynum += 1
    continue

stockSymbols = readListFromFile(STOCK_LIST_FILENAME)

# ---- DOWNLOAD DATA CODE ----
# driver = webdriver.Chrome(chromedriver)
# signIntoWolfram('userinfo.txt')
# # downloadFundamentalCSVs(stockSymbols) # if already downloaded, comment this out
# retrySymbols = readListFromFile(STOCK_LIST_FILENAME)
# retryLoop(retrySymbols)