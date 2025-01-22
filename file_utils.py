import csv
import os
import shutil
import glob
from msg_utils import Msg

class PathUtils:
    @staticmethod
    def get_curr_path():
        return os.getcwd()

    @staticmethod
    def extract_all_files_with(prefix, suffix, justStem=True):
        listOfFiles = []
        if justStem:
            for file in glob.glob(prefix+"*"+suffix):
                listOfFiles.append(file[len(prefix):-len(suffix)])
        else:
            for file in glob.glob(prefix+"*"+suffix):
                listOfFiles.append(file)

        return listOfFiles


class FileUtils:
    @staticmethod
    def copy_from_to(src_dir_path, dest_dir_path):
        shutil.copy2(src_dir_path, dest_dir_path)

    @staticmethod
    def rename_from_to(src_dir_path, dest_dir_path):
        shutil.copy2(src_dir_path, dest_dir_path)

    @staticmethod
    def pull_full_filename(file_path):
        file_path = Path(file_path)
        return file_path.name

    @staticmethod
    def pull_filename_nosuffix(file_path):
        file_path = Path(file_path)
        ## if you want to pull the suffix just use file_path.suffix
        return file_path.stem

    @staticmethod
    def create_dir(dir_path):
        if os.path.exists(dir_path):
            return
        if os.path.isdir(dir_path):
            return
        os.mkdir(dir_path)

    @staticmethod
    def create_file(out_file_path):
        FileUtils.create_dir(os.path.dirname(out_file_path))
        file = open(out_file_path, 'wb')
        file.close()

    @staticmethod
    def write_content_to_file(out_file_path, file_contents_as_list):
        with open(out_file_path, "w") as file:
            for line in file_contents_as_list:
                file.write(line)

    @staticmethod
    def write_row_to_file(out_file_path, row_data):
        """
        Writes a new row into the given file
        :param out_file_path: name of the file that is to be written in
        :param row_data: the entire row entry that is to be written into the file
        :return: None
        """
        if not os.path.isfile(out_file_path):
            FileUtils.create_file(out_file_path)

        try:
            file = open(out_file_path, 'a')
            writer = csv.writer(file)
            writer.writerow(row_data)
            file.close()

        except Exception as e:
            Msg.print_error("ERROR [write_row_to_file]: could not write into " + out_file_path)
            Msg.print_error(str(e))
            assert False

    @staticmethod
    def read_csv_file(file_path, delimiter=","):
        """
        Reads and returns the data within the given file,
        or returns with an error message if no such file exists
        :param file_path    : name of the file that is to be read
        :param delimiter    : the type of the delimiter
        :return: a list of list containing all the data
        """

        try:
            file = open(file_path, 'r')
            reader = csv.reader(file, delimiter=delimiter)

            data = []
            for row in reader:
                data.append(row)
            file.close()

            return data

        except Exception:
            Msg.print_error("Error while reading from " + file_path)
            raise FileNotFoundError

    @staticmethod
    def check_is_file(file_path):
        return os.path.isfile(file_path)

    @staticmethod
    def get_dir_list_in_directory(dir_path):
        try:
            return list(filter(os.path.isdir, [os.path.join(dir_path, i) for i in os.listdir(dir_path)]))
        except Exception as e:
            Msg.print_error("ERROR: issue in retrieving directory list within given directory " + dir_path)
            Msg.print_error(str(e))

    @staticmethod
    def get_files_in_directory(dir_path, is_sorted=False):
        try:
            if not is_sorted:
                return list(filter(os.path.isfile, [os.path.join(dir_path, i) for i in os.listdir(dir_path)]))
            return sorted(list(filter(os.path.isfile, [os.path.join(dir_path, i) for i in os.listdir(dir_path)])))
        except Exception as e:
            Msg.print_error("ERROR: issue in retrieving files within directory " + dir_path)
            Msg.print_error(str(e))




if __name__ == '__main__':
    pass
