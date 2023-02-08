import pygame
import numpy as np
import pandas as pd
import time
import market

#pd.Timestamp.now().round(freq='min')

mymarket = market.Supermarket()
mymarket.init_layout()
mymarket.add_customers(23)

df = mymarket.get_customer_df()
df.sort_values(by=["global time"], inplace = True)

df[df["id"]==1]



pygame.init()
display = pygame.display.set_mode((600, 400))
clock = pygame.time.Clock()
theFont = pygame.font.Font(None,32)

layout = mymarket.layout
surf = pygame.surfarray.make_surface(layout.transpose(1, 0, 2))

running = True

t_counter = 0


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    frame = df[df["global time"]==t_counter]
    if not frame.empty:
        for i in range(len(frame)):
            customer = frame.iloc[i]
            c_id = customer["id"]
            sec_id = customer["sectionid"]
            pos_id = mymarket.cust_in_section[sec_id]
            location = mymarket.locations[str(sec_id)][pos_id]
            mymarket.draw_circle(location)
            mymarket.increment(sec_id)
            c_table = df[df["id"] == c_id]
            c_table[c_table["global time"] == t_counter]["visited"] == True
            c_table[c_table["visited"] == "True"] 



    layout = mymarket.layout
    surf = pygame.surfarray.make_surface(layout.transpose(1, 0, 2))
    display.blit(surf, (0, 0))
    clock.tick(1)
    t_counter += 1
    theTime = time.strftime("%H:%M:%S", time.localtime())
    timeText = theFont.render(str(theTime), True,(0, 0, 0),(176, 226, 255))
    display.blit(timeText, (500,370))
    pygame.display.update()



pygame.quit()




