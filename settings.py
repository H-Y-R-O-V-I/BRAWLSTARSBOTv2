import json
import configparser
from modules.print import bcolors
brawlerStatsDict = json.load(open("brawler_stats.json"))


def parse_config_file(config:  list[str]):
    config_dict = {}

    for section in config.sections():
        section_data = {}
        for key, value in config[section].items():
            if value.lower() == "true":
                section_data[key] = True
            elif value.lower() == "false":
                section_data[key] = False
            elif value.lower() == "none":
                section_data[key] = None
            else:
                try:
                    section_data[key] = int(value)
                except ValueError:
                    try:
                        section_data[key] = float(value)
                    except ValueError:
                        section_data[key] = value
        config_dict[section] = section_data

    return config_dict


class Settings:
    configParser = configparser.ConfigParser()
    configParser.read('config.ini')
    config = parse_config_file(configParser)['Default']
    
    #! Brawler's stats
    brawlerName = config['brawler_name']
    
    #! Map's characteristics
    sharpCorner = config['sharp_corner']
    centerOrder = config['center_order']
    
    #! Window Capture
    window_name = config['window_name']
    # Make this False if detection_test is outputting a blank screen, otherwise True.
    focused_window = config['focused_window']

    #! Change this to True if you have Nvidia graphics card and CUDA installed
    nvidia_gpu = config['nvidia_gpu']

    # Main contants
    DEBUG = config['debug']

    #! Do not change these
    # Detector constants
    classes = ["Player","Bush","Enemy","Cubebox"]
    """
    Threshold's index correspond with classes's index.
    e.g. First element of classes is player so the first
    element of threshold is threshold for player.
    """
    threshold = [0.4,0.4,0.43,0.65]

    print("")
    print(bcolors.BOLD + bcolors.OKGREEN + "Check https://github.com/Jooi025/BrawlStarsBot for the latest update!" + bcolors.ENDC)
    print("")

    # find brawler in the json 
    brawlerStats = brawlerStatsDict.get(brawlerName)
    if brawlerStats is not None:
        print(bcolors.WARNING + f"Selected Brawler: {brawlerName}" + bcolors.ENDC)
    else: 
        invalidBrawlerString = f"Invalid Brawler name in config.ini! (Case Sensitive)\nYou mean this?\n"
        brawlersNameList = [key for key in brawlerStatsDict]
        for name in brawlersNameList:
            if name[0].lower() == brawlerName[0].lower():
                invalidBrawlerString += f"- {name}\n"
        print(bcolors.WARNING + invalidBrawlerString + bcolors.ENDC)
        exit()

    movementSpeed = brawlerStats["Base"]["Movement speed"]
    attackRange = brawlerStats["Attack"]["Range"]
    
    try:
        heightScale = brawlerStats["HSF"]
    except KeyError:
        heightScale = None
        print(bcolors.FAIL + "HSF not found, run \"hsf_finder.py\" for more info!" + bcolors.ENDC)

    print(bcolors.OKBLUE + f"Speed: {movementSpeed} tiles/second \nAttack Range: {attackRange} tiles\nHSF: {heightScale}\n" + bcolors.ENDC)

    # interface
    if nvidia_gpu is None:
        # load TensorRT interface
        model_file_path = "yolov8_model/yolov8.engine"
        half = False
        imgsz = 640
    elif nvidia_gpu:
        # load pytorch interface
        model_file_path = "yolov8_model/yolov8.pt"
        half = False
        imgsz = (384,640)
    else:
        # load openvino interface
        model_file_path = "yolov8_model/yolov8_openvino_model"
        half = True
        imgsz = (384,640)
    
    #bot constant
    movement_key = "middle"
    midpointOffsetScale = 0.024
    
    bool_dict = {
        "sharpCorner": sharpCorner,
        "centerOrder": centerOrder,
    }

    for key in bool_dict:
        assert type(bool_dict[key]) == bool,f"{key.upper()} should be True or False"

if __name__ == "__main__":
    pass