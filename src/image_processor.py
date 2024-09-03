class ImageProcessor:
    def __init__(self, functions):
        self.functions = functions
        self.selected_idx = 0
        self.algorithm_names = self.__get_algorithm_names()

    def __get_algorithm_names(self):
        # Send an empty dictionary to the function so that it will only return the algorithms name.
        algorithm_names = []
        for idx, function in enumerate(self.functions):
            # Send an empty dictionary to the function so that it will only return the algorithms name.
            params = function({})
            algorithm_names.append(f'{idx:03d}\t{params["algorithm_name"]}')
        return algorithm_names

    def process(self, params):
        function = self.functions[self.selected_idx]
        params = function(params)
        return params

    def next_algorithm(self):
        self.selected_idx = (self.selected_idx + 1) % len(self.functions)

    def prev_algorithm(self):
        self.selected_idx = (self.selected_idx - 1) % len(self.functions)
