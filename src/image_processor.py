class ImageProcessor:
    def __init__(self, functions, selected_idx=0, print_markdown_table=False):
        self.functions = functions
        self.selected_idx = (
            selected_idx if selected_idx >= 0 and selected_idx < len(functions) else 0
        )
        self.algorithm_names = self.__get_algorithm_names()
        if print_markdown_table:
            self.print_markdown_table()

    def __get_algorithm_names(self):
        algorithm_names = []
        for function in self.functions:
            # Send an empty dictionary to the function so that it will only return the algorithms name.
            params = function({})
            algorithm_names.append(params["algorithm_name"])
        return algorithm_names

    def process(self, params):
        function = self.functions[self.selected_idx]
        params = function(params)
        return params

    def next_algorithm(self):
        self.selected_idx = (self.selected_idx + 1) % len(self.functions)

    def prev_algorithm(self):
        self.selected_idx = (self.selected_idx - 1) % len(self.functions)

    def print_markdown_table(self):
        """
        This function prints the currently available algorithms with their respective
        ID and description in a markdown table so that it can be easily copy pasted
        into the repositories README.
        """
        print(
            "Available algorithms and their IDs in a markdown table for the README:\n"
        )
        print("| ID | algorithm |")
        print("| :---: | :--- |")
        for idx, algorithm_name in enumerate(self.algorithm_names):
            print(f"| `{idx}` | {algorithm_name} |")
        print("\n")
