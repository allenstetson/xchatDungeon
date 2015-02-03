__module_name__ = 'environment'
__module_version__ = '1.0'
__module_description__ = 'Weather, time of day, local features, etc.'
__module_author__ = 'Allen Stetson'

from random import randint
import sys
sys.path.insert(0, '/work/td/xchat/mod/')
from dnd.utils import ProbabilityArray
from dnd.locations import LocationGenerator

class EnvirGenerator(object):
    def __init__(self):
        # Keep these sorted... sorta.
        self.times = ["dawn", "morning", "afternoon", "day", "dusk", "twilight", "evening", "midnight", "night"]
        # Initialize settings.
        self.randNum = randint(1,100)
        self.timeOfDay = self.getTimeOfDay()
        self.temperature = self.getTemperature()
        self.conditionType = None
        self.condition = self.getCondition()
        self.nearbyFeature = None
        self.location = self.getLocation()
        self.moonPhase = self.getMoon()       
        
    def getTimeOfDay(self):
        # night, dawn, morning, day, afternoon, dusk, twilight, evening, midnight
        self.timeOfDay = self.times[randint(0,len(self.times)-1)]
        return self.timeOfDay
        
    def getTemperature(self):
        # Warm, cold, hot, frigid, cool,
        temps = [('frigid',1),('cold',2),('cool',3),('warm',3),('hot',2),('blisteringly hot',1)]
        probabilityArray = ProbabilityArray()
        temps = probabilityArray.create(temps)
        if self.randNum == 1:
            temps = ['frigid','blisteringly hot']
        self.temperature = temps[randint(0,len(temps)-1)]
        return self.temperature
        
    def getCondition(self):
        # Sunny, windy, rainy, snowy, still, blustery, clear, torrentially rainy, blizzardy, foggy, smoky
        temp = self.temperature
        conditions = [('windy','wind'),('rainy','wet'),('still','norm'),('blustery','wind'),('clear','norm'),
                      ('smoky','smoke'),('hazy','norm')]
        if temp == "frigid" or temp == "cold":
            conditions.extend([('hailing','cold'), ('snowy','cold'), ('blizzarding','cold'),
                               ('torrentially rainy','cold'),('foggy','cold'),('drizzly','cold')])
        elif temp == "hot" or temp == "blisteringly hot":
            conditions.extend([('stagnant','hot'), ('dusty','hot')])
        else:
            conditions.extend([('torrentially rainy','wet'), ('foggy','norm'), ('drizzly','wet')])
        (self.condition,self.conditionType) = conditions[randint(0,len(conditions)-1)]
        return self.condition
        
    def getLocation(self, conditionType=None):
        if not conditionType:
            conditionType = self.conditionType
        locationGenerator = LocationGenerator(conditionType=conditionType)
        self.location = locationGenerator.location
        self.getNearbyFeature()
        return self.location
        
    def getNearbyFeature(self, location=None):
        if not location:
            location = self.location
        locationGenerator = LocationGenerator(location=location)
        self.nearbyFeature = locationGenerator.nearbyFeature
        return self.nearbyFeature
    
    def getMoon(self):
        phases = ['waxing','quarter','half','gibbous','full','waning','crescent','new']
        phase = phases[randint(0,len(phases)-1)]
        return phase
    
    def getWeather(self):
        """
        Based on our initial "roll of the dice" (random int 0-100), if it is exceptionally low,
        death is imminent. Exceptionally high, and special things result. In the middle, and you
        get a more normal weather event.

        Within the normal weather event, things like the time of day and location are used to generate
        an appropriate event.
        :return: printable string for xchat
        :rtype: str
        """
        # DEATH
        if self.randNum == 1:
            printStr =  "It is an unbearably %s %s. It takes all of your effort to stave off death from this %s weather, " % (self.temperature,self.timeOfDay,self.condition)
            printStr += "and soon your strength will run out. Your bones will litter the %s where you lay." % (self.location)
            return(printStr)
        # PARADISE
        elif self.randNum == 95:
            printStr =  "It is a perfect %s in the %s. The weather could not be more to your liking. " % (self.timeOfDay, self.location)
            printStr += "You can not help but wonder if you hold the favor of your gods, at the moment."
            return(printStr)
        # DENIAL
        elif self.randNum > 95:
            printStr =  "It is a quiet, air-conditioned %s in the workplace. " % (self.timeOfDay)
            printStr += "The ambient hum of machines fills the air with soothing white noise, its haze broken only by occasional echoes of coworker dialogue in the distant cubicles. "
            printStr += "You recline comfortably in your office chair, toggling idly between desktops as your mind drifts to far-off fantasy lands, "
            printStr += "pondering what the future will bring and "
            if self.timeOfDay in self.times[:2]:
                printStr += "what the fates have decreed for lunch today."
            elif self.timeOfDay in self.times[-2:]:
                printStr += "when you can stop burning the midnight oil."
            else:
                printStr += "digesting the plate of lunch you consumed earlier."
            return(printStr)
        # NORMAL (not DEATH, PARADISE, or DENIAL)
        else:
            # UNDERDARK
            if self.location == "underdark":
                printStr = "It is a %s %s %s in the world above, though down here in the %s it is always the same." % (self.temperature, self.condition, self.timeOfDay, self.location)
                if self.conditionType == "cold":
                    printStr += " The cold from the %s seems to radiate downward, although the torches provide a comforting warmth in this otherwise " % self.nearbyFeature
                    printStr += "unwelcoming world."
                elif self.conditionType == "hot":
                    printStr += " The heat from the %s seems to radiate downward, although the dark shadows provide a comforting respite in this otherwise " % self.nearbyFeature
                    printStr += "unwelcoming world."
                else:
                    printStr += " The looming shadows, oppressive silence, and stench of this world make you long for the %s." % self.nearbyFeature
                return(printStr)
            # NOT UNDERDARK
            else:
                printStr = "It is a %s %s %s in the %s." % (self.temperature, self.condition, self.timeOfDay, self.location)
                if self.location == "coast":
                    printStr = printStr.replace(" in ", " on ")
        ## MOON
        if self.timeOfDay in ['night','twilight','evening','midnight']:
            if not self.conditionType == "wet":
                if not self.moonPhase == "new":
                    typesOfGlows = ['a calming','an eerie','an otherworldly','a dreamy']
                    glow = typesOfGlows[randint(0,len(typesOfGlows)-1)]
                    printStr += " The %s moon casts %s glow on the landscape." % (self.moonPhase, glow)
                if self.moonPhase == "full":
                    printStr += " The ominous howl of a nearby creature fills you with unease."
        ## WET
        if self.conditionType == "wet":
            printStr += " Rain pelts the %s all around." % self.nearbyFeature
            if self.randNum < 4:
                printStr += " Floodwaters rise ever higher. You search for nearby debris on which to cling for safety."
            elif self.randNum < 12:
                printStr += " The deafening peal of thunder reverberates off of the %s nearby as blinding flash of lightning strikes not far away." % self.nearbyFeature
            elif self.temperature == "hot":
                printStr += " The cool rain brings you welcome relief from the heat of the %s." % self.timeOfDay
            elif self.condition == "rainy":
                printStr += " You turn your face to the sky and soak in the cleansing rain."
            else:
                printStr += " You seek shelter anywhere you can in an attempt to stay dry."
        ## COLD
        elif self.conditionType == "cold":
            if self.randNum <= 30:
                printStr += " A chill radiates off of the %s around you. You pull your coat close to your body in an attempt to keep warm." % self.nearbyFeature
            elif self.randNum < 50:
                printStr += " You scowl at your empty tinderbox and useless flint as you plod through the %s trying to keep your body warm." % self.nearbyFeature
            elif self.randNum > 94:
                printStr += " The cold seeping in through your armor could not feel better as it cools your sweaty, battle-worn muscles."
            else:
                printStr += " Frost coats the nearby %s; your breath rises in visible puffs. You shiver involuntarily." % self.nearbyFeature
        ## WINDY
        elif self.conditionType == "wind":
            printStr += " Winds beat the %s around you." % self.nearbyFeature
            if self.condition == "blustery":
                garmentType = ['garments','loincloth','cape','dark cloak','robes']
                garmentWorn = garmentType[randint(0,len(garmentType)-1)]
                printStr += " You lean into the oncoming wind and push through, your %s flapping behind you." % garmentWorn
            else:
                hatType = ['hat','helmet','feather cap','hood','tricorn hat','head scarf']
                hatWorn = hatType[randint(0,len(hatType)-1)]
                actionType = ['soldier on', 'charge', 'dash', 'crawl', 'plod wearily', 'march']
                actionTaken = actionType[randint(0,len(actionType)-1)]
                printStr += " You hold your %s with one hand as you %s into the wind." % (hatWorn, actionTaken)
        ## HOT
        elif self.conditionType == "hot" or self.temperature == "blisteringly hot":
            if self.randNum < 10:
                printStr += " You impotently lick your sun-battered lips with your dry tongue as you feverishly look for any sign of fresh water."
            elif self.randNum < 20:
                printStr += " A blinding light reflects off of the %s adjacent from you; a taunting reminder of the utter lack of respite from the heat." % self.nearbyFeature
            elif self.randNum > 95:
                printStr += " The heat radiating off of the nearby %s makes the cool touch of the sparkling lake in which you swim all the more refreshing." % self.nearbyFeature
            else:
                printStr += " An uncomfortable heat radiates off of the %s around you. Your sweaty clothes stick to you as you move." % self.nearbyFeature
        ## SMOKY
        elif self.condition == "smoky":
            thingsThatBurn = ['the nearby village',"the enemy's encampment", "the vermin's nest", 'what used to be your home','the weapons of war']
            if self.location == 'coast':
                thingsThatBurn.extend(['your defeated armada','the treasure galleon','the docks',"the enemy's fleet",'the shipwreck','the mermaid\'s alcove'])
            elif self.location == 'mountains':
                thingsThatBurn.extend(['cliff dwellings',"eagles' nests",'the mining encampment','the log cabin'])
            elif self.location == 'grasslands':
                thingsThatBurn.extend(['the dry grass','the landscape','the catfolk village','the vineyard'])
            elif self.location == 'jungle':
                thingsThatBurn.extend(["the hunter's perch",'the hideout','the temple','the only bridge across the gaping chasm','the secret weapon'])
            elif self.location == 'city':
                thingsThatBurn.extend(['the tavern','the prison','the gallows','the district',"the nobleman's abode",'the slave quarters','the magic academy', \
                                   'the thieves guild','your home',"that greedy bastard's home",'the safehouse','the warehouse'])
            elif self.location == 'settlement':
                thingsThatBurn.extend(['the food storage','the church','the adjacent woods',"the monster's body",'the general store',"the woodcutter's shop"])
            elif self.location == 'fort':
                thingsThatBurn.extend(["the captain's abode",'the protective wall','the map room','the stables','the war machines','the weapons store',"the raven's roost"])
            elif self.location == 'marsh':
                thingsThatBurn.extend(['the hatchery', 'the dam', 'the coven house', 'the manticore den', 'the lizardfolk village',"the green hag's cabin"])
            elif self.location == 'meadow':
                thingsThatBurn.extend(['the windmill', 'the cottage'])
            elif self.location == 'forest':
                thingsThatBurn.extend(['the ettercap den'])
            elif self.location == 'hills':
                thingsThatBurn.extend(["the hill giant's home"])
            
            whatBurned = thingsThatBurn[randint(0,len(thingsThatBurn)-1)]
            
            if self.randNum < 4:
                printStr += " The charred remains of %s mark your irrevocable decent into evil." % whatBurned
            elif self.randNum < 7:
                printStr += " The charred remains of %s serve as a reminder of your unquestioning devotion to your deity." % whatBurned
            elif self.conditionType == 'cold' and self.randNum < 50:
                printStr += " The smouldering remains of %s provide at least a little warmth to your otherwise numb body." % whatBurned
            elif self.conditionType == 'wet' and self.randNum < 50:
                printStr += " The smouldering remains of %s sizzle with each drop of precipitation unlucky enough to target it." % whatBurned
            elif self.randNum < 30:
                printStr += " The charred remains of %s scar the land." % whatBurned
            elif self.randNum < 60:
                printStr += " The charred remains of %s fill you with pride." % whatBurned
            elif self.randNum < 80:
                printStr += " The charred remains of %s fill you with rage." % whatBurned
            elif self.randNum < 99:
                printStr += " The charred remains of %s fill you with sadness." % whatBurned
            elif self.randNum < 100:
                printStr += " The thick hookah smoke still pleasantly burns your nostrils and massages your mind." % whatBurned
                
        return(printStr)
