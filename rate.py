import numpy as np
from matplotlib import pyplot as plt
from matplotlib import dates
import datetime as dt
import urllib.request
import re
import calendar
import sys

area = "san-mateo-ca"
if len(sys.argv) > 1:
	area = sys.argv[1]
url = "https://coronavirus-sf.now.sh/" + area + ".html"

days_data = []
cases_data = []
months = list(calendar.month_abbr)
html = urllib.request.urlopen(url).read().decode("utf-8")
regex = re.compile(r"\[\'([a-zA-Z]+) ([0-9]+)\', ([0-9]+), ([0-9]+)\]")
for match in regex.finditer(html):
	date = str(months.index(match.group(1))) + "/" + match.group(2) + "/2020"
	days_data.append(date)
	cases_data.append(int(match.group(3)))

cases = np.asarray(cases_data)
grad = np.gradient(cases)

date_list = [dt.datetime.strptime(x, "%m/%d/%Y") for x in days_data]

ax = plt.gca()

formatter = dates.DateFormatter("%m-%d")
ax.xaxis.set_major_formatter(formatter)

locator = dates.AutoDateLocator()
ax.xaxis.set_major_locator(locator)

plt.title(url + " Cases Gradient")
plt.xlabel("Date")
plt.plot(date_list, grad)
plt.savefig("out.png")