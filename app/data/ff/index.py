import datetime
import logging
from csv import writer

from pandas import read_csv
from bs4 import BeautifulSoup
from requests import get


def setLogger():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename='logs_file', filemode='w')
    console = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

def getEconomicCalendar(startlink, endlink):
    logging.info("Scraping data for link: {}".format(startlink))
    baseURL = "https://www.forexfactory.com/"
    r = get(baseURL + startlink)
    data = r.text
    soup = BeautifulSoup(data, "lxml")
    table = soup.find("table", class_="calendar__table")
    trs = table.select("tr.calendar__row.calendar_row")
    fields = ["date", "time", "currency", "impact", "event", "actual", "forecast", "previous"]
    curr_year = startlink[-4:]
    curr_date = ""
    curr_time = ""

    for tr in trs:
        try:
            for field in fields:
                data = tr.select("td.calendar__cell.calendar__{}.{}".format(field,field))[0]
                if field=="date" and data.text.strip()!="":
                    curr_date = data.text.strip()
                elif field=="time" and data.text.strip()!="":
                    # time is sometimes "All Day" or "Day X" (eg. WEF Annual Meetings)
                    if data.text.strip().find("Day")!=-1:
                        curr_time = "12:00am"
                    else:
                        curr_time = data.text.strip()
                elif field=="currency":
                    currency = data.text.strip()
                elif field=="impact":
                    # when impact says "Non-Economic" on mouseover, the relevant
                    # class name is "Holiday", thus we do not use the classname
                    impact = data.find("span")["title"]
                elif field=="event":
                    event = data.text.strip()
                elif field=="actual":
                    actual = data.text.strip()
                elif field=="forecast":
                    forecast = data.text.strip()
                elif field=="previous":
                    previous = data.text.strip()

            dt = datetime.datetime.strptime(",".join([curr_year,curr_date,curr_time]),
                                            "%Y,%a%b %d,%I:%M%p")
            print(",".join([str(dt),currency,impact,event,actual,forecast,previous]))
        except:
            with open("errors.csv","a") as f:
                writer(f).writerow([curr_year,curr_date,curr_time])

    if startlink==endlink:
        logging.info("Successfully retrieved data")
        return

    follow = soup.select("a.calendar__pagination.calendar__pagination--next.next")
    follow = follow[0]["href"]
    getEconomicCalendar(follow, endlink)

def load_data():
    df = read_csv('calendar.csv').dropna()
    df.columns = ["date", "currency", "impact", "event", "actual", "forecast", "previous"]
    df.set_index("date")
    for i in range(len(df.index)):
        row = df.iloc[i]
        row["impact"] = row["impact"].replace(" Impact Expected", "")
        cols = ["actual", "forecast", "previous"]
        for col in cols:
            row[col] = row[row].replace("%", "")
            row[col] = row[row].replace("B", "")
            row[col] = row[row].replace("M", "")
            row[col] = row[row].replace("K", "")
    return df

if __name__ == "__main__":
    setLogger()
    with open("calendar.csv", "a") as f:
        writer(f).writerow(getEconomicCalendar("calendar.php?week=dec25.2007", "calendar.php?week=jul3.2018"))
    load_data()
