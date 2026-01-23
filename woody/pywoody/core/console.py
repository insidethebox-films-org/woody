import logging
import os
from functools import wraps
from contextlib import redirect_stdout, redirect_stderr

# --- Colours ---
WOODY = "\033[38;2;255;255;0m\033[1m"      
PROJECT = "\033[94m"
PRODUCT = "\033[38;2;138;43;226m"
GREEN = "\033[92m"     
ORANGE = "\033[38;2;255;165;0m" 
RED = "\033[91m"         
RESET = "\033[0m"
BOLD = "\033[1m"

# --- Custom Logging Levels ---
SUCCESS_LEVEL = 25
logging.addLevelName(SUCCESS_LEVEL, "SUCCESS")

# --- Error Handling ---
class WoodyError(Exception):
    def __init__(self, message, level="error", label="Error"):
        self.message = message
        self.level = level
        self.label = label
        super().__init__(self.message)

    def __str__(self):
        return format_msg(self.label, self.message, self.level)

def handle_woody_errors(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except WoodyError as e:
            print(str(e))
            return None
        except Exception as e:
            print(format_msg("Fatal", str(e), "error"))
            return None
    return wrapper

def quiet(func):
    """Decorator to suppress all prints and logs during function execution"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        
        original_level = woody_logger.level
        
        logging.disable(logging.CRITICAL)
        
        with open(os.devnull, 'w') as devnull:
            with redirect_stdout(devnull), redirect_stderr(devnull):
                try:
                    result = func(*args, **kwargs)
                    return result
                finally:
                    logging.disable(logging.NOTSET)
                    woody_logger.setLevel(original_level)
    
    return wrapper

# --- Formatting ---
def format_msg(label, message, level="info"):
    levels = {
        "success": GREEN, 
        "error": RED, 
        "warning": ORANGE, 
        "woody": WOODY, 
        "info": WOODY
    }
    color = levels.get(level.lower(), RESET)
    return f"{color}[{label}]{RESET} {message}"

def get_prompt(project_name, context):
    project = project_name or "none"
    
    if context == None:
        return f"{WOODY}[woody]{RESET}{PROJECT}[{project}]{RESET} > "
    
    tree = context[0]
    group = context[1]
    asset = context[2]
    
    product_type = context[3]
    product_name = context[4]

    if product_type == None:
        return f"{WOODY}[woody]{RESET}{PROJECT}[{project}]{RESET}[{tree}/{group}/{asset}] > "
    else:
        return f"{WOODY}[woody]{RESET}{PROJECT}[{project}]{RESET}[{tree}/{group}/{asset}]{PRODUCT}[{product_type}/{product_name}]{RESET} > "

# --- Logging  --- 
class WoodyConsoleHandler(logging.Handler):
    def emit(self, record):
        msg = record.getMessage()
        if record.levelno == SUCCESS_LEVEL:
            print(format_msg("Success", msg, "success"))
        elif record.levelno >= logging.ERROR:
            print(format_msg("Error", msg, "error"))
        elif record.levelno >= logging.WARNING:
            print(format_msg("Warning", msg, "warning"))
        else:
            print(format_msg("woody", msg, "info"))

def setup_logger():
    logger = logging.getLogger("woody")
    logger.setLevel(logging.DEBUG)
    
    if not logger.handlers:
        logger.addHandler(WoodyConsoleHandler())
    return logger

woody_logger = setup_logger()