#!/usr/bin/env python3.5
import math
import warnings

def von_mises(sx=0, sy=0, sz=0, txy=0, tyz=0, txz=0):
  """
This function calculates the Von Mises yield criterion from the three principal
normal stress components () and three principal shear stresses.

  """
  return (((sx-sy)**2 + (sy-sz)**2 + (sz-sx)**2 + 6*(txy**2 + tyz**2 + txz**2)) /2)**(1/2)

class Tube:
  def __init__(self):
    self.__rext     = None     # external radius
    self.__rint     = None     # internal radius
    self.__wt       = None     # wall thickness
    self.__len      = None     # cylinder length
    self.__mat      = None     # cylinder material
    self.__pext     = None     # external pressure
    self.__pint     = None     # internal pressure
    self.__fax      = None     # axial tension
    self.__tax      = None     # axial torsion
    self.__trad     = None     # radial torsion
    self.__capped   = None     # capped tube, e.g. pressure vessel
    self.__dimorder = []       # order at which radial dimensions are provided
    self.__dimlock  = None
    self.__aliases  = {'re' : 'radius_external',
                       'ri' : 'radius_internal',
                       'de' : 'diameter_external',
                       'di' : 'diameter_internal',
                       'w'  : 'wallthickness',
                       'l'  : 'length',
                       'mat': 'material',
                       'pe' : 'pressure_external',
                       'pi' : 'pressure_internal',
                       'fa' : 'force_axial',
                       'ta' : 'torsion_axial',
                       'tr' : 'torsion_radial'}
    w = (((3 * (self.pressure_external - self.pressure_internal) * 
           self.radius_external**3) / self.material.youngs_modulus)**(1/3))
    return self.wallthickness / w
  def buckling_longitudinal_force(self):
    w = (self.radius_external -
         (self.radius_external**4 -
          ((4 * self.force_axial * self.length**2) /
           (math.pi**3 * self.material.youngs_modulus)))**(1/4))
    return self.wallthickness / w
  def stress_pressure(self):
    """Determines the individual stress components due to internal or external pressure."""
    # gets s1, s2, s3, t1 for the inner and outer edge of the tube
      if self.pressure_external < self.pressure_internal: #internal pressure
        if self.capped:
          s1 = ((self.pressure_net * self.radius_internal ** 2) / 
                (self.radius_external**2 - self.radius_internal**2))
        else:
          s1 = 0
        s2i = ((self.pressure_net * self.radius_internal**2 * (self.radius_external**2 + self.radius_internal**2)) /
               (self.radius_internal**2 * (self.radius_external**2 - self.radius_internal**2)))
        s2e = ((self.pressure_net * self.radius_internal**2 * (self.radius_external**2 + self.radius_external**2)) /
               (self.radius_external**2 * (self.radius_external**2 - self.radius_internal**2)))
        s3i = ((-1 * self.pressure_net * self.radius_internal**2 * (self.radius_external**2 - self.radius_internal**2)) /
               (self.radius_internal**2 * (self.radius_external**2 - self.radius_internal**2)))
        s3e = ((-1 * self.pressure_net * self.radius_internal**2 * (self.radius_external**2 - self.radius_internal**2)) /
               (self.radius_internal**2 * (self.radius_external**2 - self.radius_internal**2)))
        
      
      elif self.pressure_external > self.pressure_internal:
        if self.capped:
          s1 = ((self.pressure_net * self.radius_external ** 2) / 
                (self.radius_external**2 - self.radius_internal**2))
        else:
          s1 = 0
      else:
      
    return None
  def stress_tension(self):
    """Determines the individual stress components due to longitudinal tension."""
  def stress_torsion(self):
    """
    """
  def __setradii(self, val, propname):
    def calcmissing(radius_external = None, radius_internal = None, wallthickness = None):
      if sum(x is None for x in (radius_external, radius_internal, wallthickness)) != 1:
        raise(ValueError('Too few or many uncertainties to calculate missing value'))
      elif radius_external is None: radius_external = radius_internal + wallthickness
      elif radius_internal is None: radius_internal = radius_external - wallthickness
      else:                         wallthickness =   radius_external - radius_internal
      return {'radius_external': radius_external,
              'radius_internal': radius_internal,
              'wallthickness'  : wallthickness}
    dims = {'radius_external': self.__rext,
            'radius_internal': self.__rint,
            'wallthickness':   self.__wt}
    do = self.__dimorder[:]
    dl = self.__dimlock
    me = propname
    if len(do) < 2:
      if me in do: do.remove(me)
      do.append(me)
      dims[me] = val
    elif (dl is None) or (dl == me):
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
      _dims = calcmissing(**dims)  # calculates locked value
      _dims[me] = val
      _dims = {dl: _dims[dl], me: _dims[me]}
      dims = calcmissing(**_dims)  # calculates existing value from me and locked
      dims[dl] = None  # resets to a single 'None' value to prevent overdefined situation.
      do.remove(me)
      do.append(me)
    # Now for some validity testing:
    if len(do) == 2:
      _dims = calcmissing(**dims)
      if ((sum((x == abs(x)) == False for x in _dims.values()) != 0) or
          (_dims['radius_external'] <= _dims['radius_internal'])):
        raise(ValueError('Impossible dimensional parameters provided'))
    self.__rext = dims['radius_external']
    self.__rint = dims['radius_internal']
    self.__wt   = dims['wallthickness']
    self.__dimlock  = dl
    self.__dimorder = do[:]
  
  if True:    # define base properties
    if True:  # property radius_external
      @property
      def radius_external(self):
        if not self.__rext is None:
          return self.__rext
        elif (not self.__rint is None) and (not self.__wt is None):
          return self.__rint + self.__wt
        else:
          raise(AttributeError('Parameter not defined'))
      @radius_external.setter
      def radius_external(self, val):
        self.__setradii(val, 'radius_external')
      @radius_external.deleter
      def radius_external(self):
        self.__rext = None
        if 'radius_external' in self.__dimorder: self.__dimorder.remove('radius_external')
    if True:  # property radius_internal
      @property
      def radius_internal(self):
        if not self.__rint is None:
          return self.__rint
        elif (not self.__rext is None) and (not self.__wt is None):
          return self.__rext - self.__wt
        else:
          raise(AttributeError('Parameter not defined'))
      @radius_internal.setter
      def radius_internal(self, val):
        self.__setradii(val, 'radius_internal')
      @radius_internal.deleter
      def radius_internal(self):
        self.__rint = None
        if 'radius_internal' in self.__dimorder: self.__dimorder.remove('radius_internal')
    if True:  # property wallthickness
      @property
      def wallthickness(self):
        if (not self.__wt is None):
          return self.__wt
        elif (not self.__rext is None) and (not self.__rint is None):
          return self.__rext - self.__rint
        else:
          raise(AttributeError('Parameter not defined'))
      @wallthickness.setter
      def wallthickness(self, val):
        self.__setradii(val, 'wallthickness')
      @wallthickness.deleter
      def wallthickness(self):
        self.__wt = None
        if 'wallthickness' in self.__dimorder: self.__dimorder.remove('wallthickness')
    if True:  # property length
      @property
      def length(self):                 return self.__len
      @length.setter
      def length(self, val):            self.__len = val
      @length.deleter
      def length(self):                 self.__len == None
    if True:  # property material
      @property
      def material(self):               return self.__mat
      @material.setter
      def material(self, val):          self.__mat = val
      @material.deleter
      def material(self):               self.__mat == None
    if True:  # property pressure_external
      @property
      def pressure_external(self):      return self.__pext
      @pressure_external.setter
      def pressure_external(self, val): self.__pext = val
      @pressure_external.deleter
      def pressure_external(self):      self.__pext == None
    if True:  # property pressure_internal
      @property
      def pressure_internal(self):      return self.__pint
      @pressure_internal.setter
      def pressure_internal(self, val): self.__pint = val
      @pressure_internal.deleter
      def pressure_internal(self):      self.__pint == None
    if True:  # property force_axial
      @property
      def force_axial(self):            return self.__fax
      @force_axial.setter
      def force_axial(self, val):       self.__fax = val
      @force_axial.deleter
      def force_axial(self):            self.__fax == None
    if True:  # property torsion_axial
      @property
      def torsion_axial(self):          return self.__tax
      @torsion_axial.setter
      def torsion_axial(self, val):     self.__tax = val
      @torsion_axial.deleter
      def torsion_axial(self):          self.__tax == None
    if True:  # property torsion_radial
      @property
      def torsion_radial(self):         return self.__trad
      @torsion_radial.setter
      def torsion_radial(self, val):    self.__trad = val
      @torsion_radial.deleter
      def torsion_radial(self):         self.__trad == None
    if True:  # property dimlock
      @property
      def dimlock(self):
        return self.__dimlock
      @dimlock.setter
      def dimlock(self, name):
        name = self.__aliases.get(name, name)
        if name in ('radius_external', 'radius_internal', 'wallthickness'):
          self.__dimlock = name
        else:
          raise(AttributeError('Incorrect parametername provided'))
      @dimlock.deleter
      def dimlock(self):
        self.__dimlock = None
    if True:  # property capped
      @property
      def capped(self):
        if self.__capped is True:    return True
        elif self.__capped is False: return False
        else: raise(AttributeError('Parameter not defined.'))
      @capped.setter
      def capped(self, val):
        if val is True:    self.__capped = True
        elif val is False: self.__capped = False
        else: raise(AttributeError('Illegal value provided.'))
      @capped.deleter
      def capped(self):
        self.__capped = None
    
  if True:    # define parameter variations
    if True:  # property diameter_external
      @property
      def diameter_external(self):      return self.radius_external * 2
      @diameter_external.setter
      def diameter_external(self, val): self.radius_external = val / 2
      @diameter_external.deleter
      def diameter_external(self):      del(self.radius_external)
    if True:  # property diameter_internal
      @property
      def diameter_internal(self):      return self.radius_internal * 2
      @diameter_internal.setter
      def diameter_internal(self, val): self.radius_internal = val / 2
      @diameter_internal.deleter
      def diameter_internal(self):      del(self.radius_internal)
    if True:  # net resultant pressure
      @property
      def pressure_net(self):
        return self.pressure_internal - self.pressure_external
    if True:  # cross-sectional area of cylinder wall
      @property
      def area_wall(self):  return math.pi * (self.radius_external**2 - self.radius_internal**2)
    if True:  # cross-sectional area of cylinder inside
      @property
      def area_core(self):  return math.pi * self.radius_internal**2
    if True:  # cross-sectional area of total cylinder
      @property
      def area_total(self): return math.pi * self.radius_external**2
    if True:  # second moment of area
      @property
      def Ix(self): return (math.pi / 4) * (self.radius_external**4 - self.radius_internal**4)
      @property
      def Iy(self): return self.Ix
      @property
      def Iz(self): return (math.pi / 2) * (self.radius_external**4 - self.radius_internal**4)
  
      
  
  if not True:    # define parameter aliases
    @property
    def re(self):      return self.radius_external
    @re.setter
    def re(self, val): self.radius_external = val
    @re.deleter
    def re(self):      del(self.radius_ternal)
    @property
    def ri(self):      return self.radius_internal
    @ri.setter
    def ri(self, val): self.radius_internal = val
    @ri.deleter
    def ri(self):      del(self.radius_internal)
    @property
    def de(self):      return self.diameter_external
    @de.setter
    def de(self, val): self.diameter_external = val
    @de.deleter
    def de(self):      del(self.diameter_external)
    @property
    def di(self):      return self.diameter_internal
    @di.setter
    def di(self, val): self.diameter_internal = val
    @di.deleter
    def di(self):      del(self.diameter_internal)
    @property
    def w(self):       return self.wallthickness
    @w.setter
    def w(self, val):  self.wallthickness = val
    @w.deleter
    def w(self):       del(self.wallthickness)
    
      
      
    
      