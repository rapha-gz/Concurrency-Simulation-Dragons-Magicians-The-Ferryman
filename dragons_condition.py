import threading as th
from threading import Thread, Condition
import random
from time import sleep

MAX_DRAGONS_ISLAND = 2
N_NOVICES = 10
MAX_MAGES_BOAT = 5
MAX_MAGES_ISLAND = 20

class Island:
    def __init__(self):
        self.magicians = []
        self.magicians_entering = 0
        self.dragons = 0
        self.special_dragons = 0
        self.max_mages_island_changing = MAX_MAGES_ISLAND
        self.condition_dragons_capacity = Condition()
        self.condition_special_dragons = Condition()
        self.condition_dragon = Condition()
        self.condition_dragons = Condition()
        

    def fly_in_island(self,dragon):
        with self.condition_dragons_capacity:
            while self.dragons + self.special_dragons >= MAX_DRAGONS_ISLAND:
                print(f"++++++++++++++++++++++The Dragon Island is full of dragons for {dragon.name}.")
                self.condition_dragons_capacity.wait()

        if dragon.name == "Smoug" or dragon.name == "Drogon":
            self.special_dragons += 1
            with self.condition_special_dragons:
                self.max_mages_island_changing = 0
                print(f"++++++++++++++++++++++{dragon.name} changes the number of people allowed****People Inside Max: {self.max_mages_island_changing}, Actual: {self.magicians_entering+ len(self.magicians)}****")
                while self.magicians_entering + len(self.magicians) != 0:
                    print(f"++++++++++++++++++++++{dragon.name} is wating to enter the Dragon Island.")
                    self.condition_special_dragons.wait()
        else:
            self.dragons += 1
            if self.special_dragons > 0:
                with self.condition_special_dragons:
                    while self.magicians_entering + len(self.magicians) != 0:
                        print(f"++++++++++++++++++++++{dragon.name} is wating to enter the Dragon Island.")
                        self.condition_special_dragons.wait()

            elif self.dragons == 2:
                with self.condition_dragons:
                    self.max_mages_island_changing = MAX_MAGES_ISLAND/4
                    print(f"++++++++++++++++++++++{dragon.name} changes the number of people allowed****People Inside Max: {self.max_mages_island_changing}, Actual: {self.magicians_entering + len(self.magicians) }****")
                    while self.magicians_entering + len(self.magicians) > self.max_mages_island_changing:
                        self.condition_dragons.wait()

            elif self.dragons > 2:
                with self.condition_dragons:
                    print(f"++++++++++++++++++++++{dragon.name} changes the number of people allowed****People Inside Max: {self.max_mages_island_changing}, Actual: {self.magicians_entering + len(self.magicians) }****")
                    while self.magicians_entering + len(self.magicians) > self.max_mages_island_changing:
                        print(f"{dragon.name} is waiting to enter the Dragon Island.")
                        self.condition_dragons.wait()
                    
            else:
                with self.condition_dragon:
                    self.max_mages_island_changing = MAX_MAGES_ISLAND/2
                    print(f"++++++++++++++++++++++{dragon.name} changes the number of people allowed****People Inside Max: {self.max_mages_island_changing}, Actual: {self.magicians_entering + len(self.magicians) }****")
                    while self.magicians_entering + len(self.magicians)  > (MAX_MAGES_ISLAND/2):
                        self.condition_dragon.wait()
        print(f"++++++++++++++++++++++{dragon.name} INSIDE. People allowed on the Dragon Island: {self.max_mages_island_changing}")

    def fly_out_island(self,dragon):
        with self.condition_dragons_capacity:
            if dragon.name == "Smoug" or dragon.name == "Drogon":
                self.special_dragons -= 1
                if self.special_dragons  > 0:
                    self.max_mages_island_changing = 0
                elif self.special_dragons  == 0 and self.dragons == 0:
                    self.max_mages_island_changing = MAX_MAGES_ISLAND 
                elif self.special_dragons  == 0 and self.dragons > 1:
                    self.max_mages_island_changing = MAX_MAGES_ISLAND/4
                elif self.special_dragons  == 0 and self.dragons == 1:
                    self.max_mages_island_changing = MAX_MAGES_ISLAND/2                    
            else:
                self.dragons -= 1
                if self.special_dragons > 0:
                    self.max_mages_island_changing = 0
                elif self.dragons  > 1:
                    self.max_mages_island_changing = MAX_MAGES_ISLAND/4
                elif self.dragons  == 1:
                    self.max_mages_island_changing = MAX_MAGES_ISLAND/2
                elif self.dragons  == 0:
                    self.max_mages_island_changing = MAX_MAGES_ISLAND  
            print(f">>>>>>>>>>>>>>>>>>>>>>{dragon.name} left the Dragon Island. ****People Inside Max: {self.max_mages_island_changing}, Actual: {self.magicians_entering + len(self.magicians) }****")
            self.condition_dragons_capacity.notify_all()

    def magician_out(self,magician):
        self.magicians.remove(magician)
        if len(self.magicians) == 0:
            with self.condition_special_dragons:
                self.condition_special_dragons.notify_all()
        if len(self.magicians) <= (MAX_MAGES_ISLAND/2):
            with self.condition_dragon:    
                self.condition_dragon.notify_all()
        if len(self.magicians) <= (MAX_MAGES_ISLAND/4):
            with self.condition_dragons:
                self.condition_dragons.notify_all()

