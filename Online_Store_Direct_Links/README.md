The goal of this project is to provide the most optimal solution for redirecting users to plants listed on external sites. We currently redirect users to the site's hompeage. In a perfect world, they would click on the link and immediately be brought to the sites listing of the plant. Unfortunately, due to plants going out of stock, differences in naming and changes in urls - this is not feasible. 

The three alternatives are:

1. Direct links which use a common url pattern i.e. ww<span>w.ernstseed.com/product/{Common Name}. These work if the names we have in our database match the names the site uses. 

2. Search links which use the sites search tool (if they have one). For example, ww<span>w.izelplants.com/catalogsearch/result/?q={scientific_name}. Errors arise from the plant being out of stock, or a poorly designed search tool. 

3. Duckduckgo links that redirect to the most popular link from a query on the sites name and the scientific name of the plant. All the previously mentioned problems arise using these links. 

The solution I designed iterates through each of these links. If the page the link resolves to has the root (EnrnstSeed.com) in the url and the plants name on the page, that's the link we'll use. The heirarchy is Direct -> DuckDuckGo -> Search. In the case where none of them work, we use the sites homepage, just as before. 


__Update__

The code determining the correct urls is obselete. All online availability data is being regathered using the scripts in Scraping
