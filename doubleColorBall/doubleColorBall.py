import requests
from lxml import etree
import matplotlib.pyplot as plt
from pandas import Series

url = "http://datachart.500.com/ssq/history/newinc/history.php?start=00001&end=20115"
response = requests.get(url)
response = response.text
selector = etree.HTML(response)
reds = []
blues = []
for i in selector.xpath('//tr[@class="t_tr1"]'):
    datetime = i.xpath('td/text()')[0]
    red = i.xpath('td/text()')[1:7]
    blue = i.xpath('td/text()')[7]
    for i in red:
        reds.append(i)
    blues.append(blue)

s_blues = Series(blues)
s_blues = s_blues.value_counts()
s_reds = Series(reds)
s_reds = s_reds.value_counts()

labels_blues = s_blues.index.tolist()
sizes_blues = s_blues.values.tolist()
rect_blues = plt.bar(range(len(sizes_blues)) , sizes_blues , tick_label = labels_blues)
plt.show()


labels_red= s_reds.index.tolist()
sizes_red = s_reds.values.tolist()
rect_red = plt.bar(range(len(sizes_red)) , sizes_red , tick_label = labels_red)
plt.show()