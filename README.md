# Visa Tool
[![SLOC](https://sloc.xyz/github/erikw/cs50p-project)](#)
[![Number of programming languages used](https://img.shields.io/github/languages/count/erikw/cs50p-project)](#)
[![Top programming languages used](https://img.shields.io/github/languages/top/erikw/cs50p-project)](#)
[![Latest tag](https://img.shields.io/github/v/tag/erikw/cs50p-project)](https://github.com/erikw/cs50p-project/tags)

Final project in the [CS50p](https://cs50.harvard.edu/python/2022/) Python course.

## Demo
Demo URL:

## Problem Description
For this project I chose to write a tool that fulfils that solves I problem I know well. This makes it all more motivating as well to develop! As a frequent traveler, I'm often faced with to problems:

* I need to reserach Visa and entry information for a new country that I am interested in visiting, to arrange Visa applications etc. in time. Going out on Google each time and find a different site for each country has some problems of assessing the trustworthiness of the found sound, and maybe even translate the language to English.

* Once I've actually arrived in a country with an entry stamp in my passport, the visit is typically valid for X number of days since the day of entry e.g. 60 or 90 days. It's important to mark in my calendar the exact last day I can stay in the country, to not get in trouble with overstaying. The problem is to calculate that. Given different month lengths and leap years, and having to remember that the day of entry counts as day 1, it's easy to calculate the wrong dayte +/-1.

These two problems I've solved with the **Visa Tool** developed in this project.

I took this course not to learn Python (though I did learn some new things that I've not seen or noticed before in the language!), but to be able to help other students learn Python by taking this course.

## Solution
To solve these two related but distinct problems, the Visa Tool operates in two modes each targeting the respective problems.

To get Visa information, the best source I could find on the Internet is [projectvisa.com](https://www.projectvisa.com/) that has information for all countries in the world. While not authorative, it gives a good enough presentation for the initial Visa research. Additoinally it has links to the official websites for each country to check. This satisifes my needs. Unfortuantely there's no public API, so I had to resort to web scraping, just showing the text part of the rendered HTML. Considering that this is a tool used to query the website maybe 1-2 times a month or so, this should not cause any denial of serivce.

To calculate the last allowed day to stay in a country, the two parameters are the date of entry in the county and the length of allowed stay. Now this is not rocket science directly, it's a matter of one addition and one substraction operation. The key is to actually add and substract the right things (every time), which is why this is a helpful too compared to manual calculating or finger counting in the calendar.

## Implementation
Here's a brief implementation description in the format of looking at each module's responsibility and actions.
[0m[01;34m.[0m/
[01;34m..[0m/
constants.py
countries.csv
[01;34m.git[0m/
.gitignore
mode_cli.py
mode_interactive.py
[01;34m.mypy_cache[0m/
.mypy.ini
[01;32mproject.py[0m*
[01;34m.pytest_cache[0m/
.pytest.ini
README.md
requirements.txt
test_project.py
TODO.md
ui.py
visa.py
[01;34m.vscode[0m/
