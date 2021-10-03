import pygame
from datetime import datetime
pygame.init()
displaySize = pygame.display.Info()
size_w_minus = displaySize.current_w//91
size_h_minus = displaySize.current_h//10
size_w=displaySize.current_w
size_h=displaySize.current_h
size=[size_w,size_h]


sideBar_w = size_w//11 
sideBar_h = size_h - size_h//18
sideBarRctWStart = 20+sideBar_w//7
sideBarRctHStart = 20+sideBar_h//15
sideBarRctWE = sideBar_w/1.4
sideBarRctHghtE = sideBar_h//8 
sideBarRWdth = sideBarRctWE-sideBarRctWStart
print(size_w/648)
print(size_h/70)
print(int(size_w/2.11),int(size_h/2.55)) 






#512x512: [int(size_w/2.66),int(size_h/1.5)]
#350x350: [int(size_w/3.90),int(size_h/2.19)]
#256x256: [int(size_w/5.33),int(size_h/3)]
#128x128: [int(size_w/10.6),int(size_h/6)]
#96x96: [int(size_w/14.22),int(size_h/8)]
#64x64: [int(size_w/21.34),int(size_h/12)]
#54x54: [int(size_w/25.29),int(size_h/14.22)]
#32x32: [int(size_w/42.68),int(size_h/24)]

