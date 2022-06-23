First of all used pandas to get the country and asin value. And adds these values to the string to make the required link 
and then uses that link to download the HTML content and parse it using the bs4 library and search the required with a particular id
or class value. After we put this value in the dictionary and put the dictionary in a list after converting the list into JSON format.