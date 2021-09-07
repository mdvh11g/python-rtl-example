#!/usr/bin/env python3

import os
import cv2
import numpy as np
import pyverilator

class Search():

  '''
  алгоритм поиска, который находит позицию целевого значения в массиве
  '''

  def __init__(self, mode='Mask', omega=0x08, epsilon = 0x24):
  
      self.Mask = 0xff 
      self.sim = pyverilator.PyVerilator.build('Cap.v')
      
      self.PIXEL_SIZE = 3  
      self.PIXEL_NUM = 4   
      self.sim.io.omega = omega
      self.sim.io.epsilon = epsilon  
      if   mode == 'Mask': self.sim.io.mode = 0x0
      elif mode == 'Round': self.sim.io.mode = 0x1
      elif mode == 'Value': self.sim.io.mode = 0x2
      elif mode == 'Position': self.sim.io.mode = 0x3
      else:self.sim.io.mode = 0x0 
      self.reset()
                              
  def trace(self):
      self.sim.start_gtkwave()

  def tact(self):
      self.sim.io.clk = 0
      self.sim.io.clk = 1
  
  def reset(self):
      self.sim.io.areset = 0; self.tact()
      self.sim.io.areset = 1  
  
  def clear(self):
      self.sim.io.flow = 0
      self.sim.io.enable = 1
      self.sim.io.clear = 1
      self.tact()
      self.sim.io.enable = 0  
      self.sim.io.clear = 1
    
  def _input(self,ee):
      self.sim.io.flow = int(ee)
      self.sim.io.enable = 1
      self.sim.io.clear = 0
      self.tact()
      self.sim.io.enable = 0    
       
  def _H_print(self,img):    
      for i in range (len(img)):
        for j in range (len(img[i])):
          if j==(len(img[i])-1):
            print ('0x%03x'%img[i][j])
          elif j==0:  
            print ('  0x%03x'%img[i][j],end=' ')
          else:  
            print ('0x%03x'%img[i][j],end=' ')     

  def UpdateImage(self,img):   
      self.clear()      
      ee = 0
      ff = 0
      vv = []      
      for i in range (len(img)):
        hh = []
        for j in range (1,len(img[0])+1):
          ee += img[i][j-1]
          if not (j%self.PIXEL_NUM): 
            self._input(ee)  
            if (self.sim.io.ready):   
              ff = self.sim.io.result
            for p in range (self.PIXEL_NUM):
                hh.append(self.Mask&ff)
                ff = ff >> 2**self.PIXEL_SIZE 
          ee = ee       << 2**self.PIXEL_SIZE  #_______________
        vv.append(hh)  
      return np.array(vv)

  def SelfTest(self,_Trace='False'):
      img = [[0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08],
             [0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17, 0x18],
             [0x21, 0x22, 0x23, 0x24, 0x25, 0x26, 0x27, 0x28]]   
      print('Self Test Input:')       
      self._H_print(img)     
      if (_Trace=='True'): 
        self.trace()      
      img_new = self.UpdateImage(img)    
      print('Self Test output:') 
      self._H_print(img_new)        
 

