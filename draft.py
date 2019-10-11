import os


def get_names_set(file_dir):
    l_fname = set()
    for root, dirs, files in os.walk(file_dir):
        for name in files:
            l_fname.add(name.rsplit('-', 1)[0])
    return l_fname


s_names = get_names_set(r"D:\id")

print(len(s_names))  
