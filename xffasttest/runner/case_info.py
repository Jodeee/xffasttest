class CaseInfo:

    (SUCCESS, FAILURE, ERROR, SKIP) = range(4)

    def __init__(self) -> None:
        self.reports = None
        self.file_name = None
        self.case_module = None
        self.case_name = None
        self.case_desc = None
        self.case_source = None
        self.start_time = 0
        self.end_time = 0
        self.elapsed_time = 0
        self.status = None
        self.message = None

    def set_attrs(self, **kwargs) -> None:
        for key, value in kwargs.items():
            setattr(self, key, value)