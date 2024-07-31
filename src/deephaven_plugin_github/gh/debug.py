import json
import os

def debug_json_dump(file_name: str, content):
    if not os.environ.get("DHGH_DEBUG_DUMP_PATH"):
        return None
    
    file_path = get_debug_dump_file_path(file_name)

    print(f"Dumping project items to {file_path}")
    with open(file_path, "w") as outfile:
        json.dump(content, outfile, indent=2)

def get_debug_dump_dir() -> str:
    dir_path = os.environ.get("DHGH_DEBUG_DUMP_PATH")
    if dir_path == None:
        return None
    
    dir_path = dir_path + os.sep + ".debug"
    
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    
    return dir_path

def get_debug_dump_file_path(file_name: str) -> str:
    dir = get_debug_dump_dir()
    return dir + os.sep + file_name if dir else None