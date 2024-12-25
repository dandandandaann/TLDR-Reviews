from harvest import Harvest
from configparser import ConfigParser

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press F9 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

    config = ConfigParser()
    config.read('secrets.cfg')

    result = Harvest(config['HwApi'], 3.0).property(325889)

    print(result["reviews"][0])
    print(result["name"])
    print(result["currency"])
    print(result["type"])
    print(result["facilities"])

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
