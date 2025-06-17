from functions.run_python import run_python_file

def test():

    print("Testing running calculator main.py")
    print(run_python_file("calculator", "main.py"))
    print("")

    print("Testing running calculator tests.py")
    print(run_python_file("calculator", "tests.py"))
    print("")

    print("Test running file outside of permitted working directory")
    print(run_python_file("calculator", "../main.py"))
    print("")

    print("Testing running calculator nonexistent.py")
    print(run_python_file("calculator", "nonexistent.py"))
    print("")
    

if __name__ == "__main__":
    test()
