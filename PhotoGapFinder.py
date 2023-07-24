from PIL import Image
from os import listdir
from os import walk
from os import getcwd
#from os.path import isfile, join
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
#beg = input("Starting Date? YYYY:MM:DD\n")
#end = input("Ending Date? YYYY:MM:DD\n")
sep = int(input("Detectable Gap Size? (Days)\n"))
fileextensions = [".jpg"];
def dayssinceepoch(yyyymmdd):
    return (datetime.datetime(int(yyyymmdd[0:4]), int(yyyymmdd[5:7]), int(yyyymmdd[8:10])) - datetime.datetime(1970,1,1)).days
phototimes = []
phototimesepoch = []
gaps = []
subdirs = [x[0] for x in walk(getcwd())]
for i in subdirs:
    items = listdir(i)
    for j in items:
        flag = False
        for k in fileextensions:
            if j.endswith(k):
                flag = True
        if flag:     
            phototimes.append(Image.open(i+'\\'+j).getexif().get(36867))
            if phototimes[-1] == None:
                phototimes.pop(-1)
                phototimes.append(Image.open(i+'\\'+j).getexif().get(306))
                if phototimes[-1] == None:
                    phototimes.pop(-1)

phototimes.sort()
for i in range(len(phototimes)):
    phototimesepoch.append(dayssinceepoch(phototimes[i][0:10]))
for i in range(1, len(phototimes)):
    if phototimesepoch[i] - phototimesepoch[i - 1] > sep:
        gaps.append([phototimes[i-1], phototimes[i]])

print('Seperations:',gaps,'\n')
print('All photos:',phototimes)

["01/02/2020", "01/03/2020", "01/04/2020"]

scatter = [datetime.datetime.strptime(d[0:10],"%Y:%m:%d").date() for d in phototimes]
x_values = []
y_values = []
#print(scatter)
for i in range(len(scatter)):
    if scatter[i] not in x_values:
        x_values.append(scatter[i])
        y_values.append(1)
    else:
        y_values[x_values.index(scatter[i])] += 1;

ax = plt.gca()
formatter = mdates.DateFormatter("%Y-%m-%d")
ax.xaxis.set_major_formatter(formatter)
locator = mdates.DayLocator()
ax.xaxis.set_major_locator(locator)
locator.MAXTICKS = 100000
plt.scatter(x_values, y_values, s=3)
#plt.gcf().autofmt_xdate()
plt.show()
