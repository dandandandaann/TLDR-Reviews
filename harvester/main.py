from harvest import Harvest
from config import setup_logging, load_config

if __name__ == '__main__':
    logger = setup_logging()
    config = load_config('secrets.cfg')

    result = Harvest(config['HwApi']).property(325889)

    print(result["reviews"][0])
    print(result["name"])
    print(result["currency"])
    print(result["type"])
    print(result["facilities"])

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
