import os
import sys

def edit_file():
    validate_arguments()
    
    args = sys.argv[1]
    input_file_path = sys.argv[2]
    output_file_path = sys.argv[3]
    
    with open(input_file_path) as f:
        contents = f.read()
    
    if args == 'reverse':
        with open(output_file_path, 'w') as f:
            f.write(contents[::-1])
    elif args == 'copy':
        with open(output_file_path, 'w') as f:
            f.write(contents)
    elif args == 'duplicate-contents':
        with open(input_file_path, 'w') as f:
            f.write(contents * int(sys.argv[3]))
            
    elif args == 'replace-string':
        with open(input_file_path, 'w') as f:
            f.write(contents.replace(sys.argv[3], sys.argv[4]))

def validate_arguments():
    try:
        assert sys.argv[1] in ['reverse', 'copy', 'duplicate-contents', 'replace-string']
        
        if sys.argv[1] == 'reverse' or sys.argv[1] == 'copy':
            assert len(sys.argv) == 4
            assert os.path.exists(sys.argv[2])
        elif sys.argv[1] == 'duplicate-contents':
            assert len(sys.argv) == 4
            assert os.path.exists(sys.argv[2])
            assert sys.argv[3].isdigit()
        elif sys.argv[1] == 'replace-string':
            assert len(sys.argv) == 5
            assert os.path.exists(sys.argv[2])
            
    except AssertionError:
        print('Invalid arguments')
        sys.exit(1)
        
if __name__ == "__main__":
    edit_file()
