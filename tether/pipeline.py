class Pipeline:
    ...

    def step(self, *args, **kwargs):
        """Defines a new pipeline step with optional parameters. """
        if len(args) == 1 and len(kwargs) == 0 and callable(args[0]):
            # called as @step
            ...
        
        else:
            # called as @step(*args, **kwargs)
            ...