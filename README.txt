Requirements:
Python, Pip and Selenium needs to be installed in the computer

Python Installation on Windows 10: https://www.journaldev.com/30076/install-python-windows-10 (Programmin Language)
Pip Installation With Python: https://phoenixnap.com/kb/install-pip-windows		      (Python Library)
How to Install Selenium with Pip: https://pypi.org/project/selenium/                          (One of the libraries, the bot)


1) Execute run application under dist directory

2) wait for the bot to do the work (it should take between 2-3 hours)

3) the spreadsheets will be under the dist/spreadsheets directory once the program is done running

4) add all the data in the usssa_coaches spreadsheet to the coaches spreadsheet

5) put the spreadsheets: spreadsheet1, spreadsheet2, coaches, directors all in one single file

6) Delete Duplicated Data for spreadsheet1 and spreadsheet2 

How to: https://support.microsoft.com/en-us/office/filter-for-unique-values-or-remove-duplicate-values-ccf664b0-81d6-449b-bbe1-8daaec1e83c2

**Select all the columns, clice remove duplicate values, unselect "GAME/TOURNAMENT ID"**

You might need help with this, hit me up if anything.

6) Include this formulas in spreadsheet1 under Coach Name:

for coach name in spreadsheet 1
=IFERROR(VLOOKUP(D3,Coaches!$A$2:$G$779,7,0),"")

=VLOOKUP(D3,Coaches!$A$2:$K$779,11,0) and apply it for all the ones below (just double click in the right bottom corner of the cell, or google
"how to apply the same formula to all rows in the same column").

7) Include this formulas in spreadsheet1 under Coach Name:

=VLOOKUP(D3,Coaches!$A$2:$K$779,11,0) and apply it for all the ones below (just double click in the right bottom corner of the cell, or google
"how to apply the same formula to all rows in the same column").

8) Include this formulas in spreadsheet2 under Coach Name:

=VLOOKUP(B2,Coaches!$A$2:$K$779,11,0) and apply it for all the ones below (just double click in the right bottom corner of the cell, or google
"how to apply the same formula to all rows in the same column").

9) Make sure you delete Spreadsheet1 and Spreadsheet2 once you copy/cut them to your computer before you run the program again..otherwise it will try to
overrite those files and the program will fail.