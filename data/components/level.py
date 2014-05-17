

class Level(object):
    def __init__(self, obst_json, width, height, num_cows, 
                         cow_rangex, cow_rangey, cow_angle,
                         cowboy_pos, title):
        self.obst_json = obst_json
        self.num_cows = num_cows
        self.width = width
        self.height = height
        self.cow_rangex = cow_rangex
        self.cow_rangey = cow_rangey
        self.cow_angle = cow_angle
        self.cowboy_pos = cowboy_pos
        self.title = title
        
levels = {1: Level("level1", 3000, 3000, 10, (100, 400), (100, 400), 1.75,
                           (550, 400), "Learning the Ropes"),      
              2: Level("level2", 4000, 4000, 30, (100, 400), (100, 400), 1.75,
                           (550, 370), "The Long Way 'Round"),
              3: Level("level3", 4000, 4000, 20, (100, 400), (2600, 3000), 0,
                           (200, 2500), "Whoa, Wolf Woes"),
              4: Level("level4", 4000, 4000, 30, (1500, 2500), (100, 600), 1.5,
                           (2000, 700), "A Rocky Start"),
              5: Level("level5", 2000, 2000, 50, (100, 1900), (100, 1900), "random",
                           (1000, 900), "Roundup"),
              6: Level("level6", 4000, 4000, 25, (3500, 3850), (3500, 3850), .5,
                           (3700, 3900), "Heinous Lupus"),
              7: Level("level7", 4000, 4000, 25, (3500, 3850), (600, 1000), 1,
                           (3700, 1150), "How Now, Down Cow"),
              8: Level("level8", 4000, 4000, 5, (2000, 2100), (100, 200), 1.5,
                           (1900, 200), "Wolf Insanity")}
