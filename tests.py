from functions.get_files_info import get_files_info
from functions.test_get_file_content import get_file_content

def main():
    working_dir = "calculator"
    print(get_file_content("calculator", "lorem.txt"))
   

main()