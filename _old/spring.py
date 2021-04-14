#!/usr/bin/env python3.5

import os
import sys
import math
import pint
import utils
from collections import OrderedDict
import traceback

u = pint.UnitRegistry()


E = u('205 GPa')   # Modulus of Elasticity
G = u(' 80 GPa')   # Modulus of Rigidity
v = 0.28           # Poisson's ratio
s = u('978 MPa')   # Young's modulus
H = u('70 mm')     # Effective spring range

D = u('80 mm')
w = u(' 5 mm')
h = u('10 mm')
P = u('25 kN')
n = 5


# Notational conversion for Roarks'

if True:     # x property
#    @property
#    def x(self):
#      pass
#    @x.setter
#    def x(self, val):
#      pass
#    @x.deleter
#    def x(self):
#      pass
#  if True:     # _x property
#    @property
#    def _x(self):
#      pass
#    @_x.setter
#    def _x(self, val):
#      raise AttributeError('\'_x\' property cannot be explicitly set.')
#    @_x.deleter
#    def _x(self):
#      raise AttributeError('\'_x\' property cannot be explicitly deleted.')
  pass

def whoami():
  return traceback.extract_stack()[-3][2]

class CircularReferenceError(Exception):
  pass

class Spring:
  def __init__(self, external_diameter=None, internal_diameter=None, mean_diameter=None, height=None, # provide one out of three diameters
                     wire_diameter=None,     wire_width=None,        wire_height=None,                # provide diam, or width and height
                     coil_angle=None,        coil_pitch=None,        coil_count=None,                 # provide two out of three
                     v=None, E=None):
    self.__cname = 'Spring'
    self.__UD = {"external_diameter": None,  
                 "internal_diameter": None,  
                 "mean_diameter"    : None,  
                 "height"           : None,  
                 "wire_round"       : None,  # True or False
                 "wire_width"       : None,  
                 "wire_height"      : None,  
                 "coil_angle"       : None,  
                 "coil_pitch"       : None,  
                 "coil_count"       : None,  # n = h/p       | n = 
                 "poissonsratio"    : None,  # v = (E/2G)-1
                 "elasticitymodulus": None,  # E = 2G(1+v)
                 "rigiditymodulus"  : None}  # G = E/(2(1+v))
  if True:  # property calculations
    def __mean_diameter(self, source=None):        # done
      me = whoami().lstrip('_')
      if source is None: source = []
      if me in source:   raise(CircularReferenceError())
      source.append(me)
      # define the different methods with which to get or calculate 'me'
      def m0(self):
        if not self.__UD[me] is None:
          return self.__UD[me], [me]
      def m1(self):
        ed = self.__external_diameter(source)
        ww = self.__wire_width(source)
        if not None in [ed, ww]:
          return ed[0] - ww[0], utils.union(ed[1], ww[1])
      def m2(self):
        id = self.__internal_diameter(source)
        ww = self.__wire_width(source)
        if not None in [id, ww]:
          return id[0] + ww[0], utils.union(id[1], ww[1])
      def m3(self):
        cp = self.__coil_pitch(source)
        ca = self.__coil_angle(source)
        if not None in [cp, ca]:
          return cp[0] / (math.pi * math.tan(ca[0])), utils.union(cp[1], ca[1])
      def m4(self):
        h  = self.__height(source)
        cc = self.__coil_count(source)
        ca = self.__coil_angle(source)
        if not None in [h, cc, ca]:
          return h[0] / (math.pi * cc[0] * math.tan(ca[0])), utils.union(h[1], cc[1], ca[1])
      for m in (m0, m1, m2, m3, m4):
        try:
          r = m()
          if r: return r
        except CircularReferenceError:
          pass
    def __external_diameter(self, source=None):    # done
      me = whoami().lstrip('_')
      if source is None: source = []
      if me in source:   raise(CircularReferenceError())
      source.append(me)
      def m0(self):
        if not self.__UD[me] is None:
          return self.__UD[me], [me]
      def m1(self):
        md = self.__mean_diameter(source)
        ww = self.__wire_width(source)
        if not None in [md, ww]:
          return md[0] + ww[0], utils.union(md[1], ww[1])
      def m2(self):
        id = self.__internal_diameter(source)
        ww = self.__wire_width(source)
        if not None in [id, ww]:
          return id[0] + 2*ww[0], utils.union(id[1], ww[1])
      for m in (m0, m1, m2):
        try:
          r = m()
          if r: return r
        except CircularReferenceError:
          pass
    def __internal_diameter(self, source=None):    # done
      me = whoami().lstrip('_')
      if source is None: source = []
      if me in source:   raise(CircularReferenceError())
      source.append(me)
      def m0(self):
        if not self.__UD[me] is None:
          return self.__UD[me], [me]
      def m1(self):
        md = self.__mean_diameter(source)
        ww = self.__wire_width(source)
        if not None in [md, ww]:
          return md[0] - ww[0], utils.union(md[1], ww[1])
      def m2(self):
        ed = self.__external_diameter(source)
        ww = self.__wire_width(source)
        if not None in [ed, ww]:
          return ed[0] - 2*ww[0], utils.union(ed[1], ww[1])
      for m in (m0, m1, m2):
        try:
          r = m()
          if r: return r
        except CircularReferenceError:
          pass
    def __height(self, source=None):               # done
      me = whoami().lstrip('_')
      if source is None: source = []
      if me in source:   raise(CircularReferenceError())
      source.append(me)
      def m0(self):
        if not self.__UD[me] is None:
          return self.__UD[me], [me]
      def m1(self):
        cc = self.__coil_count(source)
        cp = self.__coil_pitch(source)
        if not None in [cc, cp]:
          return cc[0] * cp[0], utils.union(cc[1], cp[1])
      for m in (m0, m1):
        try:
          r = m()
          if r: return r
        except CircularReferenceError:
          pass
    def __wire_width(self, source=None):           # done
      me = whoami().lstrip('_')
      if source is None: source = []
      if me in source:   raise(CircularReferenceError())
      source.append(me)
      def m0(self):
        if not self.__UD[me] is None:
          return self.__UD[me], [me]
      def m1(self):
        md = self.__mean_diameter(source)
        ed = self.__external_diameter(source)
        if not None in [md, ed]:
          return ed[0] - md[0], utils.union(md[1], ed[1])
      def m2(self):
        md = self.__mean_diameter(source)
        id = self.__internal_diameter(source)
        if not None in [md, id]:
          return md[0] - id[0], utils.union(md[1], id[1])
      def m3(self):
        ed = self.__external_diameter(source)
        id = self.__internal_diameter(source)
        if not None in [ed, id]:
          return (ed[0] - id[0])/2, utils.union(ed[1], id[1])
      for m in (m0, m1, m2, m3):
        try:
          r = m()
          if r: return r
        except CircularReferenceError:
          pass
    def __wire_height(self, source=None):          # done
      me = whoami().lstrip('_')
      if source is None: source = []
      if me in source:   raise(CircularReferenceError())
      source.append(me)
      def m0(self):
        if not self.__UD[me] is None:
          return self.__UD[me], [me]
      for m in (m0):
        try:
          r = m()
          if r: return r
        except CircularReferenceError:
          pass
    def __coil_angle(self, source=None):           # done
      me = whoami().lstrip('_')
      if source is None: source = []
      if me in source:   raise(CircularReferenceError())
      source.append(me)
      def m0(self):
        if not self.__UD[me] is None:
          return self.__UD[me], [me]
      def m1(self):
        md = self.__mean_diameter(source)
        cp = self.__coil_pitch(source)
        if not None in [md, cp]:
          return math.atan(cp[0]/(math.pi * md[0])), utils.union(md[1], cp[1])
      for m in (m0, m1):
        try:
          r = m()
          if r: return r
        except CircularReferenceError:
          pass
    def __coil_pitch(self, source=None):           # done
      me = whoami().lstrip('_')
      if source is None: source = []
      if me in source:   raise(CircularReferenceError())
      source.append(me)
      def m0(self):
        if not self.__UD[me] is None:
          return self.__UD[me], [me]
      def m1(self):
        md = self.__mean_diameter(source)
        ca = self.__coil_angle(source)
        if not None in [md, ca]:
          return math.pi * md[0] * math.tan(ma[0]), utils.union(md[1], ca[1])
      def m2(self):
        h  = self.__height(source)
        cc = self.__coil_count(source)
        if not None in [h, cc]:
          return h[0] / cc[0], utils.union(h[1], cc[1])
      for m in (m0, m1, m2):
        try:
          r = m()
          if r: return r
        except CircularReferenceError:
          pass
    def __coil_count(self, source=None):           # done
      me = whoami().lstrip('_')
      if source is None: source = []
      if me in source:   raise(CircularReferenceError())
      source.append(me)
      def m0(self):
        if not self.__UD[me] is None:
          return self.__UD[me], [me]
      def m1(self):
        h  = self.__height(source)
        cp = self.__coil_pitch(source)
        if not None in [h, cp]:
          return h[0] / cp[0], utils.union(h[1], cp[1])
      for m in (m0, m1):
        try:
          r = m()
          if r: return r
        except CircularReferenceError:
          pass
    def __poissonsratio(self, source=None):        # done
      me = whoami().lstrip('_')
      if source is None: source = []
      if me in source:   raise(CircularReferenceError())
      source.append(me)
      def m0(self):
        if not self.__UD[me] is None:
          return self.__UD[me], [me]
      def m1(self):
        em = self.__elasticitymodulus(source)
        rm = self.__rigiditymodulus(source)
        if not None in [em, rm]:
          return (em[0] / (2*rm[0]) -1), utils.union(em[1], rm[1])
      for m in (m0, m1):
        try:
          r = m()
          if r: return r
        except CircularReferenceError:
          pass
    def __elasticitymodulus(self, source=None):    # done
      me = whoami().lstrip('_')
      if source is None: source = []
      if me in source:   raise(CircularReferenceError())
      source.append(me)
      def m0(self):
        if not self.__UD[me] is None:
          return self.__UD[me], [me]
      def m1(self):
        pr = self.__poissonsratio(source)
        rm = self.__rigiditymodulus(source)
        if not None in [pr, rm]:
          return 2 * rm[0] * (1 + pr[0]), utils.union(pr[1], rm[1])
      for m in (m0, m1):
        try:
          r = m()
          if r: return r
        except CircularReferenceError:
          pass
    def __rigiditymodulus(self, source=None):      # done
      me = whoami().lstrip('_')
      if source is None: source = []
      if me in source:   raise(CircularReferenceError())
      source.append(me)
      def m0(self):
        if not self.__UD[me] is None:
          return self.__UD[me], [me]
      def m1(self):
        pr = self.__poissonsratio(source)
        em = self.__elasticitymodulus(source)
        if not None in [pr, em]:
          return em[0] / (2 * (1 + pr[0])), utils.union(pr[1], em[1])
      for m in (m0, m1):
        try:
          r = m()
          if r: return r
        except CircularReferenceError:
          pass
  
  if True:  # Declare standardized properties
    def __mygetattr__(self, par):
      val = getattr(self, '_{}__{}'.format(self.__class__.__name__, par))()
      if val: return val[0]
      else:   raise(AttributeError('\'{}\' property not defined.'.format(par)))
    def __mysetattr__(self, par, value):
      val = getattr(self, '_{}__{}'.format(self.__class__.__name__, par))()
      if (val is None) or (val[1][0] == par): self.__UD[par] = value
      else: raise(AttributeError('\'{}\' property already defined through: {}'.format(par, ', '.join(["'"+p+"'" for p in val[1]]))))
    def __mydelattr__(self, par):
      val = getattr(self, '_{}__{}'.format(self.__class__.__name__, par))()
      if not val or val[1][0] == par: self.__UD[par] = None
      else: raise(AttributeError('\'mean_diameter\' property cannot be deleted. Defined through: {}'.format(', '.join(["'"+p+"'" for p in val[1]]))))
    @property
    def mean_diameter(self):            self.__mygetattr__(whoami())
    @mean_diameter.setter
    def mean_diameter(self, value):     self.__mysetattr__(whoami(), value)
    @mean_diameter.deleter
    def mean_diameter(self):            self.__mydelattr__(whoami())
    @property
    def external_diameter(self):        self.__mygetattr__(whoami())
    @external_diameter.setter
    def external_diameter(self, value): self.__mysetattr__(whoami(), value)
    @external_diameter.deleter
    def external_diameter(self):        self.__mydelattr__(whoami())
    @property
    def internal_diameter(self):        self.__mygetattr__(whoami())
    @internal_diameter.setter
    def internal_diameter(self, value): self.__mysetattr__(whoami(), value)
    @internal_diameter.deleter
    def internal_diameter(self):        self.__mydelattr__(whoami())
    @property
    def height(self):                   self.__mygetattr__(whoami())
    @height.setter
    def height(self, value):            self.__mysetattr__(whoami(), value)
    @height.deleter
    def height(self):                   self.__mydelattr__(whoami())
    @property
    def coil_angle(self):               self.__mygetattr__(whoami())
    @coil_angle.setter
    def coil_angle(self, value):        self.__mysetattr__(whoami(), value)
    @coil_angle.deleter
    def coil_angle(self):               self.__mydelattr__(whoami())
    @property
    def coil_pitch(self):               self.__mygetattr__(whoami())
    @coil_pitch.setter
    def coil_pitch(self, value):        self.__mysetattr__(whoami(), value)
    @coil_pitch.deleter
    def coil_pitch(self):               self.__mydelattr__(whoami())
    @property
    def coil_count(self):               self.__mygetattr__(whoami())
    @coil_count.setter
    def coil_count(self, value):        self.__mysetattr__(whoami(), value)
    @coil_count.deleter
    def coil_count(self):               self.__mydelattr__(whoami())
    @property
    def poissonsratio(self):            self.__mygetattr__(whoami())
    @poissonsratio.setter
    def poissonsratio(self, value):     self.__mysetattr__(whoami(), value)
    @poissonsratio.deleter
    def poissonsratio(self):            self.__mydelattr__(whoami())
    @property
    def elasticitymodulus(self):        self.__mygetattr__(whoami())
    @elasticitymodulus.setter
    def elasticitymodulus(self, value): self.__mysetattr__(whoami(), value)
    @elasticitymodulus.deleter
    def elasticitymodulus(self):        self.__mydelattr__(whoami())
    @property
    def rigiditymodulus(self):          self.__mygetattr__(whoami())
    @rigiditymodulus.setter
    def rigiditymodulus(self, value):   self.__mysetattr__(whoami(), value)
    @rigiditymodulus.deleter
    def rigiditymodulus(self):          self.__mydelattr__(whoami())
    
  if True:  # Declare customized properties
    if True:  # wire_diameter
      @property
      def wire_diameter(self):
        me = whoami()
        val = getattr(self, '_{}__{}'.format(self.__class__.__name__, 'wire_width'))()
        if self.__UD['wire_round'] is True and val: return val[0]
        elif self.__UD['wire_round'] is None and val:
          warnings.warn('\'{}\' derived from other parameters. Assuming round wire.'.format(me))
          return val[0]
        else: raise(AttributeError('\'{}\' property not defined.'.format(me)))
      @wire_diameter.setter
      def wire_diameter(self, value):
        me = whoami()
        val = getattr(self, '_{}__{}'.format(self.__class__.__name__, 'wire_width'))()
          if (val is None) or (val[1][0] == 'wire_width' and self.__UD['wire_round']):
            self.__UD['wire_width']
      @wire_diameter.deleter
      def wire_diameter(self):
    if True:  # wire_width
      @property
      def wire_width(self):
        me = whoami()
        val = getattr(self, '_{}__{}'.format(self.__class__.__name__, me))()
        if self.__UD['wire_round'] is False and val: return val[0]
        else: raise(AttributeError('\'{}\' property not defined.'.format(me)))
      @wire_width.setter
      def wire_width(self, value):
        me = whoami()
        val = getattr(self, '_{}__{}'.format(self.__class__.__name__, me))()
        if (val is None) or (val[1][0] == me and self.__UD['wire_round'] is False):
          self.__UD['wire_round'] = False
          self.__UD[me]           = value
        else:
          if self.__UD['wire_round'] is True:
            raise(AttributeError('\'wire_width\' and \'wire_height\' unavailable. Round wire selected.'))
          else:
            raise(AttributeError('\'{}\' property already defined through: {}'.format(me, ', '.join(["'"+p+"'" for p in val[1]]))))
      @wire_width.deleter
      def wire_width(self):
    if True:  # wire_height
      @property
      def wire_height(self):
      @wire_height.setter
      def wire_height(self, value):
      @wire_height.deleter
      def wire_height(self):
    
    
    
    
    

