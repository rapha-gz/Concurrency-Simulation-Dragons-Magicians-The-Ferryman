import threading as th
from threading import Thread, Semaphore
import random
from time import sleep

MAX_DRAGONS_ISLAND = 2
N_NOVICES = 10
MAX_MAGES_BOAT = 5
MAX_MAGES_ISLAND = 20
global MAX_MAGES_ISLAND_CHANGING
MAX_MAGES_ISLAND_CHANGING = MAX_MAGES_ISLAND

class Island:
    def __init__(self):
        self.magicians = []
        self.magicians_entering = 0
        self.dragons = 0
        self.special_dragons = 0
        self.semaphore_dragons_capacity = Semaphore(MAX_DRAGONS_ISLAND)
        self.semaphore_special_dragons = Semaphore(0)
        self.semaphore_dragon = Semaphore(0)
        self.semaphore_dragons = Semaphore(0)

    def fly_in_island(self,dragon):
        global MAX_MAGES_ISLAND_CHANGING
        if self.dragons + self.special_dragons >= MAX_DRAGONS_ISLAND:
            print(f"++++++++++++++++++++++The Dragon Island is full of dragons for {dragon.name}.")
        self.semaphore_dragons_capacity.acquire()
        if dragon.name == "Smoug" or dragon.name == "Drogon":
            self.special_dragons += 1
            MAX_MAGES_ISLAND_CHANGING = 0
            print(f"++++++++++++++++++++++{dragon.name} changes the number of people allowed****People Inside Max: {MAX_MAGES_ISLAND_CHANGING}, Actual: {self.magicians_entering+ len(self.magicians)}****")
            while self.magicians_entering + len(self.magicians) != 0:
                print(f"++++++++++++++++++++++{dragon.name} is wating to enter the Dragon Island.")
                self.semaphore_special_dragons.acquire()
        else:
            self.dragons += 1
            if self.special_dragons > 0:
                if self.magicians_entering + len(self.magicians) != 0:
                    print(f"++++++++++++++++++++++{dragon.name} is wating to enter the Dragon Island.")
                    self.semaphore_special_dragons.acquire()      

            elif self.dragons == 2:
                MAX_MAGES_ISLAND_CHANGING = MAX_MAGES_ISLAND/4
                print(f"++++++++++++++++++++++{dragon.name} changes the number of people allowed****People Inside Max: {MAX_MAGES_ISLAND_CHANGING}, Actual: {self.magicians_entering + len(self.magicians) }****")
                while self.magicians_entering + len(self.magicians) > MAX_MAGES_ISLAND_CHANGING:
                    print(f"++++++++++++++++++++++{dragon.name} is waiting to enter the Dragon Island.")
                    self.semaphore_dragons.acquire()

            elif self.dragons > 2:
                print(f"++++++++++++++++++++++{dragon.name} changes the number of people allowed****People Inside Max: {MAX_MAGES_ISLAND_CHANGING}, Actual: {self.magicians_entering + len(self.magicians) }****")
                while self.magicians_entering + len(self.magicians) > MAX_MAGES_ISLAND_CHANGING:
                    print(f"++++++++++++++++++++++{dragon.name} is waiting to enter the Dragon Island.")
                    self.semaphore_dragons.acquire()
                    
            else:
                MAX_MAGES_ISLAND_CHANGING = MAX_MAGES_ISLAND/2
                print(f"++++++++++++++++++++++{dragon.name} changes the number of people allowed****People Inside Max: {MAX_MAGES_ISLAND_CHANGING}, Actual: {self.magicians_entering + len(self.magicians) }****")
                while self.magicians_entering + len(self.magicians)  > (MAX_MAGES_ISLAND/2):
                    self.semaphore_dragon.acquire()
        sleep(0.01)
        print(f"++++++++++++++++++++++{dragon.name} INSIDE. People allowed on the Dragon Island: {MAX_MAGES_ISLAND_CHANGING}")

    def fly_out_island(self,dragon):
        global MAX_MAGES_ISLAND_CHANGING
        if dragon.name == "Smoug" or dragon.name == "Drogon":
            self.special_dragons -= 1
            if self.special_dragons  > 0:
                MAX_MAGES_ISLAND_CHANGING = 0
            elif self.special_dragons  == 0 and self.dragons == 0:
                MAX_MAGES_ISLAND_CHANGING = MAX_MAGES_ISLAND 
                self.semaphore_special_dragons.release()
            elif self.special_dragons  == 0 and self.dragons >= 2:
                MAX_MAGES_ISLAND_CHANGING = MAX_MAGES_ISLAND/4
            elif self.special_dragons  == 0 and self.dragons == 1:
                MAX_MAGES_ISLAND_CHANGING = MAX_MAGES_ISLAND/2
                self.semaphore_dragon.release()
            print(f">>>>>>>>>>>>>>>>>>>>>>{dragon.name} left the Dragon Island. ****People Inside Max: {MAX_MAGES_ISLAND_CHANGING}, Actual: {self.magicians_entering + len(self.magicians) }****")
                
        else:
            self.dragons -= 1
            if self.special_dragons > 0:
                MAX_MAGES_ISLAND_CHANGING = 0
            elif self.dragons  > 1:
                MAX_MAGES_ISLAND_CHANGING = MAX_MAGES_ISLAND/4
            elif self.dragons  == 1:
                MAX_MAGES_ISLAND_CHANGING = MAX_MAGES_ISLAND/2
                self.semaphore_dragons.release()
            elif self.dragons  == 0:
                MAX_MAGES_ISLAND_CHANGING = MAX_MAGES_ISLAND 
                self.semaphore_dragon.release()
            print(f">>>>>>>>>>>>>>>>>>>>>>{dragon.name} left the Dragon Island. ****People Inside Max: {MAX_MAGES_ISLAND_CHANGING}, Actual: {self.magicians_entering + len(self.magicians) }****")
        self.semaphore_dragons_capacity.release()

    def magician_out(self,magician):
        self.magicians.remove(magician)
        if len(self.magicians) == 0:
            if self.special_dragons + self.dragons > 1:
                for i in range(self.special_dragons + self.dragons):
                    self.semaphore_special_dragons.release()
                    sleep(0.005) #for allowing the semaphore to restore, if not in the case that there is a normal dragon waiting
                    #to enter to the island, only the special dragon would enter, which is the first in the semaphore
            elif self.special_dragons == 1:
                self.semaphore_special_dragons.release()
            else:
                self.semaphore_special_dragons.release()
        elif (len(self.magicians) <= (MAX_MAGES_ISLAND/2) and self.dragons == 1):
            self.semaphore_dragon.release()
        elif (len(self.magicians) <= (MAX_MAGES_ISLAND/4) and self.dragons >= 2):
            self.semaphore_dragons.release()

