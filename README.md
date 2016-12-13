## Crawler for Yahoo Buy

### Description/Target <br>
This is a my first crawler homework for Scrapy and my target is to get best sell product of Yahoo shop. <br>

### Strategy
Currently, I have no idea what is the best analysis althgorim for predict the best product of Yahoo shop, therefore, I decide to follow the billboard of Yahoo to retrieve the potential goods for sell.

### Data Flow <br>
web content -- [parsed by] -- > crawler -- [save to] --> SQLite DB -- [read by] --> report

### File Structures<br>
$ tree ./ <br>
./ <br>
├── README.md <br>
├── Yahoo.sqlite <br>
├── juvoplus2 <br>
│   ├── \_\_init\_\_.py <br>
│   ├── items.py <br>
│   ├── pipelines.py <br>
│   ├── settings.py <br>
│   ├── spiders <br>
│   │   ├── \_\_init\_\_.py <br>
│   │   ├── crawler.py <br>
│   │   ├── db.py <br>
│   │   └── report.py <br>
│   └── tests <br>
│       ├── \_\_init\_\_.py <br>
│       ├── db\_test.py <br>
│       └── report\_test.py <br>
├── run\_crawler.sh <br>
├── run\_report.sh <br>
└── scrapy.cfg <br>

### Libraries <br>
1. CRAWLER:
	1. scrapy
	2. beautiful soup
	3. json
	4. sqlite3
2. REPORT:
	1. sqlite3 
	2. argparse
3. TEST:
	1. unittest

### HOW-TO
1. run crawler script: <br> 
$ ./run_crawler.sh
2. run report script: <br> 
$ ./run_report.sh -u TOP\_TEN\_FOR\_ALL <br>

### The Road Ahead
1. CRAWLER:
	1. Current target url is a static string, maybe could get target url by parsing java script.
	2. Only parse "Billboard" of Yahoo, could parse more categories to enrich data.
2. REPORT:
	1. Only support 2 use cases, could support more.
3. SYSTEM LIMITATION/POTENTIAL RISK:
	* When we try to retrieve more content from Yahoo, the possible limitation of this crawler is performance and we could have several aspect to enhance it.
		1. Replace SQLite with MySQL/PostgreSQL
		2. I have put scrapy framework in the script and when we want to have more client to parse data, we could leverage "Twisted" framework to empower our spiders. 

### Example
$ ./run_report.sh -h
usage: report.py [-h] [-U] [-u USECASES] [-s SORT_UP_DOWN] <br>
<br>
optional arguments: <br>
  -h, --help       show this help message and exit <br>
  -U               List Usecases <br>
  -u USECASES      Apply Usecase <br>
  -s SORT_UP_DOWN  Apply sort sequence (asc/desc), default is desc  <br>
<br> 
$ ./run_report.sh -U <br>
TOP_TEN_FOR_ALL <br>
TOP_TWO_PER_CATEGORY <br>
<br>
$ ./run_report.sh -u TOP_TEN_FOR_ALL <br>
電視,CHIMEI 奇美 TL-50W600 50吋 廣色域智慧聯網顯示器+視訊盒,20900.0 <br>
電冰箱,樂金LG 253公升Smart 變頻上下門冰箱GN-L305SV,16900.0 <br>
電視,CHIMEI 奇美 TL-43W600 43吋 廣色域智慧聯網顯示器+視訊盒,15900.0 <br>
電冰箱,樂金LG 186公升Smart 變頻上下門冰箱GN-L235SV,14900.0 <br>
電冰箱,聲寶250L經典品味雙門電冰箱SR-L25G(S2)璀璨銀,14200.0 <br>
電冰箱,TOSHIBA東芝226L二門電冰箱GR-S24TPB(含運送和基本安裝),11900.0 <br>
電冰箱,聲寶140L經典品味雙門冰箱SR-L14Q(S1),11400.0 <br>
歐系精品包 / 配件,【萬寶龍】小牛皮4810   6卡皮夾,8280.0 <br>
歐系精品包 / 配件,LONGCHAMP Fantaisie質感尼龍短把手提/斜背兩用水餃包(芙蓉紅/中),7980.0 <br>
歐系精品包 / 配件,LONGCHAMP 尼龍短把手提/斜背兩用水餃包(中/深藍),6100.0 <br>
  

