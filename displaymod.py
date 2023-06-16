import pygame
import time

def main(*args):

    #print(args)

    if len(args) > 0:
        reg = args[0]

    if len(args) > 1:
        args = args[1]

    if args:
        match args[2][1]:

            case 0:
                pygame.init()

            case 1:
                reg['esp']= pygame.display.set_mode((args[3][1], args[4][1]))

            case 2:
                reg['esp'] = (args[3][1],args[4][1],args[5][1])
            
            case 3:
                pygame.draw.rect(args[3][1], args[4][1], pygame.Rect(args[5][1], args[6][1], args[7][1], args[8][1]),  args[9][1]) #surface ,color, rect dim 1 2 3 4, ??
                
            case 4:
                pygame.display.flip()
                time.sleep(10)
            


    return reg