**get_textfiles** - This is the primary script that impliments the procedures from utils and scrapers on all listed nurseries.

**get_matches** - A program that checks for plants in each text file associated with the nurseries. The output is a long DataFrame of (Symbol,Nursery,URL) and an aggregate 
DataFrame of (Symbol, list of urls).

**utils** - A py file that contains the methods for each file extension.

* For non-html extensions, the general procedure is as follows: use the response module to make an http request to the 
url, store to tmp as a binary file, read in using the requisite module, remove embeddings, then write to a text file. 
* For html extensions, use the response module to make an http request to the url. Then, use BeautifulSoup to extract the text from the file.


**scrapers** - Contains methods for grabbing urls for each web page