class Dragon(Thread):
    def __init__(self, name,island,ferry):
        Thread.__init__(self)
        self.name = name
        self.island = island
        self.ferry = ferry
        
    def run(self):
        i = 0
        while(N_NOVICES > self.ferry.travels and i < 3):
            print(f"++++++++++++++++++++++{self.name} is flying.")
            sleep(random.random())
            self.island.fly_in_island(self)
            sleep(random.random())
            print(f"++++++++++++++++++++++{self.name} is about to leave the Dragon Island.")
            self.island.fly_out_island(self)
            sleep(5)
            i += 1

class Magician(Thread):
    def __init__(self,name,island,ferry,semaphore):
        Thread.__init__(self)
        self.name = name
        self.island = island
        self.place = -1 #place = -1 Magicians City, place = 0 Ferry, place = 1 Island
        self.direction = 1
        self.ferry = ferry
        self.semaphore_ferry_magician = semaphore

    def run(self):
        print(f"{self.name} is at the pier waiting to enter the boat to go to the Dragon Island.")
        self.ferry.embark(self,self.direction,-self.direction)
        while self.place != 1:
            self.semaphore_ferry_magician.acquire()
        print(f"The {self.name} is looking for scales.")
        sleep(random.random())
        print(f"The {self.name} has finished looking.")
        self.ferry.magicians_back +=1
        self.direction = -1
        self.ferry.embark(self,self.direction,-self.direction)
        self.ferry.travels += 1

