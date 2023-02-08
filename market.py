import numpy as np
import pandas as pd
from PIL import Image


ENTRANCE = [(370, 130 - i*30) for i in range(5)]
FRUITS = [(55 + i*30, 40) for i in range(7)]
DAIRY  = [(55 + 30*i, 140) for i in range(7)]
SPICES  = [(55 + 30*i, 240) for i in range(7)]
DRINKS = [(100, 365 + 30*i) for i in range(7)]
checkout_pos1 = [(325 - 30*i, 415) for i in range(7)]
checkout_pos2 = [(325 - 30*i, 505) for i in range(7)]
CHECKOUT = np.hstack((checkout_pos1, checkout_pos2)).reshape((14, 2))

ENCODING = {"0":"checkout", 
            "1":"dairy", 
            "2":"drinks",
            "3":"fruit",
            "4":"spices",
            "5":"entrance"}


class Customer:
    def __init__(self, id, section=5):
        self.id = id
        self.section = ENCODING[str(section)]
        self.sectionid = section
        self.section_vec = np.zeros(6)
        self.section_vec[section] = 1
        self.sequence_section = []
        self.sequence_section_id = []
        self._sequence_time = []
        self.sequence_cum_time = []
        self.time = np.random.randint(1, 10)
        self.transition = np.array([[0.        , 0.        , 0.        , 0.        , 0.        , 0.        ],
                                    [0.29214759, 0.        , 0.24741722, 0.21854305, 0.24189215, 0.        ],
                                    [0.43200286, 0.02879721, 0.        , 0.26149656, 0.27770337, 0.        ],
                                    [0.38665204, 0.28835253, 0.16098007, 0.        , 0.16401536, 0.        ],
                                    [0.18150729, 0.35844056, 0.28991579, 0.17013637, 0.        , 0.        ],
                                    [0.        , 0.2952041 , 0.14514977, 0.36420922, 0.19543691, 0.        ]])
        self.checkedout = False
        self.propagate()


    def next_section(self):
        if not self.checkedout:
            index = np.random.choice(np.arange(6), replace=True, p=np.dot(self.section_vec, self.transition))
            self.section = ENCODING[str(index)]
            self.sectionid = index
            self.section_vec = np.zeros(6)
            self.section_vec[index] = 1
            self.time = np.random.poisson(lam=2) + 1
            if index == 0:
                self.checkedout = True
    

    def propagate(self):
        while not self.checkedout:
            self.sequence_section.append(self.section)
            self.sequence_section_id.append(self.sectionid)
            self._sequence_time.append(self.time)
            self.sequence_cum_time.append(sum(self._sequence_time))
            self.next_section()
        self.sequence_section.append(self.section)
        self.sequence_section_id.append(self.sectionid)
        self._sequence_time.append(self.time)
        self.sequence_cum_time.append(sum(self._sequence_time))


    def to_df(self):
        return pd.DataFrame({"id":                 self.id, 
                             "section":            self.sequence_section,
                             "sectionid":          self.sequence_section_id,
                             "time spend in min":  self._sequence_time,
                             "global time":        self.sequence_cum_time,
                             "visited":            False})
        



class Supermarket:

    def __init__(self):
        self.cust_in_section = 6*[0]
        self.customers = []
        self.layout = np.zeros((120, 180))
        self.locations = {}


    def add_customers(self, n):
        for i in range(n):
            self.customers.append(Customer(i))
        self._initialize_locations(n)
        
    
    def _initialize_locations(self, n):
        ENTRANCE = [(370, 130 - i*30) for i in range(n)]
        FRUITS = [(55 + i*30, 40) for i in range(n)]
        DAIRY  = [(55 + 30*i, 140) for i in range(n)]
        SPICES  = [(55 + 30*i, 240) for i in range(n)]
        DRINKS = [(100, 365 + 30*i) for i in range(n)]
        checkout_pos1 = [(325 - 30*i, 415) for i in range(n)]
        checkout_pos2 = [(325 - 30*i, 505) for i in range(n)]
        CHECKOUT = np.hstack((checkout_pos1, checkout_pos2)).reshape((2*n, 2))
        self.locations = {"0":CHECKOUT,
                          "1":DAIRY,
                          "2":DRINKS,
                          "3":FRUITS,
                          "4":SPICES,
                          "5":ENTRANCE}


    def get_customer_df(self):
        return pd.concat([cust.to_df() for cust in self.customers], axis=0)


    def increment(self, section):
        self.cust_in_section[section] += 1


    def decrease(self, section):
        self.cust_in_section[section] -= 1


    def draw_circle(self, pos):
        posx, posy = pos
        for i in range(90):
            phi = i/360*2*np.pi
            x = int(np.floor(10*np.cos(phi)))
            y = int(np.floor(10*np.sin(phi)))
            self.layout[posx - x:posx + x, posy - y:posy + y] = 255, 0, 0


    def undraw_circle(self, pos):
        posx, posy = pos
        for i in range(90):
            phi = i/360*2*np.pi
            x = int(np.floor(10*np.cos(phi)))
            y = int(np.floor(10*np.sin(phi)))
            self.layout[posx - x:posx + x, posy - y:posy + y] = 176,226,255


    def init_layout(self):
        self.layout = np.zeros((400, 600, 3), dtype="uint8")
        self.layout[:, :] = 176,226,255
        self.layout[40:250, 60:100] = 25,25,112    # LEFT SHELF
        self.layout[40:250, 160:200] = 25,25,112   # MIDDLE SHELF
        self.layout[40:190, 260:300] = 25,25,112   # RIGHT SHELF
        self.layout[40:80, 350:560] = 25,25,112    # UPPER RIGHT SHELF
        self.layout[230:340, 350:390] = 0, 0, 0    # LEFT CHECKOUT
        self.layout[230:340, 440:480] = 0, 0, 0    # MIDDLE CHECKOUT
        self.layout[230:340, 530:570] = 0, 0, 0    # RIGHT CHECKOUT
        self.layout[335:340, :350] = 0, 0, 0       # BORDER
        self.layout[335:340, 570:] = 0, 0, 0       # BORDER
        self.layout[:5, :] = 0, 0, 0               # BORDER
        self.layout[-5:, :] = 0, 0, 0              # BORDER
        self.layout[:335, :5] = 0, 0, 0            # BORDER
        self.layout[:, -5:] = 0, 0, 0              # BORDER
        self.layout[335:340, 100:160] = 176, 226, 255     # OPENING


    def __repr__(self):
        return Image.fromarray(self.layout, 'RGB')

    