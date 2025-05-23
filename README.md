# CS50P Project - Visa Tool 🛂
[![SLOC](https://sloc.xyz/github/erikw/cs50p-project?lower=true)](#)
[![Number of programming languages used](https://img.shields.io/github/languages/count/erikw/cs50p-project)](#)
[![Top programming languages used](https://img.shields.io/github/languages/top/erikw/cs50p-project)](#)
[![Number of files in repo](https://img.shields.io/github/directory-file-count/erikw/cs50p-project)](#)
[![Repo file size](https://img.shields.io/github/repo-size/erikw/cs50p-project
)](#)
[![Latest tag](https://img.shields.io/github/v/tag/erikw/cs50p-project)](https://github.com/erikw/cs50p-project/tags)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://black.readthedocs.io/en/stable/the_black_code_style/current_style.html)

[![Tests](https://github.com/erikw/cs50p-project/actions/workflows/tests.yml/badge.svg)](https://github.com/erikw/cs50p-project/actions/workflows/tests.yml)
[![Lint](https://github.com/erikw/cs50p-project/actions/workflows/linter.yml/badge.svg)](https://github.com/erikw/cs50p-project/actions/workflows/linter.yml)
[![CodeQL](https://github.com/erikw/cs50p-project/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/erikw/cs50p-project/actions/workflows/codeql-analysis.yml)
[![Dependabot Updates](https://github.com/erikw/cs50p-project/actions/workflows/dependabot/dependabot-updates/badge.svg)](https://github.com/erikw/cs50p-project/actions/workflows/dependabot/dependabot-updates)

<p align="center">
    <!-- Ref: https://dev.to/azure/adding-a-github-codespace-button-to-your-readme-5f6l -->
    <a href="https://github.com/codespaces/new?hide_repo_select=true&ref=main&repo=917050205" title="Open in GitHub Codespaces" ><img alt="Open in GitHub Codespaces" src="https://github.com/codespaces/badge.svg"></a>
</p>

Final [project](https://cs50.harvard.edu/python/2022/project/) in the [CS50P](https://cs50.harvard.edu/python/2022/) Python course.

## Demo
<a href="https://youtu.be/cyB0gfufMFk" title="View demo video"><img src="img/demo_video_preview.png" width="580" alt="Demo Video Preview"></a>

*Demo URL: https://youtu.be/cyB0gfufMFk*


## Achievements
Official certificate awared as of completion of this course:

<a href="https://cs50.harvard.edu/certificates/19eba3e9-7198-4909-a320-eebd70f26b70" title="Official certificate"><img src="img/cert_thumbnail.png" width="300" alt="Certificate Preview"></a>

*Verification URL: https://cs50.harvard.edu/certificates/19eba3e9-7198-4909-a320-eebd70f26b70*


## Problem Description
For this project I chose to write a tool that solves a problem I know well, a problem I often have in my life. This makes it all more motivating as well to develop! As a frequent traveler, I'm often faced with two problems:

* I need to research Visa and entry information for a new country that I am interested in or are going to visit, to arrange Visa applications etc. in time. Going out on Google each time and find a different site for each country has some problems with assessing the trustworthiness of the found sound, and maybe even translate the language to English.

* Once I've actually arrived in a country with an entry stamp in my passport, the visit is typically valid for X number of days since the day of entry e.g. 60 or 90 days. It's important to mark in my calendar the exact last day I can stay in the country, to not get in trouble with overstaying. The problem is to calculate that. Given different month lengths and leap years, and having to remember that the day of entry counts as day 1, it's easy to calculate the wrong date +/-1.

These two problems I've solved with the **Visa Tool** developed in this project.

I took this course not to learn Python (though I did learn some new things that I've not seen or noticed before in the language!), but to be able to help other students learn Python by taking this course.

## Solution
To solve these two related but distinct problems, the Visa Tool operates in two modes each targeting the respective problems.

To get Visa information, the best source I could find on the Internet is [projectvisa.com](https://www.projectvisa.com/) that has information for all countries in the world. While not authoritative, it gives a good enough presentation for the initial Visa research. Additionally it has links to the official websites for each country to check. This satisfies my needs. Unfortunately there's no public API, so I had to resort to web scraping, just showing the text part of the rendered HTML. Considering that this is a tool used to query the website maybe 1-2 times a month or so, this should not cause any denial of service.

To calculate the last allowed day to stay in a country, the two parameters are the date of entry in the county and the length of allowed stay. Now this is not rocket science directly, it's a matter of one addition and one subtraction operation. The key is to actually add and subtract the right things (every time), which is why this is a helpful tool compared to manual calculating or finger counting in the calendar.

## Usage
If you don't specify any CLI arguments, the program will launch in interactive mode. Run the program with `-h` or `<command> -h` for the most up to date help descriptions.


```command
$ pip install -r requirements.txt
$ ./project.py -h
 _   _  _               _____                _
| | | |(_)             |_   _|              | |
| | | | _  ___   __ _    | |    ___    ___  | |
| | | || |/ __| / _` |   | |   / _ \  / _ \ | |
\ \_/ /| |\__ \| (_| |   | |  | (_) || (_) || |
 \___/ |_||___/ \__,_|   \_/   \___/  \___/ |_|


usage: Visa Tool [-h] [-v] {visa_info,exit_calc} ...

Utility for Visa related queries. See subcommands.

positional arguments:
  {visa_info,exit_calc}
                        Optional Commands. If none is given, the program will
                        run in interactive mode. Run $(python project.py
                        <command> -h) for more info about a command.
    visa_info           Get Visa information for a country.
    exit_calc           Calculate the last day you can stay in a country given
                        the entry date and entry stamp validity length.

options:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit

Find support and source code at https://github.com/erikw/cs50p-project
```

## Implementation
Here's a brief implementation description in the format of looking at each module and file's responsibility and actions.

For this project, I opted to add [type hints](https://docs.python.org/3/library/typing.html) and check with the [`mypy`](https://github.com/python/mypy) tool for compliancy.

#### :page_facing_up: [`.gitignore`](.gitignore)
Self-explanatory. What to ignore from being tracked in the VCS.

#### :page_facing_up: [`.mypy.ini`](.mypy.ini)
Configuration file for the static type checker.

#### :page_facing_up: [`.pytest.ini`](.pytest.ini)
Configuration file for `pytest`. Needed to work around a [bug](https://github.com/Exahilosys/survey/issues/38) that I discovered in the library I used for user input querying.

#### :page_facing_up: [`constants.py`](constants.py)
Contains all constants. I broke these out to its own module to avoid circular dependencies between modules that use the same constants.

#### :page_facing_up: [`countries.csv`](countries.csv)
This is a static list of all allowed countries that projectvisa.com knows about. It's in the format that is used in their URL scheme as there could be different ways of abbreviating or styling a country's name. A future extension of this program would introduce a second column being the display name, and use this in the interactive ui selector.

#### :page_facing_up: [`mode_cli.py`](mode_cli.py)
When the CLI mode is activated the functions in this module are used to parse CLI arguments and call the requested functionality with the right parameters.

#### :page_facing_up: [`mode_interactive.py`](mode_interactive.py)
When the program is launched in interactive mode (meaning no CLI args), then the functions in here will take care of querying the user in the right order for the feature to activate and the corresponding parameters needed for that feature.

#### :page_facing_up: [`project.py`](project.py)
This is the main module, as per specified mandatory naming convention according to the problem description. The main module will set up a signal handler for the SIGINT (ctr+c) signal and handle a clean exit, print a welcome screen with ASCII art, and then chose to start the program in CLI or interactive mode as determined by whether or not any CLI arguments was passed by the invoker.

#### :page_facing_up: [`requirements.txt`](requirements.txt)
Pip Python package manager listing needed runtime dependencies and development tools used.

#### :page_facing_up: [`test_project.py`](test_project.py)
Testing functions in `project.py` according to the naming conventions layed out in the problem description.

#### :page_facing_up: [`ui.py`](ui.py)
This module takes responsibility for producing much of the output of the user and the formatting of this.

#### :page_facing_up: [`visa.py`](visa.py)
The Visa module contains the main business logic of this program including date calculation and Visa information fetching and parsing.


## Development
Remember to run:
```command
$ pip install -r requirements.txt
$ pytest
$ mypy .
$ isort .
$ black .
```
