# GITalyzer

##  Summary:
GITalyzer is a git patch analyzer which does string and syntax level parsing to analyze and generate reports for the repositories written in Python. Below is the working of parser. 

To run the parsers first run:
`python3 issues.py`

This will download a number of patch files from Python respositories and save them under ***Repos/repo_name/*** directory.

After the downloads are finished, run:
`python3 analyzer.py`

This script will runn mutiple analysis on a syntax-level and generate reports according to the results.

The reports are *.svg* files and can be opened with a browser or any 3rd part application of your choice.

* * *

## Flow Diagram:

![Flow Diagram](https://bitbucket.org/sjoshi37/sandeep_joshi_debojit_kaushik_hw2/raw/cf3c892aae0b51b5e255a0e40fd9697cb8a848a6/readme_images/analyzer_flow.jpeg)

Example output graph:
![Frequency analysis](https://bitbucket.org/sjoshi37/sandeep_joshi_debojit_kaushik_hw2/raw/7d0f5c85485d305e67a7658ba89e9349c5732305/readme_images/graph.png)

* * *

### Dependencies:
Before running any of the above commands, run
`pip3 install -r Requirements.txt`

This will install the required dependencies in your machine. We recommend you use virtual environment to isolate the working env.

Create a virtual environement run:
`virtualenv -p python3 <chosen_env_name_goes_here>`

*Note: This repository is a part of the CS540 Advanced Techniques in Software Engineering course imparted by Dr. Mark Grechanik at the University of Illinois at Chicago.*

* * *

### Developers:
* Debojit Kaushik
    * E-mail: dkaush4@uic.edu
    * [Github](https://www.github.com/dkaushik94)
* Sandeep Joshi
    * E-Mail: sjoshi37@uic.edu
    * [Github](https://www.github.com/sandeepjoshi1910)