from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python import run_python_file


info_test_cases = [
    ["calculator", "."],
    ["calculator", "pkg"],
    ["calculator", "/bin"],
    ["calculator", "../"]
]

content_test_cases = [
    ["calculator", "main.py"],
    ["calculator", "pkg/calculator.py"],
    ["calculator", "/bin/cat"],
    ["calculator", "pkg/does_not_exist.py"]
]

write_test_cases = [
    ["calculator", "lorem.txt", "wait, this isn't lorem ipsum"],
    ["calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"],
    ["calculator", "/tmp/tmp.txt", "this should not be allowed"],
]

run_test_cases = [
    ["calculator", "main.py"],
    ["calculator", "main.py", ["3 + 5"]],
    ["calculator", "tests.py"],
    ["calculator", "../main.py"],
    ["calculator", "nonexistent.py"],
]

#for case in info_test_cases:
#    try:
#        result_list = get_files_info(case[0], case[1])
#        output_string = f"Result for {case[1]} directory:\n"
#        output_string += "\n".join(result_list)
#        print(output_string)
#    except Exception as e:
#        print(f"{e}");    

#for case in content_test_cases:
#    try:
#        print(get_file_content(case[0], case[1]))
#    except Exception as e:
#        print(f"{e}")    

#for case in write_test_cases:
#    try:
#        print(write_file(case[0], case[1], case[2]))
#    except Exception as e:
#        print(F"{e}")    

for case in run_test_cases:
    try:
        if len(case) == 2:
            print(run_python_file(case[0], case[1]))
        else:
            print(run_python_file(case[0], case[1], case[2]))    
    except Exception as e:
        print(F"{e}")    