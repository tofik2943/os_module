import sys
import os
import shutil
import time

SEPARATOR = os.path.sep
add_dir = (lambda file_name, directory: f"{os.path.dirname(directory)}{SEPARATOR}{file_name}")


def handle_initialization():
    fake_initialization()
    try:
        path1, path2, t_path, *empty_or_exception_thrown = sys.argv
        if not (os.path.isdir(path1) and
                os.path.isdir(path2) and
                os.path.isdir(t_path)):
            raise ValueError
        return Exercise(path1, path2, t_path)
    except ValueError:
        print("3 paths haven't been delivered as argument")
        exit(1)


def fake_initialization():
    absolute_path_for_this_file = os.path.abspath(__file__)
    dir_name = os.path.dirname(absolute_path_for_this_file)
    k1 = f"{dir_name}{SEPARATOR}k1{SEPARATOR}"
    k2 = f"{dir_name}{SEPARATOR}k2{SEPARATOR}"
    t = f"{dir_name}{SEPARATOR}t{SEPARATOR}"
    return Exercise(k1, k2, t)


class Exercise:

    def __init__(self, k1, k2, t):
        self.k1 = k1
        self.k2 = k2
        self.t = t
        self.list_of_files_to_transfer = []
        self.is_Sorted = False
        self.list_of_symlinks_to_repair = []

        self.list_of_folders_to_traverse = []
        self.list_of_folders_to_traverse.append(self.t)

        self.dict_of_traversed_folders = {}

    def load_files_to_transfer(self):
        self.list_of_files_to_transfer = os.listdir(self.k1)
        temp_list = []
        for file in self.list_of_files_to_transfer:
            temp_list.append(add_dir(file, directory=self.k1))
        self.list_of_files_to_transfer = temp_list

    def accept_regular_files_with_write_access(self):
        list_wanted_files = []
        for file in self.list_of_files_to_transfer:
            if os.access(file, os.W_OK) and os.path.isfile(file) and not os.path.islink(file):
                list_wanted_files.append(file)
        self.list_of_files_to_transfer = list_wanted_files
        self.is_Sorted = True

    def create_copies_in_k2(self):
        if not self.is_Sorted:
            raise Exception
        for file_path in self.list_of_files_to_transfer:
            src = file_path
            dst = f"{self.k2}{os.path.basename(file_path)}"
            print(
                f"#######################################################################################################\n"
                f"copy(src,dst)\n"
                f"src:\t{src}\n"
                f"dst:\t{dst}\n"
                f"#######################################################################################################\n")
            shutil.copyfile(src, dst)

    def load_symlinks_from_k1(self):
        self.list_of_symlinks_to_repair = []
        self.list_of_symlinks_to_repair = [add_dir(symlink, directory=self.k1)
                                           for symlink in os.listdir(self.k1)
                                           if os.path.islink(add_dir(symlink, directory=self.k1))
                                           and os.readlink(add_dir(symlink, directory=self.k1))[0] == "."]

    def delete_old_symlinks_create_updated_symlinks_pointing_at_directory(self):
        for symlink in self.list_of_symlinks_to_repair:
            symlink_dir = f"{os.path.dirname(symlink)}{SEPARATOR}"
            symlink_target = os.readlink(symlink)

            symlink_target_real_path = os.path.realpath(f"{symlink_dir}{symlink_target}")
            symlink_src = symlink_target_real_path
            symlink_dst = symlink
            if os.path.isdir(symlink_src):
                os.remove(symlink)
                os.symlink(symlink_src, symlink_dst)
                print(f"os.symlink(symlink_src, symlink_dst))\n"
                      f"symlink_src:\t{symlink_src}\n"
                      f"symlink_dst:\t{symlink_dst}\n"
                      f"#######################################################################################################")

    def traverse(self):
        while len(self.list_of_folders_to_traverse) != 0:
            unchecked = self.list_of_folders_to_traverse.pop()
            if os.path.isdir(unchecked):
                sons = list(os.listdir(unchecked))
                for son in sons:
                    son = add_dir(son, unchecked) + SEPARATOR
                    if os.path.isdir(son):
                        self.list_of_folders_to_traverse.append(son)
                self.dict_of_traversed_folders[unchecked] = len(sons)

    def print_folders_created_after_5min_with_at_most_3_subfolders(self):
        list_appropriate_folders = list(folder
                                        for folder in self.dict_of_traversed_folders
                                        if self.dict_of_traversed_folders[folder] <= 3
                                        if time.time() - os.stat(folder).st_ctime > 300)

        print('#######################################################################################################')
        for counter in range(0, len(list_appropriate_folders)):
            print(f"{counter + 1}.\tsubfolders:\t{self.dict_of_traversed_folders[list_appropriate_folders[counter]]}"
                  f"\tCreated {int((time.time() - os.stat(list_appropriate_folders[counter]).st_ctime) / 60)} minutes ago"
                  f" path:\t{list_appropriate_folders[counter]}")
        print('#######################################################################################################')


if __name__ == '__main__':
    exercise = fake_initialization()  # handle_initialization()
    # transfer_paths_to_full_path

    # zad.1
    exercise.load_files_to_transfer()
    exercise.accept_regular_files_with_write_access()
    exercise.create_copies_in_k2()

    # zad.2
    exercise.load_symlinks_from_k1()
    exercise.delete_old_symlinks_create_updated_symlinks_pointing_at_directory()

    # zad.3
    exercise.traverse()
    exercise.print_folders_created_after_5min_with_at_most_3_subfolders()
