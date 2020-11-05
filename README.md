# Youth Mental Health Research Project
1. On line 74, specify the name of the subreddit using a string with `subreddit = ""` (ex. for r/SF9, you would type `subreddit = 'SF9'`) 
2. On line 89, input your Reddit login and project information. 
>Here is the link to creating a Reddit project and specification of Client ID, Client Secret, and User Agent: 
>(Getting Started" Header) https://towardsdatascience.com/scraping-reddit-data-1c0af3040768
3. The end date is automatically set to the current time on line 72, with `datetimend_at = math.ceil(datetime.utcnow().timestamp())`
4. The start date is specified on line 76. In the segment `timedelta(days=20)`, input the number of days you want to go back (ex. to go back a year, input `days=365`)
 
