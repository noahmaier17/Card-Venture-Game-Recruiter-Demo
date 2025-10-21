import os

from send2trash import send2trash


def code():
    directory_path = "Logs/"

    ## Gets all the files
    files = []
    for entry in os.listdir(directory_path):
        full_path = os.path.join(directory_path, entry)
        if os.path.isfile(full_path):
            files.append(directory_path + entry)
    print(files)

    ## Sends them to the trash
    send2trash(files)

if __name__ == '__main__':
    code()