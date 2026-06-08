import ast
def parse_python_metadata(content):
    tree=ast.parse(content)
    classes = []
    functions = []
    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            classes.append(node.name)

        elif isinstance(node, ast.FunctionDef):
            functions.append(node.name)

        elif isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)

        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.append(node.module)

    return {
        "classes": classes,
        "functions": functions,
        "imports": imports
    }