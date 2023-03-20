import sys

def error_message_detail(error,error_detail:sys):
    _,_,exc_tb=error_detail.exc_info()
    file_name=exc_tb.tb_frame.f_code.co_filename
    error_message="Error occured in python script name [{}] line number [{}],error message [{}]".format(file_name,exc_tb.tb_lineno,str(error))
    return error_message 

class CustomExeception(Exception):
    def __init__(self,error_message,error_detail:sys):
        super().__init__(error_message)
        self.error_messsage=error_message_detail(error_message,error_detail)

    def __str__(self) -> str:
        return self.error_messsage