import os
import inspect
import importlib

def extract_functions_and_classes(module):
	functions = []
	classes = []
	for name, obj in inspect.getmembers(module):
		if inspect.isfunction(obj) and obj.__module__ == module.__name__:
			functions.append(name)
		elif inspect.isclass(obj) and obj.__module__ == module.__name__:
			classes.append(name)
	return functions, classes

def main():
	base_path = os.path.dirname(os.path.abspath(__file__))
	package_name = "hangulpy"
	package_path = os.path.join(base_path, package_name)

	import_statements = []

	for filename in os.listdir(package_path):
		if filename.endswith(".py") and filename != "__init__.py" and filename != "utils.py":
			module_name = filename[:-3]  # Remove .py extension
			module = importlib.import_module(f"{package_name}.{module_name}")

			functions, classes = extract_functions_and_classes(module)

			if functions or classes:
				import_statements.append(f"from .{module_name} import " + ", ".join(functions + classes))

	# Output the import statements to the console
	for statement in import_statements:
		print(statement)

if __name__ == "__main__":
	main()
