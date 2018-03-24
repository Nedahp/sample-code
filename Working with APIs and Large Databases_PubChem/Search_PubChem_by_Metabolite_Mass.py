
# read the excel file containing the list of mass measurements
# input: a file name
# output: list of mass measurements
def readFile(fileName):
    import pandas as pd
    from pandas import Series, DataFrame
    data = pd.read_excel(fileName)
    mass_list = data['masses']
    return mass_list


# find the range of mass you want to search the database for
# input: list of mass measurments, error margine(such as 10ppm)
# output: min and max of the mass range
def extract_compounds_with_matchedMasses_from_PubChem(masses,tolerence):
    matched_in_PubChem = {}
    ppm_divisor = 1000000
    for i in range(len(masses)):
        print i
        compounds = []
        mass = masses[i]
        massMargine = (mass / ppm_divisor) * tolerence
        min_mass = mass - massMargine
        max_mass = mass + massMargine
        html = make_query_to_PubChem(min_mass, max_mass)
        count = extract_count_of_mass_match_in_PubChem(html)
        matched_in_PubChem[mass] = count
    return matched_in_PubChem



# make a URL and query to PubChem
# input: range of mass we want to make a query for
# output: content of the url to PubChem
def make_query_to_PubChem(min_mass, max_mass):
    import urllib2
    main_part = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pccompound&usehistory=y&retmax=0&term='
    url = main_part + str(min_mass) + ':' + str(max_mass) + '[exactmass]'
    response = urllib2.urlopen(url)
    html = response.read()
    return html



# extract count of matches from the url content to PubChem
# input: content of a url
# output: count of matches in a mass range from PunChem
def extract_count_of_mass_match_in_PubChem(html):
    idx1 = html.find('<Count>')
    idx2 = html.find('</Count>')
    count = html[idx1+7 : idx2]
    return int(count)



# main function
def mainFunction(massFile_Name,tolerence):
    # read the mass measurements
    masses = readFile(massFile_Name)
    # for each product mass find number of compounds in PubChem within the mass range
    matched_in_PubChem_by_mass = extract_compounds_with_matchedMasses_from_PubChem(masses,tolerence)
    return matched_in_PubChem_by_mass 



# run the code and save the results
import csv
result = mainFunction('list_of_masses.xlsx',10)
with open('matches_in_PubChem_by_mass.csv', 'wb') as output:
    writer = csv.writer(output)
    for key, value in result.iteritems():
        writer.writerow([key, value])





