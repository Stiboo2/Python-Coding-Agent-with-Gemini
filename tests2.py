from functions.get_files_info import get_files_info
from functions.test_get_file_content import get_file_content

def main():
    working_dir = "calculator"
    print(get_files_info("calculator", "."))
    print(get_files_info(working_dir))
    print(get_files_info("calculator", "pkg"))
    print(get_files_info("calculator", "/bin"))
    print(get_files_info("calculator", "../"))

main()