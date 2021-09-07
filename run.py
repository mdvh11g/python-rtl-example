#!/usr/bin/env python3

import cv2
import Filters

filter = Filters.Search('Position',0x10,0x20)
                             # Mask
                             # Round, 
                             # Value, 
                             # Position,  %

filter.SelfTest()
#filter.SelfTest(_Trace = 'True')


#img = cv2.imread('1.jpg',0)
#img = filter.UpdateImage(img)
#cv2.imwrite('out.png',img)