class Dragon(Thread):
    def __init__(self, name,island,ferry):
        Thread.__init__(self)
        self.name = name
        self.island = island
        self.ferry = ferry
        
    def run(self):
        for i in range(3):
            print(f"++++++++++++++++++++++{self.name} is flying.")
            sleep(random.random())
            self.island.fly_in_island(self)
            sleep(random.random())
            print(f"++++++++++++++++++++++{self.name} is about to leave the Dragon Island.")
            self.island.fly_out_island(self)

class Magician(Thread):
    def __init__(self,name,island,ferry,condition):
        Thread.__init__(self)
        self.name = name
        self.island = island
        self.place = -1 #place = -1 Magicians City, place = 0 Ferry, place = 1 Island
        self.direction = 1
        self.ferry = ferry
        self.condition_ferry_magician = condition

    def run(self):
        sleep(random.random())
        print(f"{self.name} is at the pier waiting to enter the boat to go to the Dragon Island.")
        self.ferry.embark(self,self.direction,-self.direction)
        print(f"{self.name} is on the boat at the pier.")
        with self.condition_ferry_magician:
            while self.place != 1:
                self.condition_ferry_magician.wait()
        print(f"The {self.name} is looking for scales.")
        sleep(random.random())
        print(f"The {self.name} has finished looking.")
        self.direction = -1
        self.ferry.embark(self,self.direction,-self.direction)

