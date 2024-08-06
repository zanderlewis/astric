import ast
import black
import os


def remove_comments_and_format(file_path):
    with open(file_path, "r") as source:
        tree = ast.parse(source.read())
    code_without_comments = ast.unparse(tree)
    formatted_code = black.format_str(code_without_comments, mode=black.FileMode())
    with open(file_path, "w") as source:
        source.write(formatted_code)


def cleanup():
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                remove_comments_and_format(file_path)


cleanup()
