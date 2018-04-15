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


* * *

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

![if_pattern_analysis](https://bitbucket.org/sjoshi37/sandeep_joshi_debojit_kaushik_hw2/raw/cfc83ef6ee77a265f44c813a88af7daa937432c7/readme_images/id_checker.png)


## Change Analysis

`change_analyzer` takes into context what is the current keyword of the line. After doing this it extract respective properties from the line and stores it into a hashmap to construct the extracted sugar. 

For example:
>*if/elif* are the keywords,clauses following these are the new conditions that are >being written in the patch file. 

>*for* is the keyword,
>   value from this is the varialbe following for, and after 'in' is the range of the loop that has been introduced.
    
And so on, this method analyses over predefined keywords.

## Frequency Analysis

`frequency_analyzer` is a naive method which analyses over many patch files (preferably thousands) to extract highest used syntax keywords in patches. It does this by detecting keywords, and storing how manuy time that keyword was introduced or removed.

* * *

# Limitations

- If analysis module is naive. For example, an if statement like this - `if x > 10 and y != 34`, the part `10 and y != 34` is considered as RHS. So a specific change like `y == 34` will be considered as a change in the entire RHS. This affects the insight otherwise we would've been able to obtain. Also we are comparing each addition line with each removal line. This might not reflect the actual scenario. But we're doing this as we're unsure of which additon corresponds to which deletion. This is the reason you might see a high number in the frequency of the last case listed above. 

- In finding patterns either in `if` or  `while` and `for` turned out harder than we imagined. Regex helps us to find patterns in the code but we couldn't use regex to find recursive pattens in code which made us to adapt our code to build a naive soultion. Patterns line `if (num_products > 10 and y < x.get_productId()) or (inventory_size < 4578 and lost_inventory > 2347):` are very hard to detect using regex. Also, once we even find these patterns, the possible combinations are exhaustive.

- In the If analysis module, sometimes there are just not enough data to find patterns in the patch files. We paginated around 15 pages of pull requests to get enough data. Some repositories doesn't have data specific to the if analysis pattern.

- Since we're performing complex string operations, the code can run slowly at times. The code sometimes runs with complexity in the order of O(n^4). When we have huge data (around 2.5 GB of patch files), we have noticed considerable amount of time being taken to analyze the patch files.

- CodeAnalysis class methods dont take into account the context of the code. Whether the same line was modified or the current line is a new line. This reduces the value of the analysis of the reports. It would be great if some correlation coudl be found which would give us a deeper insight into the patch fixes and what they tend to do.

* * *

### Developers:

* Debojit Kaushik
    * E-mail: dkaush4@uic.edu
    * [Github](https://www.github.com/dkaushik94)
* Sandeep Joshi
    * E-Mail: sjoshi37@uic.edu
    * [Github](https://www.github.com/sandeepjoshi1910) 

*Note: This repository is a part of the CS540 Advanced Techniques in Software Engineering course imparted by Dr. Mark Grechanik at the University of Illinois at Chicago.*

# References

- Github REST API & documentation
- StackOverflow posts alot of it
- Python Documentation
- Regex101.com
- JSONPretty Print to better see large JSON objects
- PyGal
- PyPI
- .*
