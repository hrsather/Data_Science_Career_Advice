def get_quals(file_name):
    qual_list = []
    with open(file_name) as tech_file:
        qual_list = tech_file.read().splitlines()
    return qual_list