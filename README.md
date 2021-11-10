# Amy's HW 3 - Web Scraping
**This is how my `ebay-dl.py` file scrapes item data from eBay and saves the information on the search term as a JSON file.**

---
## Scraping Data and Storing them in a JSON File

The `ebay-dl.py` file scrapes eBay's html code to create a JSON file of their product data. 

The `ebay-dl.py` file does the following:
1. Takes the search term from command line
2. Builds the url to download the html code
3. Processes the html to collect information on product `name`, `price`, `status`, `shipping cost`, `free returns`, and `items_sold`.
4. Loops over the items in the page
5. Loops over to collect data from the first 10 pages of search results
6. Writes and saves the list as a new JSON file

## Running Command Lines
Run the following command on `ebay-dl.py` with your search term of choice:
```
python ebay-dl.py 'search term'
```

**NOTE:** If your search term consists of more than a signle word, make sure to put quotation marks around the search term.

### Example: the commands I ran
To search for `christmas` I put the following command in the terminal:
```
python ebay-dl.py christmas
```
which created the [christmas.json](https://github.com/kimsngmin00/HW_03/blob/main/christmas.json) file.

To search for `fake plants` I put:
```
python ebay-dl.py 'fake plants'
```
which created the [fake plants.json](https://github.com/kimsngmin00/HW_03/blob/main/fake%20plants.json) file.

To search for `projector` I put:
```
python ebay-dl.py projector
```
which created the [projector.json](https://github.com/kimsngmin00/HW_03/blob/main/projector.json) file.

---
[**Click here**](https://github.com/mikeizbicki/cmc-csci040/tree/2021fall/hw_03) to see the course project. 
