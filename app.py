import requests
import json
import re
from prettytable import PrettyTable
import numpy as np

# main url for retrieval
url = "http://oscars.yipitdata.com/"

# headers to bypass security filters:
headers={'User-Agent': 'Mozilla/5.0'}

# containers for main and secondary parse 
detail_urls = []
details = []
years = []
dirty_data = {}
used_keys = []
final_budget = []

def retrieve_data():
    """ Fetch Data from main page and return for parsing """
    response = requests.get(url,headers=headers)
    jsony = json.loads(response.content)
    return jsony

def main_parse():
    """ Parses retrieved data for year and detail url """
    data = retrieve_data()
    length = len(data['results'])
    for i in range(0,length):
        years.append(int(data['results'][i]['year'].strip(" ")[0:4]))
        for k in data['results'][i]['films']:
            if k.get("Winner") == True:
                detail_url = k.get("Detail URL")
                detail_urls.append(detail_url)

def secondary_retrieve():
    """ Retrieve movie details from crawled link and makes data accessible """
    for i in detail_urls:
        response = requests.get(i,headers= headers)
        jsony = json.loads(response.content)
        details.append(jsony)

def secondary_parse():
    """ Parses json for title and budget, returning title and budget accessible by year """
    for i in range(len(details)):
        title = details[i].get("Title")
        budget = details[i].get("Budget")
        year = years[i]
        dirty_data[year] = [title,budget]

def normalize_budget():
    """ Function parses data for abnormalities in budget values """
    clean_nums = [] 
    for key,value in dirty_data.items():
        if value[1]: 
            # filter and reformat edge case values
            if  "-" in value[1]:
                result = re.search(r'16.5-18',value[1])
                nums = result.group(0)
                clean_nums.append({key:"".join(nums)})
            elif value[1][0:3] == "US$":
                num = value[1][2:]
            # filter and reformate bulk values
            elif "$" and "million" in value[1]:
                result1 = re.findall(r'\$\d.\d', value[1])
                result2 = re.findall(r'\$[0-9][0-9]', value[1])
                if result1:
                    num1 = result1[0]
                    used_keys.append(key) 
                    clean_nums.append({key: num1})
                if result2:
                    num2= result2[0]
                    used_keys.append(key)
                    clean_nums.append({key:num2})
            elif "$" in value[1]:
                num = value[1].split(" ")
                clean_num = "".join(num[0])
                if clean_num[0:2]=="US":
                    clean_num = clean_num[2:]
                    used_keys.append(key)
                    clean_nums.append({key: clean_num}) 
                else:
                    clean_num = "".join(clean_num[1:].split(","))
                    normalized_num = "${}".format(round(float(clean_num)/100000,2)) 
                    used_keys.append(key)
                    clean_nums.append({key:normalized_num})
    return(clean_nums)

def display_data():
    """ A function to print out each Year-Title-Budget combination"""
    data = normalize_budget()
    table = PrettyTable()
    table.field_names = ['Year', 'Title','Budget']
    for i in range(len(details)):
        try:
            title = details[i].get("Title")
            year = used_keys[i]
            budget = data[i][year]
            final_budget.append(data[i][year])
            table.add_row([year,title, budget])    
        except:
            budget = 0
    print(table)
    
def find_mean():
    """ print the average budget of all the winners at the end """
    clean_nums = []
    for i in final_budget:
        try:
            if i[0] == "$":
                i = float(i[1:])
                clean_nums.append(i)
            elif "-" in i[0]:
                result = re.search(r'6-7',i)
                num = result.group(0)
        except:
            error = ("error value", i)
    print("The average budget of all parse winners: {} million".format(round(np.mean(clean_nums),2)))
               
### Calls to the functions ### 
retrieve_data()
main_parse()
secondary_retrieve()
secondary_parse()
normalize_budget()
display_data()
find_mean()

"""
    Summary: 

    This was a very "puzzling" exeperience, really testing attention to detail and programming mechanics.
    I chose to take a functional approach and keep things as simple as possible. As I  noticed "boobie traps" as I got deeper into the exercise
    making the assignment more complex(encodings, spaces,chars etc.), but enjoyable to try to find solutions. 
    PrettyTable seemed like the fastest & appropriate way to return the requested information.
    Overall, I recieved a refresher course in python regex and look forward to using it more to deepend my parsing capacity.
    If I were to do it again I would most likely use pandas to make the data structuring slightly easier.

    Notes:
    - Written in python version 3.6.4
    - Please pip install prettytable (latest) and numpy(latest), to properly recieve output
    - To run file execute python app.py
    - Assumptions I have to make involve: best way to encode/decode, right conversion rates?, exclude pounds?, "6-7" may not be a dashes?
    - Ignored some values that were hard to tell whether mm, thousands or lower
    - My conversions and normilaztions are off, but for completion purposes I built everything out, 
    sacrifing accuracy for complete requirements and a working draft
    - Given more times I would:
        1. Structure code base OOP to modularize it
        2. Refactor normalize_budget, reduce nested if's to speed up the program
        3. Discover more dynamic ways to parse strings inorder to get a  more accurate statistics

"""
