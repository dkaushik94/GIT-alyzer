# GIT-alyzer

##  Summary:
GIT-alyzer is a git patch analyzer which does string and syntax level parsing to analyze and generate reports for the repositories written in Python. Below is the working of parser.

To run the parsers first run:

`python3 issues.py`

This will download a number of patch files from Python respositories and save them under ***Repos/repo_name/*** directory.
After the downloads are finished, run:

`python3 analyzer.py`

This script will run mutiple analysis on a syntax-level and generate reports according to the results.
The reports are *.svg* files and can be opened with a browser or any 3rd part application of your choice.

* * *

## Diagram:

#### Control Flow Chart:
![Flow Diagram](https://bitbucket.org/sjoshi37/sandeep_joshi_debojit_kaushik_hw2/raw/0a1c895eaf61d6afe5a38d9de452eea573f50689/readme_images/analyzer_flow.svg)

#### Example output graph after Frequency analysis on 15000 patch files:
![Frequency analysis](https://bitbucket.org/sjoshi37/sandeep_joshi_debojit_kaushik_hw2/raw/7d0f5c85485d305e67a7658ba89e9349c5732305/readme_images/graph.png)

* * *

## Dependencies:
Before running any of the above commands, run:

`pip3 install -r Requirements.txt`

This will install the required dependencies in your machine. We recommend you use virtual environment to isolate the working env.
Create a virtual environement run:

`virtualenv -p python3 <chosen_env_name_goes_here>`

After the env is created, to change working source, run:

`source <virtualenv_name>/bin/activate`

This will initiate the working environment.

*Note: This repository is a part of the CS540 Advanced Techniques in Software Engineering course imparted by Dr. Mark Grechanik at the University of Illinois at Chicago.*

* * *

### Developers:

* Debojit Kaushik
    * E-mail: dkaush4@uic.edu
    * [Github](https://www.github.com/dkaushik94)
* Sandeep Joshi
    * E-Mail: sjoshi37@uic.edu
    * [Github](https://www.github.com/sandeepjoshi1910)



# How it works

## Obtaining patch files

The script takes in three inputs - 1) GitHub username 2) GitHub password 3) No of repositories to be analyzed. With this, the script starts downloading patch files for pull requests connected to issues. We are paginating a maximum of 15 pages of pull requests per repository. The downloaded patch files are stored in the directory structure.

```
  Repos/
    --repo_1/
        --patch_file1.txt
        -- patch_file2.txt
    --repo_2/
        --patch_file1.txt
        --patch_file2.txt
```

The script does basic username and password validations. Further an initial check is done to ensure there is an active internet connection on the device.


# Analysis

## If statement pattern analysis

This part of the analyzer script is used to detect pattern of change in if statements between a pair of addition and removal lines. The following steps are taken to achieve this.

- For each patch file, get all the addition and removal lines
- Check if there are more than 1 addition and removal line containing if statement
- consolidate addition and removal lines
- Comapre each pair of addition and removal line to see what pattern it fits into. One of the following 8 patterns are possible.

```
if  no_LHS_change  (operator)         no_RHS_change:
if  no_LHS_change  (operator)           changed_RHS:
if  no_LHS_change  (operator_change)  no_RHS_change:
if  no_LHS_change  (operator_change)    changed_RHS:
if    changed_LHS  (operator)         no_RHS_change:
if    changed_LHS  (operator)           changed_RHS:
if    changed_LHS  (operator_change)  no_RHS_change:
if    changed_LHS  (operator_change)    changed_RHS:
```

For each repository, the frequency of each of the pattern is accumulated and plotted into a bar chart.

![if_pattern_analysis]()


# Limitations

- If analysis module is naive. For example, an if statement like this - `if x > 10 and y != 34`, the part `10 and y != 34` is considered as RHS. So a specific change like `y == 34` will be considered as a change in the entire RHS. This affects the insight otherwise we would've been able to obtain. 

