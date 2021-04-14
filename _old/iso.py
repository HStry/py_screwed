#!/usr/bin/env python3
"""
Module containing various functions regarding ISO threads.
"""
import math
import pint
from . import tolerances

class Threadf:
  def __init__(self):
    pass

class Threadm:
  def __init__(self):
    pass

class Thread:
  def __init__(self, Diameter, Pitch, Lead=None,
                     IntPitchTolerance=None, IntMinorTolerance=None,
                     ExtPitchTolerance=None, ExtMajorTolerance=None,
                     ThreadEngagement="N", LeftHandedness=False):
    self.Diameter = Diameter
    self.Pitch = Pitch
    self.IntPitchTolerance = IntPitchTolerance
    self.IntMinorTolerance = IntMinorTolerance
    self.ExtPitchTolerance = ExtPitchTolerance
    self.ExtMajorTolerance = ExtMajorTolerance
    self.Lead = Lead
    self.ThreadEngagement = ThreadEngagement
    self.LeftHandedness = LeftHandedness
    
  def set(self, Diameter=None, Pitch=None,
                IntPitchTolerance=None, IntMinorTolerance=None,
                ExtPitchTolerance=None, ExtMajorTolerance=None,
                Leads=None, ThreadEngagement=None, LeftHandedness=None,
                recalc=True):
    pass

def H(P):
  return (3**(1/2)/2)*P

def D1_base(D, H):
  return D - 2*(5/8)*H

def D2_base(D, H):
  return D - 2*(3/8)*H

def C_max():
  pass




def tolerance(P, ):
  pass


def eviation():
  pass


def C_min(Pitch):
  return (1/8)*Pitch

def R_min(Pitch):
  return 

def Desgn2Params(designation):
  """Desgn2Params(designation)
  Converts a thread designation according to ISO 965-1:2013, chapter 12, to its
  individual components. Returns a dictionary containing the values within the
  ISO string. Decoding is not strict. Will process "M10 × 1.5 - 7H/7g6g" as well
  as the non-conform "m8 X ph2,5p1,25(two starts) - 7H / 7g".
  
  Will extract:
    diameter, lead, pitch, tolerances, engagement, handedness.
"""
  def _2num(s):
    if s == None:
      return None
    else:
      try:
        return int(s.replace(',', '.'))
      except ValueError:
        return float(s.replace(',', '.'))
      except:
        raise
  
  def _2uc(s):
    if s == None:
      return None
    else:
      try:
        return s.upper()
      except:
        raise
  
  matchpattern = ("(?:[Mm]([0-9]+[.,]?[0-9]*))" +
                  "(?:[ ]*[xX×][ ]*(?:(?:[Pp][Hh])?([0-9]+[.,]?[0-9]*)[Pp]([0-9]+[.,]?[0-9]*))(?:[ ]*[(][a-zA-Z ]+[)])?)?" +
                  "(?:[ ]*[xX×][ ]*([0-9]+[.,]?[0-9]*))?" +
                  "(?:[ ]*[-][ ]*(?:([0-9]+[A-Z])?([0-9]+[A-Z])?[ /]*([0-9]+[a-z])?([0-9]+[a-z])?))?" +
                  "(?:[ ]*[-][ ]*([SsNnLl]))?" +
                  "(?:[ ]*[-][ ]*([Ll][Hh]))?")
  li = list(re.search(matchpattern, designation).groups())
  params = {}
  params['Diameter'] = _2num(li[0])
  params['Lead'] = _2num(li[1])
  if (li[2] != None):
    params['Pitch'] = _2num(li[2])
  else:
    params['Pitch'] = _2num(li[3])
    params['Lead'] = _2num(li[3])
  params['IntPitchTolerance'] = li[4]
  if (li[5] == None): params['IntMinorTolerance'] = li[4]
  else:               params['IntMinorTolerance'] = li[5]
  params['ExtPitchTolerance'] = li[6]
  if (li[7] == None): params['ExtMajorTolerance'] = li[6]
  else:               params['ExtMajorTolerance'] = li[7]
  params['ThreadEngagement'] = _2uc(li[8])
  if _2uc(li[9]) == 'LH': params['LeftHandedness'] = True
  else:                   params['LeftHandedness'] = False
  
  
  try:
    N_leads = (params['Lead']/params['Pitch']).is_integer()
    if not N_leads:
      raise(ValueError('Incorrect lead value for pitch. Should be exact multiple.'))
  except:
    raise
  
  return params

def Params2Desgn(Diameter, Pitch, Lead,
                 IntPitchTolerance, IntMinorTolerance,
                 ExtPitchTolerance, ExtMajorTolerance,
                 ThreadEngagement, LeftHandedness):
  if isinstance(Diameter, int):
    sDiameter = "M{:d}".format(Diameter)
  elif isinstance(Diameter, int):
    if Diameter.is_integer():
      sDiameter = "M{:d}".format(int(Diameter))
    else:
      sDiameter = "M{}".format(str(Diameter))







if __name__ == '__main__':
  print("You cannot run this module from the commandline.\n" +
        "Please importing it.")