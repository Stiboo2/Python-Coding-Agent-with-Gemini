from functions.get_files_info import get_files_info
from functions.write_file import write_file

def main():
    working_dir = "calculator"

    #print(write_file(working_dir, "lorem.txt", "wait, this isn't lorem ips"))
    #print(write_file(working_dir, "pkg/morelorem.txt", "lorem ipsum dolor"))
    
    
    print(write_file(working_dir, "/tmp/temp.txt", "this should not be all"))

main()