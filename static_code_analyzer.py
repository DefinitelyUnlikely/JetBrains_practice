import sys
import re
import os
import ast
from natsort import natsorted


def code_analyzer(path_to_analyze):
    found_errors = []

    class Analyzer(ast.NodeVisitor):

        def visit_arg(self, node):
            return node.arg, node.lineno

        def visit_FunctionDef(self, node):
            return node.name, node.lineno

        def visit_Name(self, node):
            return node.id, node.lineno

    def check_length(text):
        return len(text) > 79

    def check_indentation(text):
        if text.startswith(" "):
            if len(re.search("^ +", text)[0]) % 4:
                return True
        return False

    def check_semicolons(text):
        if "#" in text:
            text = text.split("#", maxsplit=1)[0]
        text = re.sub("[\'\"].+[\'\"]", "", text)
        if re.search(";", text):
            return True
        return False

    def check_comments_space(text):
        if "#" in text and text[0] != "#":  # own line comments shouldn't be caught.
            text = text.split("#", maxsplit=1)[0]
            if not re.search(" {2,}$", text):
                return True
            return False

    def check_todo(text):
        if "#" in text:
            text = text.casefold().split("#", maxsplit=1)[1]
            if re.search("todo", text):
                return True
        return False

    def check_blank_lines(i):
        if line_by_line[i] != "" and line_by_line[i - 1] == "" \
                and line_by_line[i - 2] == "" and line_by_line[i - 3] == "":
            return True
        return False

    def check_construction_name_space(text):
        if "#" in text:
            text = text.split("#", maxsplit=1)[0]
        if re.search("(def|class) {2,}", text):
            return True
        return False

    def check_class_case(text):
        if "#" in text:
            text = text.split("#", maxsplit=1)[0]
        if re.search("class +[a-z].*:", text) or re.search("class +.*_.*:", text):
            return True
        return False

    def check_line(index, line):

        if check_length(line):
            found_errors.append(f"{file_path}: Line {index + 1}: S001 Too long")

        if check_indentation(line):
            found_errors.append(f"{file_path}: Line {index + 1}: S002 Indentation is not a multiple of four")

        if check_semicolons(line):
            found_errors.append(f"{file_path}: Line {index + 1}: S003 Unnecessary semicolon")

        if check_comments_space(line):
            found_errors.append(f"{file_path}: Line {index + 1}:"
                                f" S004 At least two spaces required before inline comments")

        if check_todo(line):
            found_errors.append(f"{file_path}: Line {index + 1}: S005 TODO found")

        if check_blank_lines(index):
            found_errors.append(f"{file_path}: Line {index + 1}: S006 More than two blank lines used before this line")

        if check_construction_name_space(line):
            found_errors.append(
                f"{file_path}: Line {index + 1}: S007 Too many spaces after {re.search('(def|class) +(.+)', line)[1]}")

        if check_class_case(line):
            found_errors.append(f"{file_path}: Line {index + 1}: S008 Class name {re.search('class +(.+)', line)[1]}"
                                f" should be written in CamelCase")

    if os.path.isdir(path_to_analyze):
        files = os.listdir(path_to_analyze)
        head_path = path_to_analyze
    else:
        files = [os.path.basename(path_to_analyze)]
        head_path = os.path.dirname(path_to_analyze)

    for file in files:

        if file.endswith(".py"):

            file_path = os.path.join(head_path, file)

            with open(file_path, "r") as analyze:
                raw_code = analyze.read()
                line_by_line = raw_code.splitlines()

            tree = ast.parse(raw_code)
            nodes = ast.walk(tree)
            catched_variables = []

            for n in nodes:
                if isinstance(n, ast.FunctionDef):
                    if re.search("[A-Z]", Analyzer().visit(n)[0]):
                        found_errors.append(f"{file_path}: Line {Analyzer().visit(n)[1]}: S009 Function name "
                                            f"{Analyzer().visit(n)[0]} should be written in snake_case")
                    for item in n.args.defaults:
                        if isinstance(item, (ast.List, ast.Dict, ast.Set)):
                            found_errors.append(f"{file_path}: Line {Analyzer().visit(n)[1]}: S012"
                                                f" The default argument value is mutable.")
                if isinstance(n, ast.arg):
                    if re.search("[A-Z]", Analyzer().visit(n)[0]):
                        found_errors.append(f"{file_path}: Line {Analyzer().visit(n)[1]}: S010 argument name "
                                            f"{Analyzer().visit(n)[0]} should be written in snake_case")
                if isinstance(n, ast.Name):
                    if re.search("[A-Z]", Analyzer().visit(n)[0]) and Analyzer().visit(n)[0] not in catched_variables:
                        found_errors.append(f"{file_path}: Line {Analyzer().visit(n)[1]}: S011 Variable name "
                                            f"{Analyzer().visit(n)[0]} should be written in snake_case")
                        catched_variables.append(Analyzer().visit(n)[0])

            for index_of_line, code in enumerate(line_by_line):
                check_line(index_of_line, code)

    for error in natsorted(found_errors):
        print(error)


if __name__ == "__main__":
    args = sys.argv
    if len(args) != 2:
        print("The script should be called with one argument, a file or a directory.")
    else:
        code_analyzer(args[1])
