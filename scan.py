import os


# get all ".git" directories under dir_name, ignore "vendor" and "node_modules"
def get_git_dir(dir_name):
    list_of_dir = os.listdir(dir_name)
    ignore_dir = ["vender", "node_module"]
    all_dir = list()
    try:
        for entry in list_of_dir:
            full_path = os.path.join(dir_name, entry)
            if os.path.isdir(full_path):
                if full_path in ignore_dir:
                    continue
                if full_path.endswith(".git"):
                    all_dir.append(full_path)
                all_dir = all_dir + get_git_dir(full_path)
    except:
        pass

    return all_dir
