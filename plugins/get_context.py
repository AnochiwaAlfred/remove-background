
# dashboard.context_processors.

from dashboard import context_processors 

def get_context():
    blacklist = ['apps', 'reverse']
    whitelist = []
    for item in dir(context_processors):
        if "__" not in item and item not in blacklist:
            whitelist.append(f"dashboard.context_processors.{item}")
    return whitelist
    
