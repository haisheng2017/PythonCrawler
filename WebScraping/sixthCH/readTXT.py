# from urllib.request import urlopen
# textPage = urlopen("http://www.pythonscraping.com/pages/warandpeace/chapter1.txt")
# print(textPage.read())
from urllib.request import urlopen
from io import StringIO
import csv

data = urlopen("http://pythonscraping.com/files/MontyPythonAlbums.csv").read().decode('ascii', 'ignore')
dataFile = StringIO(data)
# csvReader = csv.reader(dataFile)
dictReader = csv.DictReader(dataFile)
for row in dictReader:
    print(row)