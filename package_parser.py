import re
from os import path

# patterns to find
regex_dict = {
    'name': re.compile(r'^Package:\s'),
    'description': re.compile(r'^Description:\s'),
    'dependencies': re.compile(r'^Depends:\s'),
    'white_space': re.compile(r'^\s* ')
}

PackageList = []
FilePath_A = "/var/lib/dpkg/status"
FilePath_B = "./status.real"


# set filepath
def file_path():
    if path.exists(FilePath_A):
        return FilePath_A
    else:
        return FilePath_B


# read lines
def parse_file(filepath):
    with open(filepath, "r", encoding="utf8") as file_object:
        line = str(file_object.readline())
        current_lines = []

        while line:
            current_lines.append(line)
            if line == '\n':
                PackageList.append(read_lines(current_lines))
                current_lines.clear()
            line = str(file_object.readline())


# check if pattern exists
def parse_line(line):
    for key, rx in regex_dict.items():
        match = rx.search(line)
        if match:
            return key, match

    return None, None


# read lines and add to dict
def read_lines(lines):
    package_dict = {}
    for line in lines:
        line = line.rstrip()
        key, match = parse_line(line)
        if key is not None and key != 'white_space':
            line = line.replace(match.group(), '')
            package_dict.update({key: line})
        elif key == 'white_space' and 'description' in package_dict:
            b = str(package_dict['description'] + "\n" + line)
            package_dict.update({'description': b})

    return package_dict


# cut version numbers from dependencies to list and delete duplicates
def clean_dependencies(package_list):
    for package in package_list:
        if 'dependencies' in package:
            clean = re.sub(r'\s\([^)]*\)', '', package['dependencies'])
            clean = clean.replace(' ', '')
            clean = re.split(r',|\|', clean)
            package.update({'dependencies': list(dict.fromkeys(clean))})


def find_inverses(current_package, package_list):
    inverses = []
    for package in package_list:
        if 'dependencies' in package:
            if current_package['name'] in package['dependencies']:
                inverses.append(package['name'])
    if inverses:
        current_package.update({'inv_dependencies': inverses})


# get inverse dependencies
def inverse_dependencies(package_list):
    for current_package in package_list:
        find_inverses(current_package, package_list)


# return names
def get_names(package_list):
    names = []
    for package in package_list:
        names.append(package['name'])

    return sorted(names)


# return packages
def get_package(package_list, package_name):
    for package in package_list:
        if package_name == package['name']:
            return package


def main():
    parse_file(file_path())
    clean_dependencies(PackageList)
    inverse_dependencies(PackageList)

    return PackageList
