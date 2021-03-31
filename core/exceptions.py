
class AutoCoreException(Exception):
    pass

class AlreadyConfiguredTableException(AutoCoreException):
    def __init__(self, table_name: str, base_url: str):
        self.table_name = table_name
        self.base_url = base_url
        super(AlreadyConfiguredTableException, self).__init__(self)
    
    def __str__(self):
        return (
            f"Table {self.table_name} or route {self.base_url} had already"
            " been configured. They are repeated"
        )

class TableNotConfiguredYetException(AutoCoreException):
    def __init__(self, table_name: str):
        self.table_name = table_name
        super(TableNotConfiguredYetException, self).__init__(self)
    
    def __str__(self):
        return (
            f"Table {self.table_name} has not "
            "been configured to an url yet"
        )

class MethodNotAllowedException(AutoCoreException):
    pass