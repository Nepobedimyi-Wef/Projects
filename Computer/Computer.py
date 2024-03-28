class Computer():
    def __init__(self, type):
        self.type = type
        self.comp_properties = {}
        
    def set_properties(self, color, video_card, processor, memory):
        self.comp_properties = {"Color": color, "Video Card": video_card, "Processor": processor, "Memory": memory}

    def get_properties(self):
        return self.comp_properties

class Desktop(Computer):
    def __init__(self, type):
        super().__init__(type)

computer = Computer("MSU")
computer.set_properties("Black", "RTG4010", "Untile Cire i1-288sigma", 1024)

desktop = Desktop("Kyzen")
desktop.set_properties("Blue", "RTG3030", "Untile Cire i1-2man", 512)

computers = [computer, desktop]

def find_black_computer(computers):
    black_comp = 0
    for comp in computers:
        if comp.get_properties()["Color"] == "Black":
            black_comp += 1
    print(f"Number of Black Computers = {black_comp}")

find_black_computer(computers)
