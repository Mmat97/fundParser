# fundParser
fundParser

## fundParser
fundParser



## Advantages
1.Parses fund holdings pulled from EDGAR, given a ticker or CIK
2. Generates a .tsv file



## Installation and Run 
**Install:** 

```
	pip3 install requests
```

```
	pip3 install beautifulsoup4
```

```
	pip3 install lxml
```


**Run:** 

To start, in fundParser directory, 

```
	python3 -m main (ticker or CIK)
```





## Tools/Languages/References
**Language:** 

[Python3.7](https://www.python.org/downloads/)

**OS Used:** 

-Mac OS(Terminal)

**Editors:** 
-Visual Studio Code 




## Functions

def get_url(tickorcik): get search results 

def handle_13FHR(url, forms): get 13F page 

def check_13F_format(file_page): check format of 13F page 

def get_holdings_table(archive_url): obtain link to actual table

def convert_holdings_tsv(fund_url):convert table to tsv 

## Example

```
python3 -m main 0001166559
```

output.tsv file in fundParser directory contains the newly outputted tsv data for the given ticker, 
in this case the table for Gates Foundation