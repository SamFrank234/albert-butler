# albert-butler
NYU's class registration system (named "Albert" after Albert Gallatin), is notoriously difficult to navigate.
It's even harder to use when you want to also check out professor scores from RateMyProfessor. I built this project
to make well-informed class registration at NYU much simpler. Here's what I built and what I learned:

1. WebScraping

First I had to get data from RateMyProfessor. As far as I knew, they had no public API (more on that later) so I 
decided to learn scraping. I used Selenium and ChromeDriver to collect information about every professor at NYU.
This got the job done, but all the pop-up ads on RMP were messing with the automation, so I had to monitor the process,
which wasn't ideal. If I feel like redoing it, I will probably check out headless chrome. A few months after wrapping up,
while I was checking out other similar projects for other schools, I noticed that instead of webscraping these projects
were hitting an RMP API. I tried out the url, and, lo and behold, it still worked! However, I could not find any documentation
or even any reference of this API online, so I figured it had not been maintained or updated for some time and the data would
not be up to date. I spent a lot of time trying to guess some other endpoints, but I didn't find anything interesting.

2. REST API

Now that I had my data, I needed to set up access, so I made a quick REST API using the Django framework. This was my intro to
Django, APIs, and web dev (and my first real Python programming), so I learned a lot even from a pretty simple project. I hosted
this on Heroku's free tier with a PostgreSQL db included, but they discontinued that tier and I didn't think it was worth it to pay,
so I took down my API. I never got to spread it to as many users as I hoped, but I did use it myself and sent it to a couple of my
friends who all said it was really useful, so I can feel a little proud of my little project :).

3. Chrome Extension

I decided on a chrome extension as the front end for a couple reasons: FE design wasn't (and still isn't) one of my strengths, and 
more importantly, using an extension helped me bypass the tricky problem of Albert authentication. Any student could log in, load
the course registration page, and then run the extension with access to all the information I needed right in the HTML. Finding this
information proved trickier than expected, as the registration page was very complex, with opaque naming conventions and seemingly 
infinitely nested components, but I finally managed to get the info I needed form the developer tools console in my browser. Unfortunately,
I just could not manage to get it to work in my code. Finally, after reading throguh what felt like the entirety of the Mozilla DOM docs,
I realized that the class registration page came up in a pop-up iframe, which acted like its own document with its own permissions. I 
changed my payload JS script double inject into this iframe, and that solved it, many hours later! 

Summary:
Overall, this was a great project. I learned a lot of new skills, including Django, HTML/DOM, Javascript, and web scraping, and I built
something with real value for a sizeable population of target users. Even though I ended up taking this down before publishing it, I am
proud of what I built and how I built it. Feel free to look around!
