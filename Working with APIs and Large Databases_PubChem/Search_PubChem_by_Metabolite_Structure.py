
# generate the address to the molfile of a molecule
# input: specification of potential metabolites, index of the metabolite of interest
# output: local address to the molfile of metabolite of interest
def adress_to_product_molFile(data, index):
    # generate the address to product's mol file
    path_to_product_MolFile_folder = '/Users/Neda/Desktop/Operators_Project/Prof_Lee_project/project2/Code_main/gut'
    parentMetkeggID = data['parentMetkeggID'][index]
    parentMetkeggID = str(parentMetkeggID)
    productID = data['productID'][index]
    productID = str(productID)
    local_path_to_molFile = '/' + parentMetkeggID +'/product_' + productID + '.mol'
    global_path_to_molFile= path_to_product_MolFile_folder + local_path_to_molFile
    return global_path_to_molFile


# convert a molfile to a smiles file using OpenBable
# input: a molfile
# output: a smiles file
def convert_mol_to_smiles(path_to_molFile):
    # conver mol file to smiles using opaenBable
    import string 
    import os
    input_file = path_to_molFile
    output_file = string.replace(input_file,'mol','smiles')
    os.system('babel -h -i mol '+ path_to_molFile + ' -o smi ' + output_file)
    return output_file


# open and read content of a file
# input: local address to a file
# output: content of a file
def readFile(fileAddress):
    # read the smiles file
    f = open(fileAddress,'r')
    product_smiles = f.read().rstrip()
    return product_smiles


# search PubChem using a smiles file
# input: a smiles file
# output: all metabolite IDs that their structure matches to the input smiles file
def search_by_SMILES(smiles):
    # install pubchempy first and then import it to python as pcp
    import pubchempy as pcp
    # search the data base
    CIDs = []
    try:
        results = pcp.get_compounds(smiles, 'smiles')
        for result in results: 
            CIDs.append(result.cid)
    except:
        print 'serverError'
    return CIDs


# main function
# read a list of smiles files and search PubChem based on the smiles structures
def main_function(massFile_Name):
    import pandas as pd
    from pandas import Series, DataFrame
    matches = {}
    data = pd.read_excel(massFile_Name)
    for i in range(len(data)):
        print i
        path_to_molFile = adress_to_product_molFile(data, i)
        path_to_smilesFile = convert_mol_to_smiles(path_to_molFile)
        product_smiles = readFile(path_to_smilesFile)
        CIDs = search_by_SMILES(product_smiles)
        matches.update({i:CIDs})
    return matches



# run the code and save the results
massFile_Name = 'list_of_potential_metabolites.xlsx'
matches_in_PubChem_by_smiles = main_function(massFile_Name)
# write the results to a file
import csv
with open('matches_in_PubChem_by_smiles.csv', 'wb') as output:
    writer = csv.writer(output)
    for key, value in matches_in_PubChem_by_smiles.iteritems():
        writer.writerow([key, value])

