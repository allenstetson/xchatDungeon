__module_name__ = 'dnd.location'
__module_version__ = '1.0'
__module_description__ = 'Choose a geographic location'
__module_author__ = 'Allen Stetson'


from random import randint

class LocationGenerator(object):
    def __init__(self, location=None, world=None, kingdom=None, conditionType=None):
        self.location = location
        self.world = world
        self.kingdom = kingdom
        self.conditionType = conditionType
        self.nearbyFeatures = []
        self.nearbyFeature = None
        if not self.location:
            self.location = self.getLocation()
        self.getNearbyFeatures()

    def getLocation(self):
        if self.world and self.world.lower() == 'faerun':
            # Load the list kingdoms
            faerunFile = file("/work/td/xchat/lists/kingdoms_of_faerun.txt")
            faerunList = faerunFile.readlines()
            loc = faerunList[randint(0,len(faerunList)-1)]
            loc = loc.replace('\n', '')
            self.location = loc
            return self.location
        locations = ['coast','mountains','swamp','underdark','grasslands','jungle','city','settlement','fort','forest',
                     'tundra','hills','lowlands','steppe','marsh','meadow']
        if self.conditionType == "cold":
            locations.extend(['icelands'])
        elif self.conditionType == "hot":
            locations.extend(['desert'])
        self.location = locations[randint(0,len(locations)-1)]
        return self.location

    def getNearbyFeatures(self):
        if self.location == 'coast':
            self.nearbyFeatures = ['rocky shoals','tide pools','docks','creaking galleons','shipwreck',
                                   'enormous statue']
        elif self.location == 'mountains':
            self.nearbyFeatures = ['rocky cliffs','cliff dwelling','rocky temple','mines','craggy rocks']
        elif self.location == 'swamp':
            self.nearbyFeatures = ['thick muddy waters','looming swamp trees']
        elif self.location == 'underdark':
            self.nearbyFeatures = ['surface above']
        elif self.location == 'grasslands':
            self.nearbyFeatures = ['grassy plains','vineyard','catfolk village','savannah','lone acacia tree']
        elif self.location == 'jungle':
            self.nearbyFeatures = ['leafy canopy','enormous ant hills','broad fronds','stagnant water','leafy temple',
                                   'makeshift dwellings']
        elif self.location == 'city':
            self.nearbyFeatures = ['huddled rooftops','dirty streets','crowded streets','empty buildings',
                                   'festive buildings','bustling vendor stands','numerous carriages','guild halls',
                                   'temples','royal castle','nobles\' homes','slums']
        elif self.location == 'settlement':
            self.nearbyFeatures = ['makeshift structures',"woodcutter's shop",'stables','livestock pens',
                                   'food storage','church','adjacent woods','general store']
        elif self.location == 'fort':
            self.nearbyFeatures = ['barracks',"captain's abode",'protective wall','map room','stables','war machines',
                                   'weapons store',"raven's roost",'lookout tower']
        elif self.location == 'forest':
            self.nearbyFeatures = ['enormous tree trunks','stone menhir','dry pines','proud trees']
        elif self.location == 'tundra':
            self.nearbyFeatures = ['stunted trees','matted grass']
        elif self.location == 'hills':
            self.nearbyFeatures = ['rocky deposits','rolling hilltops','emerald green grass',
                                   'dry mustard-colored weeds','ancient ruins']
        elif self.location == 'lowlands':
            self.nearbyFeatures = ['peat bogs','sucking mud','sickly grass','verdant pastures']
        elif self.location == 'steppe':
            self.nearbyFeatures = ['shrubs','briar','pebbly ground']
        elif self.location == 'marsh':
            self.nearbyFeatures = ['reeds','foul water','lonely hut','menhir','druid temple','hatchery', 'dam',
                                   'coven house','manticore den', 'lizardfolk village',"green hag's cabin"]
        elif self.location == 'meadow':
            self.nearbyFeatures = ['wildflowers','lush grasses','hollow blackened trees','stables','farm house',
                                   'windmill','cottage']
        elif self.location == 'icelands':
            self.nearbyFeatures = ['endless hills of snow','snowy wastelands','unforgiving drifts',
                                   'mountains of white','lone dwelling']
        elif self.location == 'desert':
            self.nearbyFeatures = ['vast expanse of sandy dunes','menacing cacti','oasis','coconut palms',
                                   'flat red rocks','mesa','thorny shrubs','tumbleweed-strewn desert floor']
        else:
            self.nearbyFeatures = ['nearby features']

        self.nearbyFeature = self.nearbyFeatures[randint(0,len(self.nearbyFeatures)-1)]