def spring(D, w, h, n, P, G):
  a = max(w, h)/2
  b = min(w, h)/2
  R = (D-w)/2
  c = R/b
  
  if w == h:
    if c <= 3: raise(Exception('Cannot calculate.'))
    f = (2.789 * P * R**3 * n) / (G * b**4)
    t = ((4.8 * P * R) / (8 * b**3)) * (1 + (1.2/c) + (0.56/c**2) + (0.5/c**3))
  else:
    if h > w and c <= 3: raise(Exception('Cannot calculate.'))
    if w > h and c <= 5: raise(Exception('Cannot calculate.'))
    f = ((3 * math.pi * P * R**3 * n) / (8 * G * b**4)) * (1 / ((a/b) - 0.627*(math.tanh((math.pi * b)/(2*a)) + 0.004)))
    t = ((P * R * (3*b + 1.8*a))/(8 * b**2 * a**2)) * (1 + (1.2/c) + (0.56/c**2) + (0.5/c**3))
  return f.to('mm'), t.to('MPa')


def mktable(D, wr, hr, n, P, G):
  values = [[None]]
  wr = list(wr)
  for h in hr:
    values.append([h])
    for w in wr:
      if not w in values[0]: values[0].append(w)
      f, t = spring(D, w, h, n, P, G)
      values[-1].append([f, t])
  with open('output.csv', 'w', encoding='utf-8') as f:
    # ,3 mm,,4 mm,,5 mm,
    # ,f (mm),t (MPa),f (mm),t (MPa),f (mm),t (MPa)
    # 10 mm,53.4,987,50.1,778,45.8,669
    f.write(''.join([',{0.magnitude:.1f} {0.units:~P},'.format(i) for i in values[0][1:]]))
    f.write('\n')
    f.write(''.join([',f (mm),t (MPa)' for i in values[0][1:]]))
    f.write('\n')
    for lines in values[1:]:
      f.write('{0.magnitude:.1f} {0.units:~P},'.format(lines[0]))
      f.write(','.join(['{.magnitude:.1f},{.magnitude:.0f}'.format(i[0], i[1]) for i in lines[1:]]))
      f.write('\n')
    
    
    
    
      
      
      