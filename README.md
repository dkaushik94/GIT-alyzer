# Homework 2

Your second homework assignment is to create a Git repository analyzer by automatically obtaining fixes to the source code that developers performed to address bug/issue reports for software applications. We are interested to determine patterns of code fixes in response to issues/bug reports as expressed in **patches**, which are modular code fragments that specify changes between versions of the code artifacts in a repo. These changes are often specified as instructions that are applied to the source code to implement the fix. Thus, instead of committing the code directly, a developer creates a patch and  applies/pushes it to the git repo, which takes instructions from the patch and applies it to the source code. Historically, the name patch originated from the Unix tool called *patch* that updated text files using instructions from a separate file called [a patch file](https://en.wikipedia.org/wiki/Patch_%28Unix%29). Git patches are essentially metadata files that describe how to apply changes to the source code of the previous version of the application to switch to the next consecutive version of the same application. For example, the following lines in a patch "- int a = 2" and "+ float b = 3" would mean that the declaration and initialization of the variable a in some Java file is replaced with the declaration and initalization of the variable b, hence + and - signs in the beginning of the lines. You can find more information in various sources (e.g., https://git-scm.com/docs/git-format-patch). Patches are effective because they make it easier for software developers to understand the changes to the source code at a high level and link them to specific issues/bug reports. The goal of this homework is to determine if there are "common" bugs based on the repeated patterns of patches that are applied to the source code to fix bugs.

In this homework, which you will build on the results of your previous homework, you will again use the Github Developer API to obtain open-source software projects with their metainformation. I recommend that you use **JGit** that has rich functionality and well-documented [JGit API calls](https://www.eclipse.org/jgit/), however, you can explore the toolkit/frameworks space on your own and find something that fits the task better. For each repo that you iterate through in Github (in reality, you will iterate through several repos), you will obtain patches for fixes as well as all metainformation related to these fixes, when available (e.g., the description of the issue/bug, dates and times and the content of discussions, developers ids). You will obtain existing patches or create new ones as needed by diffing consequtive versions and linking the patch to a specific commit and extracting and saving its metadata (e.g., the commit message). As a result, you will obtain a rich data set that can contain information about program entities (e.g., fields, their types, control structures, parameters of methods) that were modified as a result of fixes to specific bugs/issues.

To analyze how patches modify the source code, you can use the Application Programming Interface (API) of the tool called Understand (https://scitools.com/non-commercial-license/), a static code analysis tool that supports many programming languages and it is used by many Fortune 500 companies, an Eclipse parser, or some other open-source tools. If you haven't done so and if you choose Understand, you should apply for a non-commercial license immediately, install the tool, and investigate its IDE and its API libraries. You can complete this homework using a language of your choice, e.g., Java or Scala or Python or Go or Clojure or simply the utility curl when applicable (I prefer that you use Java for this assignment). You will use Maven or SBT or Gradle - your choice - for building the project. You can use the latest community version of *IntelliJ IDE* for this assignment.

The output of your analyzer will be a list of tuples in a format of your choice (e.g., JSON, XML) that contain frequences of changes to the source code entities based on the analyzed patches. For example, the following entry describes changing the type of a parameter of a method and its use in the if statement: 
```
<method frequency=20>m1
	<file>f.java</file>
	<change>
		<parameter oldtype="int" newtype="double">salary</parameter>
	</change>
	<change>
		<ifstatement addcondition="true">salary \gt 0</ifstatement>
	</change>
</method>
```

This part of the homework requires a lot of thinking, since it is important to choose abstract representation for software modifications that are general enough to capture patterns of changes in patch files, and yet it should be specific enough to differentiate between changes that differ from one another. Small changes like replacing the sign plus with the minus are easy to capture and generalize as arithmetic operator replacements; more complex changes that are spread across multiple files are much more difficult to generalize. A part of your grade will be determined by the algorithm that you will create for this task.

Please make sure that you were already added as a member of CS_540_2018 team in Bitbucket. Separate repositories will be created for each of your homeworks and for the course project. You will find a corresponding entry for this homework. You will fork this repository and your fork will be private, no one else besides you, your teammates and your course instructor will have access to your fork. Please remember to grant a read access to your repository to your instructor. You can commit and push your code as many times as you want. Your code will not be visible and it should not be visible to other students, except for your teammates. When you push it, your instructor will see you code in your separate private fork. Making your fork public or inviting other students to join your fork will result in losing your grade. For grading, only the latest push timed before the deadline will be considered. If you push after the deadline, your grade for the homework will be zero. For more information about using git and bitbucket specifically, please use this link as the starting point https://confluence.atlassian.com/bitbucket/bitbucket-cloud-documentation-home-221448814.html.

------

For an additional bonus (up to 10%!) you will incorporate a machine learning algorithm for capturing and generalizing patterns of changes. Your ideas and creativity are highly welcome and will be rewarded! For example, you can obtain issues for each pulled software project and you can attempt to link these issues to specific patches using keywords that correspond to specific changes (e.g., the presence of null pointer exceptions in bug reports). You can create a separate database into which you can save the attributes of the pulled repos and bug reports and generalized patterns of changes. In short, your additional bonus will be based on how you connect various sources of information, not on simply downloading bits and pieces of information. Let your imagination fly!

------

Even though this is a individual homework, it can be done collaboratively. You are allowed to form groups with up to three teammates. If you want to work alone, it is perfectly fine. Logistically, one of you will create a private fork and will invite one or two of her classmates with the write access to your fork. You should be careful - once you form a group and write and submit code, you cannot start dividing your work and claim you did most of the work. Your forkmates may turn out to be freeloaders and you will be screwed. Be very careful and make sure that you trust your classmates before forming your group. I cannot and I will not resolve your internal group conflicts. Your submission will include the names of all of your forkmates and you will receive the same grade for this homework. Working in a group will be an excellent opportunity for you to explore branching in git, merging, and resolving semantic conflicts when merging your code changes. Don't pass on this opportunity!

I allow you to post questions and replies, statements, comments, discussion, etc. on Piazza. Remember that you cannot share your code and your solutions, but you can ask and advise others using Piazza on where resources and sample programs can be found on the internet, how to resolve dependencies and configuration issues, and how to design the logic of the algorithms and the workflows. Yet, your implementation should be your own or your team's and you cannot share it with the entire class. Alternatively, you cannot copy and paste someone else's implementation and put your name on it. Your submissions will be checked for plagiarism. When posting question and answers on Piazza, please select the appropriate folder, i.e., hw2 to ensure that all discussion threads can be easily located.

------

Submission deadline: Saturday, April 7 at 7PM CST. Your submission will include your source code, detailed documentation on all aspects of the installation and configuration of your solution, one or more of the SBT/Gradle/Maven build configurations, the README.md file in the root directory that contains the description of your implementation, how to compile and run it using your chosen build tool(s), and what are the limitations of your implementation. Please follow this naming convention while submitting your work : "Firstname_Lastname_hw2", so that we can easily recognize your submission. Those who work in groups can use longer names: "Firstname1_Lastname1_Firstname2_Lastname2_Firstname3_Lastname3_hw2". I repeat, please make sure that you will give me read access to your private forked repository.

------
THE INSTRUCTOR WILL NOT ANSWER ANY REQUESTS FROM STUDENTS STARTING 7PM THE NIGHT BEFORE THE SUBMISSION DEADLINE.
------

Evaluation criteria:
* the maximum grade for this homework is 25%. Points are subtracted from this maximum grade: for example, saying that 2% is lost if some requirement is not completed means that the resulting grade will be 25%-2% => 23%;

* no comments or insufficient comments: up to 20% lost;

* no unit and integration tests: up to 20% lost;

* code does not compile or it crashes without completing the core functionality: up to 25% lost;

* the documentation is missing or insufficient to understand how to compile and run your program: up to 20% lost;

* only a subset of your functionality works: up to 20% lost;

* the minimum grade for this homework cannot be less than zero.
