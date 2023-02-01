from replacer import modify_code


def write_to_file(code, filename):
    try:
        with open(filename, 'w') as f:
            f.write(code)
    except Exception as e:
        print(f"Error writing code to file: {e}")


def execute_code(filename):
    user_ns = {}
    try:
        with open(filename, "r") as file:
            code = file.read()
        exec(compile(code, "<string>", "exec"), user_ns, user_ns)
    except Exception as e:
        print(f"Error executing code: {e}")


def main():
    filename = "codes/strategy.py"
    subfiles = ("config.py", "handles/tick.py", "utils.py", "calc.py")
    with open(filename, "r") as file:
        code = file.read()
    code = modify_code(code, "codes", subfiles)
    write_to_file(code, filename)
    execute_code(filename)


if __name__ == '__main__':
    main()
