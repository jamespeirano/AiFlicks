import datetime

# This function will generate a timestamped and function-scoped print output.
def pprint(message, function_name):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [Function: {function_name}] {message}")