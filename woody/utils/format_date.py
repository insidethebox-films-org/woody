from datetime import datetime

def format_date(key=None, value=None):

    if value is None:
        return "None"
    
    if isinstance(value, datetime):
        return value.strftime("%d %b, %Y  %I:%M %p")
    
    if key in ['created_time', 'modified_time']:
        try:
            if isinstance(value, str):
                dt = datetime.fromisoformat(value.replace('Z', '+00:00'))
                return dt.strftime("%d %b, %Y  %I:%M %p")
        except:
            pass
        
    return str(value)