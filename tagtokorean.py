data = {}  # create an empty dictionary to store the data

with open('tag-to-korean.txt', 'r') as file:  # replace filename.txt with the name of your file
    lines = file.readlines()  # read all the lines from the file

for line in lines:
    line = line.strip()  # remove leading/trailing whitespaces
    if line:  # skip empty lines
        key, value = line.split(',', 1)  # split the line by comma (maximum of 1 split), resulting in a list of 2 items
        data[key] = value.strip()  # add the key-value pair to the dictionary