class Ferryman(Thread):
    def __init__(self,name,island,semaphore):
        Thread.__init__(self)
        self.name = name
        self.direction = 1 #     1 = direction to the Island and -1 direction to the Magicians City
        self.place = -1 #place = -1 Magicians City, place = 0 Water, place = 1 Island
        self.magicians = []
        self.magicians_back = 0
        self.travels = 0
        self.island = island
        self.semaphore_ferry = Semaphore(100)
        self.semaphore_ferry_back = Semaphore(100)
        self.semaphore_ferry_magician = semaphore
        self.gate = False
    
    def embark(self,magician,direction,other_direction):
            if magician.direction == -1:
                self.semaphore_ferry_back.acquire()
                print(f"{magician.name} is on the boat at the shore waiting to go back home.")
                self.island.magician_out(magician)
            else:                   
                while (len(self.magicians) == MAX_MAGES_BOAT or self.direction == other_direction or self.gate == False or self.place != magician.place):
                    self.semaphore_ferry.acquire()
                if self.island.special_dragons > 0:
                    self.semaphore_ferry.acquire()
                elif (len(self.island.magicians) + self.island.magicians_entering >= MAX_MAGES_ISLAND_CHANGING):
                    self.semaphore_ferry.acquire()
                self.island.magicians_entering += 1   
                print(f"{magician.name} is on the boat at the pier.")
            magician.place = 0
            self.magicians.append(magician)
    
    def disembark(self):
        if self.direction == -1:
            for i in range(len(self.magicians)):
                self.magicians[i].place = -1

            while len(self.magicians) > 0:
                self.magicians.pop()
                self.semaphore_ferry_magician.release()
        else:
            for i in range(len(self.magicians)):    
                self.magicians[i].place = 1
            while len(self.magicians) > 0:
                self.island.magicians.append(self.magicians.pop())
                self.semaphore_ferry_magician.release()
        self.semaphore_ferry.release()

    def run(self):
        while N_NOVICES > self.travels:
            self.gate = False
            self.direction = 1
            print(f"[{self.name}] is at the pier of the Magicians City. GATES OPENED.")
            self.gate = True
            for i in range(int(MAX_MAGES_ISLAND_CHANGING-len(self.island.magicians)-self.island.magicians_entering)):
                if (self.island.special_dragons == 0):
                    self.semaphore_ferry.release()
                    sleep(0.005)
            sleep(0.100)
            print("GATES CLOSED.")
            print(f"		 ****Max People Inside the Dragon Island: {MAX_MAGES_ISLAND_CHANGING}, Actual: {self.island.magicians_entering + len(self.island.magicians)}****") 
            self.gate = False
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
            self.gate = True
            print(f"		 ****Max People Inside the Dragon Island: {MAX_MAGES_ISLAND_CHANGING}, Actual: {len(self.island.magicians)}****")
            for i in range(self.magicians_back):
                self.semaphore_ferry_back.release()
                self.magicians_back = 0 
            sleep(0.100)
            print(f"		 ****Max People Inside the Dragon Island: {MAX_MAGES_ISLAND_CHANGING}, Actual: {len(self.island.magicians)}****")
            print("GATES CLOSED.")
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
    Dragon_Island = Island()
    semaphore_magicians_ferry = Semaphore(100)
    Charon = Ferryman("Charon",Dragon_Island,semaphore_magicians_ferry)
    Dragon("Dragon 1",Dragon_Island,Charon).start()
    Dragon("Dragon 2",Dragon_Island,Charon).start()
    Dragon("Dragon 3",Dragon_Island,Charon).start()
    Dragon("Smoug",Dragon_Island,Charon).start()
    Dragon("Drogon",Dragon_Island,Charon).start()
    Charon.start()
    for i in range(N_NOVICES):
        Magician("Magician "+str(i+1),Dragon_Island,Charon,semaphore_magicians_ferry).start()
        sleep(0.02)
    
if __name__ == "__main__":
    main()