#!/usr/bin/env python3
from . import iso
from . import tolerances
from . import preferred_numbers
from . import stresses
from . import thread


class Dim:
  def __init__(self, nom, d1, d2=None, mt='worst-case'):
    # Compare type: 
    #   'exact'        Exact comparison.
    #                  (5 +0.5/-0.2) != (5.2 +0.3/-0.4)
    #   'equivalent'   Equivalent comparison.
    #                  (5 +0.5/-0.2) == (5.2 +0.3/-0.4)
    #   'linear.5'     linear overlap compare. Numerical value after period is
    #                  ratio of required overlap. e.g. in this case 50% overlap
    #                  is required. Overlap is tested in one direction.
    #                  Should one dimension be wider than the other, it may
    #                  occur that both (a == b), (b != a) are true.
    #                  (5 +0.5/-0.2) == (5.5 +0.2/-0.5)
    #                  (5 +0.5/-0.2) != (5.5 +0.5/-0.2)
    #   'sd.5'
    # Contain type:
    self.COMPARE_TYPE = 'exact'
    self.MODEL_TYPE = mt # currently only 'worst-case' is implemented.
                         # Statistical variation, aka. 'stat-var', is still on
                         # the to-do list.
    self.value = nom
    if d2==None: d2 = -1 * d1
    self.dmin = min(d1, d2)
    self.dmax = max(d1, d2)
    self.min = self.value + self.dmin
    self.max = self.value + self.dmax
    self._compound = [[[self.value, self.dmin, self.dmax]],[]]
  def recalculate(self):
    if self.MODEL_TYPE == 'worst-case':
      val = 0
      dmin = 0
      dmax = 0
      for v in self._compound[0]:
        val = val + v[0]
        dmin = dmin + v[1]
        dmax = dmax + v[2]
      for v in self._compound[1]:
        val = val - v[0]
        dmin = dmin - v[1]
        dmax = dmax - v[2]
    self.value = val
    self.dmin = dmin
    self.dmax = dmax
    self.min = self.value + self.dmin
    self.max = self.value + self.dmax
  def __repr__(self):
    return "<class '{0}.{1}'> {2:} ({3:}/{4:})".format(self.__module__, self.__class__.__name__, self.value, self.dmax, self.dmin)
  def __str__(self):
    return "{0:} ({1:}/{2:})".format(self.value, self.dmax, self.dmin)
  def __format__(self, spec):
    pass
  def __add__(self, other):
    # method for arithmetic operation "+"
    if isinstance(other, Dim):
      self._compound[0].extend(other._compound[0])
      self._compound[1].extend(other._compound[1])
      self.recalculate()
      return self
  def __sub__(self, other):
    if isinstance(other, Dim):
      self._compound[0].extend(other._compound[1])
      self._compound[1].extend(other._compound[0])
    # method for arithmetic operation "-"
  def __mul__(self, other):
    # method for arithmetic operation "*"
    if (isinstance(other, int) or
        (isinstance(other, float) and other.is_integer())):
      self._compound[0] = int(other) * self._compound[0]
      self._compound[1] = int(other) * self._compound[1]
    return NotImplemented
  def __truediv__(self, other):  return NotImplemented
  def __matmul__(self, other):   return NotImplemented
  def __floordiv__(self, other): return NotImplemented
  def __mod__(self, other):      return NotImplemented
  def __divmod__(self, other):   return NotImplemented
  def __pow__(self, other):      return NotImplemented
  def __lshift__(self, other):   return NotImplemented
  def __rshift__(self, other):   return NotImplemented
  def __and__(self, other):      return NotImplemented
  def __xor__(self, other):      return NotImplemented
  def __or__(self, other):       return NotImplemented

class Mat:
  def __init__(self):
    # 
    self.yld  = None
    self.uts  = None
    self.emod = None

