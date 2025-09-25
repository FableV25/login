import logging

info_logger = logging.getLogger('notes_app.info')
warning_logger = logging.getLogger('notes_app.warning')
error_logger = logging.getLogger('notes_app.error')
general_logger = logging.getLogger('notes_app')

def log_info(message, extra_data=None):
    """Log info level messages"""
    if extra_data:
        info_logger.info(f"{message} - Extra data: {extra_data}")
    else:
        info_logger.info(message)

def log_warning(message, extra_data=None):
    """Log warning level messages"""
    if extra_data:
        warning_logger.warning(f"{message} - Extra data: {extra_data}")
    else:
        warning_logger.warning(message)

def log_error(message, exception=None, extra_data=None):
    """Log error level messages"""
    error_message = message
    if exception:
        error_message += f" - Exception: {str(exception)}"
    if extra_data:
        error_message += f" - Extra data: {extra_data}"
    error_logger.error(error_message, exc_info=exception is not None)

def log_debug(message, extra_data=None):
    """Log debug level messages"""
    if extra_data:
        general_logger.debug(f"{message} - Extra data: {extra_data}")
    else:
        general_logger.debug(message)

class LogFunctionCall:
    def __init__(self, function_name, user_id=None):
        self.function_name = function_name
        self.user_id = user_id
    
    def __enter__(self):
        user_info = f" (User: {self.user_id})" if self.user_id else ""
        log_info(f"Entering function: {self.function_name}{user_info}")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            log_error(f"Function {self.function_name} failed", exc_val)
        else:
            log_info(f"Function {self.function_name} completed successfully")