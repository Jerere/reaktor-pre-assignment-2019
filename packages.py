import re
import time

filepath_a = "/var/lib/dpkg/status"
filepath_b = "status.real"

# patterns to find
regex_dict = {
    'name': re.compile(r'^Package:\s'),
    'desc': re.compile(r'^Description:\s'),
    'depends': re.compile(r'^Depends:\s'),
    'wspace': re.compile(r'^\s* ')
}

packageList = []

# check if pattern exists
def parseLine(line):
    for key, rx in regex_dict.items():
        match = rx.search(line)
        if match:
            return key, match

    return None, None


# read lines and add to dict
def readLines(lines):
    package_dict = {}
    for a in lines:
        a = a.rstrip()
        key, match = parseLine(a)
        if key != None and key != 'wspace':
            a = a.replace(match.group(), '')
            package_dict.update({key : a})
        elif key == 'wspace' and 'desc' in package_dict:
            b = package_dict['desc'] + "\n" + a
            package_dict.update({'desc' : b})

    return package_dict


# cut version numbers from dependencies to list and delete duplicates
def cleanDependsToList(a):
    for i in a:
        if 'depends' in i:
            clean = re.sub(r'\s\([^)]*\)', '', i['depends'])
            clean = clean.replace(' ', '')
            clean = re.split(r',|\|',clean)
            i.update({'depends' : list(dict.fromkeys(clean))})


# read lines
def parseFile(filepath):
    with open(filepath, "r", encoding="utf8") as file_object:
        line = str(file_object.readline())
        currentLines = []

        while line:
            currentLines.append(line)
            if line == '\n':
                packageList.append(readLines(currentLines))
                currentLines.clear()
            line = str(file_object.readline())


def getInverses(currentPackage, a):
    b = []
    for i in a:
        if 'depends' in i:
            if currentPackage['name'] in i['depends']:
                b.append(i['name'])
    if b:
        currentPackage.update({'invDepends' : b})

# get inverse dependencies
def inverseDependencies(a):
    for currentPackage in a:
        getInverses(currentPackage, a)

# return names
def getNames(a):
    names = []
    for i in a:
        names.append(i['name'])

    return sorted(names)

# return packages
def getPackage(a, name):
    for i in a:
        if name == i['name']:
            return i


def main():
    parseFile(filepath_b)
    cleanDependsToList(packageList)
    inverseDependencies(packageList)

    return packageList

if __name__ == '__main__':
    main()
