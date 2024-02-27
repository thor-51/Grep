#Equivalent Grep command in Python

import re #For regular expressions
import os #For operating system related functions
from colorama import Style, Fore #For coloring output

def grep(p, fp, case_sensitive=True, pwp=True, before=0, after=0, recursive=False, exclude=None): #Function with parameters
    '''
    "p" - regex pattern to search
    "fp" - list of file paths to search
    "case_sensitive" - flag indicating whether the search should be case-sensitive
    "pwp" - flag indicating whether to print lines with the matching pattern
    "before" - number of lines to print before the matching line
    "after" - number of lines to print after the matching line
    "recursive" - flag indicating whether to search recursively through directories
    "exclude" - regex pattern to exclude files from search
    ''' 
    ep = re.compile(exclude) if exclude else None #Compiles the 'exclude' pattern into a regex object

    for file_path in fp: #Iterates over each file path in the fp list
        if os.path.isdir(file_path): #Checls if the file path is a directory
            if recursive: #Set to true
                sub_files = [os.path.join(file_path, f) for f in os.listdir(file_path)] #Creates a list of file paths in the directory 'file_path'
                grep(p, sub_files, case_sensitive=case_sensitive, pwp=pwp, before=before, after=after, recursive=True, exclude=exclude)
                #Recursive call of grep function with the sub_files list and the same parameters, except recursive is set to True
            else:
                print(f"grep: {file_path}: Is a directory")
            continue

        if ep and ep.match(file_path): #Checks if ep is not None and if the file_path matches the ep. If it matches, the file is excluded from the search
            continue

        if not os.path.isfile(file_path):
            print(f"grep: {file_path}: No such file or directory")
            continue

        match_count = 0 #Count number of lines that match the pattern in the file
        with open(file_path, 'r') as file: #Opens file for reading
            lines = file.readlines() #Reads all lines 
            for line_number, line in enumerate(lines, start=1): #Iterates over each line keeping track of the line number
                search_p = re.compile(p, re.IGNORECASE if not case_sensitive else 0) #Compiles p into a regular expression object with re.IGNORECASE for case-sensitive matches
                if search_p.search(line):
                    match_count += 1 #Increment the count of lines by 1 
                    start = max(line_number - before, 1) #Calculates the start line number to print based on the before parameter
                    end = min(line_number + after + 1, len(lines) + 1) #Calculates the end line number to print based on the after parameter
                    for i in range(start, end):
                        if pwp:
                            colored_line = search_p.sub(f"{Fore.RED}\\g<0>{Style.RESET_ALL}", lines[i - 1].strip()) #Adding color to the matched pattern using colorama
                            print(f"{file_path}:{i}: {colored_line}") #Print the file path, line number, and colored line
                        elif not pwp:
                            print(f"{file_path}:{i}: {lines[i - 1].strip()}")
                    print()

        print(f"Number of lines matching the pattern in {file_path}: {match_count}") #Print the total number of lines that matched the pattern  

#INPUT based on the user's choice
p = input("Enter the pattern to search: ")
fp = input("Enter the file paths (with a space in between): ").split()
pwp = input("Print lines with pattern -> Y or N: ").upper() == 'Y'
case_sensitive = input("Case sensitive search -> Y or N: ").upper() == 'Y'
before = int(input("Enter the context lines to print before the pattern matching line: "))
after = int(input("Enter the context lines to print after the pattern matching line: "))
recursive = input("Search recursively through directories -> Y or N: ").upper() == 'Y'
exclude = input("Provide a regular expression to exclude the file path matching the regex (or None): ") or None

#Calling of grep function with the given inputs to perform the search
grep(p, fp, case_sensitive=case_sensitive, pwp=pwp, before=before, after=after, recursive=recursive, exclude=exclude)