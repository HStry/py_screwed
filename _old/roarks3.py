#!/usr/bin/env python3.5
import math
import warnings

def von_mises(*, sx =0, sy =0, sz =0,
                 txy=0, txz=0, tyz=0):
  return (((sx-sy)**2 + (sy-sz)**2 + (sz-sx)**2 + 6*(txy**2 + txz**2 + tyz**2))/2)**(1/2)
  

class Tube:
  def __init__(s, r_e=None, r_i = None, w=None, l=None):
    s.__r_e      = None  # external radius
    s.__r_i      = None  # internal radius
    s.__w        = None  # wall thickness
    s.__l        = None  # length
    s.__p_e      = None  # external pressure
    s.__p_i      = None  # internal pressure
    s.__f_a      = None  # axial force
    s.__m_a      = None  # axial moment
    s.__m_r      = None  # radial moment
    s.__mat      = None  # cylinder material
    s.__capped   = False # capped tube vs. uncapped
    s.__dimorder = []    # order at which radial dimensions are provided.
    s.__dimlock  = None  # locked radial dimension
    s.aliases = {'radius_external'  : 'r_e',
                 'radius_internal'  : 'r_i',
                 'diameter_external': 'd_e',
                 'diameter_internal': 'd_i',
                 'wallthickness'    : 'w'  ,
                 'length'           : 'l'  ,
                 'pressure_external': 'p_e',
                 'pressure_internal': 'p_i',
                 'pressure_net'     : 'p'  ,
                 'force_axial'      : 'f_a',
                 'momenm_axial'     : 'm_a',
                 'momenm_radial'    : 'm_r',
                 'material'         : 'mat'}
    if not r_e is None: s.r_e = r_e
    if not r_i is None: s.r_i = r_i
    if not w   is None: s.w   = w
    if not l   is None: s.l   = l
  def __setradii(s, val, propname):
    def calcmissing(r_e = None, r_i = None, w = None):
      if sum(x is None for x in (r_e, r_i, w)) != 1:
        raise(ValueError('radial dimensions over- or underdefined. Unable to perform calculation.'))
      elif r_e is None: r_e = r_i + w
      elif r_i is None: r_i = r_e - w
      else:             w   = r_e - r_i
      return {'r_e': r_e, 'r_i': r_i, 'w': w}
    dims = {'r_e': s.__r_e, 'r_i': s.__r_i, 'w': s.__w}
    do = s.__dimorder[:]
    dl = s.__dimlock
    me = s.aliases.get(propname, propname)
    if len(do) < 2:
      if me in do: do.remove(me)
      do.append(me)
      dims[me] = val
    elif (dl == None) or (dl == me):
      if me in do: do.remove(me)
      else:        dims[do.pop(0)] = None
      do.append(me)
      dims[me] = val
    elif dl in do:
      tr = 1 if do[0] == dl else 0
      dims[do.pop(tr)] = None
      do.append(me)
      dims[me] = val
    else:
      _dims = calcmissing(**dims)
      _dims[me] = val
      _dims = {dl: _dims[dl], me: _dims[me]}
      dims = calcmissing(**_dims)
      dims[dl] = None
      do.remove(me)
      do.append(me)
    if len(do) == 2:
      _dims = calcmissing(**dims)
      if ((sum((x == abs(x)) == False for x in _dims.values()) != 0) or
          (_dims['r_e'] <= _dims['r_i'])):
        raise(ValueError('Impossible dimensional parameters provided'))
    s.__r_e = dims['r_e']
    s.__r_i = dims['r_i']
    s.__w   = dims['w']
    s.__dimlock  = dl
    s.__dimorder = do[:]
  
  if True:     # define base properties
    if True:   # property external radius (r_e)
      @property
      def r_e(s):
        if not s.__r_e is None:
          return s.__r_e
        elif (not s.__r_i is None) and (not s.__w is None):
          return s.__r_i + s.__w
        else:
          raise(AttributeError('Parameter not defined'))
      @r_e.setter
      def r_e(s, val):
        s.__setradii(val, 'r_e')
      @r_e.deleter
      def r_e(s):
        s.__r_e = None
        if 'r_e' in s.__dimorder: s.__dimorder.remove('r_e')
    if True:   # property internal radius (r_i)
      @property
      def r_i(s):
        if not s.__r_i is None:
          return s.__r_i
        elif (not s.__r_e is None) and (not s.__w is None):
          return s.__r_e - s.__w
        else:
          raise(AttributeError('Parameter not defined'))
      @r_i.setter
      def r_i(s, val):
        s.__setradii(val, 'r_i')
      @r_i.deleter
      def r_i(s):
        s.__r_i = None
        if 'r_i' in s.__dimorder: s.__dimorder.remove('r_i')
    if True:   # property wall thickness (w)
      @property
      def w(s):
        if (not s.__w is None):
          return s.__w
        elif (not s.__r_e is None) and (not s.__r_i is None):
          return s.__r_e - s.__r_i
        else:
          raise(AttributeError('Parameter not defined'))
      @w.setter
      def w(s, val):
        s.__setradii(val, 'w')
      @w.deleter
      def w(s):
        s.__w = None
        if 'w' in s.__dimorder: s.__dimorder.remove('w')
    if True:   # property length (l)
      @property
      def l(s):        return s.__l
      @l.setter
      def l(s, val):   s.__l = val
      @l.deleter
      def l(s):        s.__l == None
    if True:   # property material (mat)
      @property
      def mat(s):      return s.__mat
      @mat.setter
      def mat(s, val): s.__mat = val
      @mat.deleter
      def mat(s):      s.__mat == None
    if True:   # property external pressure (p_e)
      @property
      def p_e(s):      return s.__p_e
      @p_e.setter
      def p_e(s, val): s.__p_e = val
      @p_e.deleter
      def p_e(s):      s.__p_e == None
    if True:   # property internal pressure (p_i)
      @property
      def p_i(s):      return s.__p_i
      @p_i.setter
      def p_i(s, val): s.__p_i = val
      @p_i.deleter
      def p_i(s):      s.__p_i == None
    if True:   # property axial force (f_a)
      @property
      def f_a(s):      return s.__f_a
      @f_a.setter
      def f_a(s, val): s.__f_a = val
      @f_a.deleter
      def f_a(s):      s.__f_a == None
    if True:   # property axial moment (m_a)
      @property
      def m_a(s):      return s.__m_a
      @m_a.setter
      def m_a(s, val): s.__m_a = val
      @m_a.deleter
      def m_a(s):      s.__m_a == None
    if True:   # property radial moment (m_r)
      @property
      def m_r(s):      return s.__m_r
      @m_r.setter
      def m_r(s, val): s.__m_r = val
      @m_r.deleter
      def m_r(s):      s.__m_r == None
    if True:   # property dimlock
      @property
      def dimlock(s):
        return s.__dimlock
      @dimlock.setter
      def dimlock(s, name):
        name = s.__aliases.get(name, name)
        if name in ('r_e', 'r_i', 'w'):
          s.__dimlock = name
        else:
          raise(AttributeError('Incorrect parametername provided'))
      @dimlock.deleter
      def dimlock(s):
        s.__dimlock = None
    if True:   # property capped
      @property
      def capped(s):
        if s.__capped is True:    return True
        elif s.__capped is False: return False
        else: raise(AttributeError('Parameter not defined.'))
      @capped.setter
      def capped(s, val):
        if val is True:    s.__capped = True
        elif val is False: s.__capped = False
        else: raise(AttributeError('Illegal value provided.'))
      @capped.deleter
      def capped(s):
        s.__capped = None
  
  if True:     # define parameter variations
    if True:   # property external diameter (d_e)
      @property
      def d_e(s):      return s.r_e * 2
      @d_e.setter
      def d_e(s, val): s.r_e = val / 2
      @d_e.deleter
      def d_e(s):      del(s.r_e)
    if True:   # property internal diameter (d_i)
      @property
      def d_i(s):      return s.r_i * 2
      @d_i.setter
      def d_i(s, val): s.r_i = val / 2
      @d_i.deleter
      def d_i(s):      del(s.r_i)
    if True:   # net resultant pressure (p)
      @property
      def p(s):
        return s.p_i - s.p_e
    if True:   # cross-sectional area of annulus (a_a)
      @property
      def a_a(s):  return math.pi * (s.r_e**2 - s.r_i**2)
    if True:   # cross-sectional area of core (a_c)
      @property
      def a_c(s):  return math.pi * s.r_i**2
    if True:   # total cross-sectional area (a)
      @property
      def a(s): return math.pi * s.r_e**2
    if True:   # second moment of area (i_x, i_y, i_z)
      @property
      def i_x(s): return (math.pi / 4) * (s.r_e**4 - s.r_i**4)
      @property
      def i_y(s): return s.i_x
      @property
      def i_z(s): return (math.pi / 2) * (s.r_e**4 - s.r_i**4)
  
  def _buckling_linear(s):
    return ((-3 * s.p * s.r_e**3) / s.mat.E)**(1/3)
  def _buckling_pressure(s):
    return (s.r_e - (s.r_e**4 - ((4 * s.f_a * s.l**2) / (math.pi**3 * s.mat.E)))**(1/4))
  def _buckling(s):
    return s.w / max(s._buckling_linear(), s._buckling_pressure())
  
  def _stress_pressure(s):
    if s.p_e < s.p_i:
      # sr = (-q * b**2 * (a**2 - r**2))/(r**2 * (a**2 - b**2))
      # srmax at r=b
      # st = (q * b**2 * (a**2 + r**2))/(r**2 * (a**2 - b**2))
      # stmax at r=b
      # tmax = (q * a**2) / (a**2 - b**2)
      # tmax at r=b
      s_a   = 0 * s.p_i if not s.capped else (s.p * s.r_i**2) / (s.r_e**2 - s.r_i**2)
      s_r_e = (-s.p * s.r_e**2 * (s.r_i**2 - s.r_e**2))/(s.r_e**2 * (s.r_i**2 - s.r_e**2))
      s_r_i = (-s.p * s.r_e**2 * (s.r_i**2 - s.r_i**2))/(s.r_i**2 * (s.r_i**2 - s.r_e**2))
      s_t_e = (s.p * s.r_e**2 * (s.r_i**2 + s.r_e**2))/(s.r_e**2 * (s.r_i**2 - s.r_e**2))
      s_t_i = (s.p * s.r_e**2 * (s.r_i**2 + s.r_i**2))/(s.r_i**2 * (s.r_i**2 - s.r_e**2))
      t_i   = (s.p * s.r_e**2) / (s.r_e**2 - s.r_i**2)
    elif s.p_e > s.p_i:
      # sr = (-q * a**2 * (r**2 - b**2))/(r**2 * (a**2 - b**2))
      # srmax at r=a
      # st = (-q * a**2 * (b**2 + r**2))/(r**2 * (a**2 - b**2))
      # stmax at r=b
      # tmax = (q * a**2) / (a**2 - b**2)
      # tmax at r=b
      s_a   = 0 * s.p_i if not s.capped else (s.p * s.r_e**2) / (s.r_e**2 - s.r_i**2)
      s_r_e = (s.p * s.r_e**2 * (s.r_e**2 - s.r_i**2))/(s.r_e**2 * (s.r_e**2 - s.r_i**2))
      s_r_i = (s.p * s.r_e**2 * (s.r_i**2 - s.r_i**2))/(s.r_i**2 * (s.r_e**2 - s.r_i**2))
      s_t_e = (s.p * s.r_e**2 * (s.r_i**2 + s.r_e**2))/(s.r_e**2 * (s.r_e**2 - s.r_i**2))
      s_t_i = (s.p * s.r_e**2 * (s.r_i**2 + s.r_i**2))/(s.r_i**2 * (s.r_e**2 - s.r_i**2))
      t_i   = (s.p * s.r_e**2) / (s.r_e**2 - s.r_i**2)
    else:
      s_a    = 0 * s.p_i
      s_r_e  = 0 * s.p_i
      s_r_i  = 0 * s.p_i
      s_t_e  = 0 * s.p_i
      s_t_i  = 0 * s.p_i
      t_i   = 0 * s.p_i
    return {'s_a'  : s_a,
            's_r_e': s_r_e,
            's_r_i': s_r_i,
            's_t_e': s_t_e,
            's_t_i': s_t_i,
            't_i'  : t_i}
  def _stress_tension(s):
    return -s.f_a / s.a_a
  def _stresses(s):
    sp = s._stress_pressure()
    st = s._stress_tension()
    return ({'sx': sp['s_r_e'],
             'sy': sp['s_t_e'],
             'sz': sp['s_a'] + st,
             'txy': 0 * s.p_i},
            {'sx': sp['s_r_i'],
             'sy': sp['s_t_i'],
             'sz': sp['s_a'] + st,
             'txy': sp['t_i']})
  def wall_stress(s):
    stress_components = s._stresses()
    return (von_mises(**stress_components[0]),
            von_mises(**stress_components[1]))









if __name__ == '__main__':
  print('import this module.')