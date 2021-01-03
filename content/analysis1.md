Title: Some Developers create 20x more bugs than others - here's what we can do about it
Date: 2021-01-03

Over the last year I've been on a mission to discover new ways of improving ROI for development teams. 
As part of my work on predicting the probability of a bug in a commit, I've been analysing some large projects and used the data to train machine learning models.
One of the most striking things I've found is the difference between the number of bugs individual developers create. It's something that people on a development team will intuitively know, but we rarely measure. It's the elephant in many team rooms, which is a shame because it's one of the largest causes of slow delivery, missed deadlines and unhappy customers. And it's fixable. 

## Analysis

I've analysed bugs in over 300 repositories over the last year. Here are 3 of the largest and most active. 
For each repo below I extracted all the commits between June 2019 and June 2020 (ignoring the most recent commits where the bugs may not have been found yet).
For every fix I find the source commit and log a bug against the committer.
I've ignored any developer who has added less than 1000 lines of code in the period as the sample size will be too small.
Here's the results:

### Microsoft ASP.NET Core

Over the year there were 3567 commits, 1156 of these contained a bug. 
On average, the 34 developers who contributed more than 1000 lines of code, created a bug every 58 lines of code added.

* 2 Developers create less than 1 bug every 1000 lines of code added
* 4 Developers create less than 1 bug every 500 lines of code added
* 8 Developers create more than 1 bug every 50 lines of code added
* 5 Developers create more than 1 bug every 25 lines of code added

![PR Review Image]({static}/images/aspnetcore_analysis.png)


### Google Angular

Over the year there were 3619 commits, 1397 of these contained a bug. 
On average, the 32 developers who contributed more than 1000 lines of code, created a bug every 79 lines of code added.

* 2 Developers create less than 1 bug every 1000 lines of code added
* 5 Developers create less than 1 bug every 500 lines of code added
* 4 Developers create more than 1 bug every 50 lines of code added
* 1 Developers create more than 1 bug every 25 lines of code added

![PR Review Image]({static}/images/Angular_analysis.png)

It's uncanny how similar these two repo stats are. 

### Facebook React

Over the year there were 1485 commits, 616 of these contained a bug. 
On average, the 13 developers who contributed more than 1000 lines of code, created a bug every 102 lines of code added.

* 0 Developers create less than 1 bug every 1000 lines of code added
* 1 Developers creates less than 1 bug every 500 lines of code added
* 1 Developers creates more than 1 bug every 50 lines of code added
* 0 Developers create more than 1 bug every 25 lines of code added

![PR Review Image]({static}/images/react_analysis.png)

As you can see React repo has the lowest level of bugs and the lowest variance, they are certainly doing something right. 
Could it be something to do with the smaller core team?

## Why is there such a large variance between developers?

From the figures we can see that it's common to see a 20x variance between the number of bugs created. We all have different strengths, 
whilst we might excel at finding creative solutions to tricky problems, we might be less good at writing tests or overcoming an urge to just get it done. 
Experienced developers often develop an intuition to know when they are not really done, particularly if they are in an environment where they are free of organisational pressure and this can result in them creating far fewer bugs than a relative novice. 
It's not all about the individual - Organisational structure, culture and size is likely to be one of the main contributors to variance between repos, something outlined [here](https://augustl.com/blog/2019/best_bug_predictor_is_organizational_complexity/) (Thanks Gareth ;-))

## Why don't we collect and share these stats for our own repos?

We all want to create safe environments for our teams, but these stats are emotive and sharing them risks triggering deep insecurities.
If they generate a fear of being judged, people may focus on reducing the bugs they create by not committing any code at all. 
One solution to this is to create a balanced set of measures, however more measures can start to feel bureaucratic and create a culture of suspicion.
Every Manager I've shown these measures to have asked me to make them available just to them - this makes me even more nervous!
In the rare case where leaders have managed to create a truly safe environment, sharing your stats and having an open honest dialogue about them could be the start of a big change. 
But who is confident enough to take the risk?

## So what can we do?

To save developers embarrassment and customers frustration we must be able to spot these bugs before they are committed. 
When we combine our strengths and work as a team to collaborate on commits we can raise the bar of the team to that of the member with the lowest bug density.
There are many ways we can do this, code reviews are good as is a team huddle to discuss the risks. Pairing is better - it catches the issues before they are written. 

If we understand where the risks lie before committing, and collaborate to focus our collective abilities, we can catch a large proportion of these bugs before they reach the wild. The best teams do this intuitively. For the rest of us I've created [ReviewML](https://www.solittlecode.com/reviewml) to help.

