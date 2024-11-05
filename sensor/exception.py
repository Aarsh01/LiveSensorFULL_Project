import sys 
# It is system Library,
# System related information, we can access it,

# Why?
# Answer: Thier are in-build functions which show us the errors. But We want to see where is the error (like file location, which line, etc). So we make file "exception file" where we write the code to customize the errors and then modify them according to us. 

def error_message_detail(error: Exception, error_detail: sys) -> str:
    """
    Extracts detailed error information.

    : error: The exception that was raised.
    : error_detail: The sys module to access traceback details.
    :return: A formatted error message string.
    """
    _, _, exc_tb = error_detail.exc_info()
    # after exc_tb we will be finding the the above 3 aspects
    
    # what is the file name where error is occured.
    file_name = exc_tb.tb_frame.f_code.co_filename
    line_number = exc_tb.tb_lineno

    error_message = (
        f"Error occurred in file [{file_name}], "
        f"line number [{line_number}], "
        f"error message: [{str(error)}]"
    )
    return error_message


class SensorException(Exception):
    """
    Custom exception class for sensor-related errors.
    """
    def __init__(self, error_message: str, error_detail: sys):
        """
        Initializes the SensorException with an error message and details.

        : error_message: The error message to be displayed.
        : error_detail: The sys module to access traceback details.
        """     
        super().__init__(error_message) # error_message is coming from supper class i.e Exception class
        self.error_message = error_message_detail(error_message, error_detail)

        
    def __str__(self) -> str:
        """Returns the string representation of the error message."""
        return self.error_message
    