import json

class EngineVars:
    running_effect = True
    
    def __init__(self):
        with open('settings.json') as json_data_file:
            data = json.load(json_data_file)
        #Initialize Hardware
        self.PIXEL_COUNT = data["hardware"]["PIXEL_COUNT"]
        self.SPI_PORT = data["hardware"]["SPI_PORT"]
        self.SPI_DEVICE = data["hardware"]["SPI_DEVICE"]
        self.RGB_ORDER = data["hardware"]["RGB_ORDER"]
        #Read Calibration
        self.redcal = data["calibration"]["red"]
        self.greencal = data["calibration"]["green"]
        self.bluecal = data["calibration"]["blue"]

        #Starting Values
        self.luminosity = data["starter"]["luminosity"]
        self.maximize = data["starter"]["maximize"]
        self.sequences = data["starter"]["sequence"]
        self.color = data["starter"]["color"]
        self.effect = data["starter"]["effect"]

        print("Running")