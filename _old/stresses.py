#!/usr/bin/env python3

import math
import re
import pint

u = pint.UnitRegistry()

__all__ = ['von_mises']

def von_mises(sx=0, sy=0, sz=0, txy=0, tyz=0, txz=0):
  """
This function calculates the Von Mises yield criterion from the three principal
normal stress components () and three principal shear stresses.

  """
  return (((sx-sy)**2 + (sy-sz)**2 + (sz-sx)**2 + 6*(txy**2+tyz**2+txz**2))/2)**(1/2)

class Material:
  def __init__(self):
    self.elasticity_modulus = None
    self.poissons_ratio     = None

# def cylinder_under_uniform_internal_pressure(radius_outer, radius_inner,
                                             # radius_spot,
                                             # pressure, capped=True,
                                             # thick_walled=None,
                                             # Mat = None):
  # if thick_walled == None:
    # # Determine automatically if the cylinder is thick-walled or thin-walled.
    # if radius_outer / (radius_outer - radius_inner) >= 20:
      # thick_walled = False
    # else:
      # thick_walled = True
  # if thick_walled:
    # # s1 = slon, s2 = stan, s3 = srad
    # srad = 
    # stan = 
    # slon = 
    # t    = 
    # sradmax = 
    # stanmax = 
    # tmax    = 

# def cylinder_under_uniform_external_pressure(radius_outer, radius_inner,
                                             # radius_spot,
                                             # pressure, capped=True,
                                             # thick_walled=None,
                                             # Mat = None):
  