class Ferryman(Thread):
    def __init__(self,name,island,condition):
        Thread.__init__(self)
        self.name = name
        self.direction = 1 #     1 = direction to the Island and -1 direction to the Magicians City
        self.place = -1 #place = -1 Magicians City, place = 0 Water, place = 1 Island
        self.magicians = []
        self.travels = 0
        self.island = island
        self.condition_ferry = Condition()
        self.condition_ferry_magician = condition
        self.gate = False

    def embark(self,magician,direction,other_direction):
            with self.condition_ferry:
                if magician.direction == -1:
                    while(self.island.magicians_entering == MAX_MAGES_BOAT or self.direction == other_direction or self.gate == False 
                        or self.place != magician.place):
                        self.condition_ferry.wait()

                else:
                    while(len(self.magicians) == MAX_MAGES_BOAT or self.direction == other_direction or self.gate == False 
                        or self.place != magician.place or self.island.special_dragons != 0 
                        or (self.island.dragons == 1 and (len(self.island.magicians) + self.island.magicians_entering >= MAX_MAGES_ISLAND/2))
                        or (self.island.dragons > 1 and (len(self.island.magicians) + self.island.magicians_entering >= MAX_MAGES_ISLAND/4))):
                        self.condition_ferry.wait()
                     
            if direction == -1:
                print(f"{magician.name} is on the boat at the shore waiting to go back home.")
                self.island.magician_out(magician)
                    
            else:
                self.island.magicians_entering += 1   
            magician.place = 0
            self.magicians.append(magician)

    def disembark(self):
        with self.condition_ferry:
            with self.condition_ferry_magician:
                if self.direction == -1:
                    for i in range(len(self.magicians)):
                        self.magicians[i].place = -1

                    while len(self.magicians) > 0:
                        self.magicians.pop()
                        self.travels += 1
                        self.condition_ferry_magician.notify_all()
                else:
                    for i in range(len(self.magicians)):    
                        self.magicians[i].place = 1
                    while len(self.magicians) > 0:
                        self.island.magicians.append(self.magicians.pop())
                        self.condition_ferry_magician.notify_all()
            self.condition_ferry.notify_all()

    def run(self):
        while N_NOVICES > self.travels:
            self.gate = False
            self.direction = 1
            print(f"[{self.name}] is at the pier of the Magicians City. GATES OPENED.")
            with self.condition_ferry:
                self.gate = True
                self.condition_ferry.notify_all()
            sleep(0.100)
            with self.condition_ferry:
                print("GATES CLOSED.")
                self.gate = False
                print(f"		 ****Max People Inside the Dragon Island: {self.island.max_mages_island_changing}, Actual: {self.island.magicians_entering + len(self.island.magicians)}****") 
                self.place = 0
            print(f"[{self.name}] is leaving the Magicians City with the magicians on board.")
            print(f"[{self.name}] is now on the way to the Dragon Island.")
            sleep(0.200)
            self.place = 1
            print(f"[{self.name}] is now in the Dragon Island waiting for all the magicians to disembark.")
            self.disembark()
            print("All magicians from the city have disembarked.")
            self.island.magicians_entering = 0
            self.direction = -1
            print(f"[{self.name}] is now in the Dragon Island waiting for magicians to embark. GATES OPENED")
            with self.condition_ferry:
                self.gate = True
                self.condition_ferry.notify_all()
            sleep(0.100)
            with self.condition_ferry:
                print("GATES CLOSED.")
                self.gate = False
                print(f"		 ****Max People Inside the Dragon Island: {self.island.max_mages_island_changing}, Actual: {len(self.island.magicians)}****")
                self.place = 0
            print(f"[{self.name}] is leaving the Dragon Island with the magicians on board.")
            sleep(0.200)
            print(f"[{self.name}] is arriving to the Magicians City.")   
            self.place = -1
            print(f"[{self.name}] is now on the Magicians City waiting for the magicians to disembark.")
            self.disembark()
            if N_NOVICES - self.travels <= 0:
                print("--------Magicians Left--------:0")
            else:
                print("--------Magicians Left--------:",N_NOVICES-self.travels)

def main():
    condition_magicians_ferry = Condition()
    Dragon_Island = Island()
    Charon = Ferryman("Charon",Dragon_Island,condition_magicians_ferry)
    Dragon("Fujur",Dragon_Island,Charon).start()
    Dragon("Saphira",Dragon_Island,Charon).start()
    Dragon("Toothless",Dragon_Island,Charon).start()
    Dragon("Smoug",Dragon_Island,Charon).start()
    Dragon("Drogon",Dragon_Island,Charon).start()
    Charon.start()
    for i in range(N_NOVICES):
        Magician("Magician "+str(i+1),Dragon_Island,Charon,condition_magicians_ferry).start()
        sleep(0.02)
    Charon.join()
    return
    
if __name__ == "__main__":
    main()