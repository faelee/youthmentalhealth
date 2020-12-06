# Youth Mental Health Research Project
## scrapeByDate.py
1. On line 50, input your Reddit login and project information.
>[Click here](https://towardsdatascience.com/scraping-reddit-data-1c0af3040768) and go to the "Getting Started" Header to see how to create a Reddit project and find out what Client ID, Client Secret, and User Agent are. <br />
2. After running the code, follow printed directions in Terminal for inputting the Subreddit name and start and end dates. 
>* For setting Subreddit name, on line 27, you can also set `subreddit =` to the name of your subreddit.  <br />
Make sure to follow the exact spelling and punctuation of the Subreddit. For example, if your Subreddit was r/NFlying, you would type `subreddit = NFlying`
>* For setting start date, on line 33, you can also replace `yearB`, `monthB`, and `dayB` in `dtB = datetime(yearB, monthB, dayB)` with the start year, month, and day, respectively.  <br />
Make sure to write your year in 4 digits (ex. 2020), your month in 2 digits (ex. 01), and your day in 2 digits (ex. 01).
>* For setting end date, on line 40, you can also replace `yearA`, `monthA`, and `dayA` in `dtA = datetime(yearA, monthA, dayA)` with the end year, month, and day, respectively. <br />
Make sure to write your year in 4 digits (ex. 2020), your month in 2 digits (ex. 01), and your day in 2 digits (ex. 01). <br />
## sameId.py
>Make sure your file names are different
1. On line 10, specify the csv for the comments of your first subreddit: `with open(PUT YOUR CSV FILE NAME HERE EX AC.CSV, 'rt') as csvfile:`
2. On line 15, specify the csv for the posts of your first subreddit
3. On line 20, specify the csv for the comments of your second subreddit
4. On line 25, specify the csv for the posts of your second subreddit
5. On lines 47, 49, 52, 54, 57, 59, 62, and 64, specify your two subreddits: <br />
Ex: `writer.writerow(['' + value, 'PUT THE NAME OF YOUR FIRST SUBREDDIT HERE Comment', 'PUT THE NAME OF YOUR SECOND SUBREDDIT HERE Post'])`

#### Notes about the .csv files
* Sometimes the author name will be blank because the user who posted the subreddit has since deleted their account.
