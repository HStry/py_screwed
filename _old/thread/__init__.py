#!/usr/bin/env python3
import types
import warnings
import math
import datetime


from .. import stresses as screwed_stresses

class Thread:
  def __init__(self, standard=None, diameter=None, pitch=None, starts=None, name=None):
    # Tracking global and user provided values' modification time
    self.__UD = {"global":      datetime.datetime.utcnow(),
                 "standard":    None,  # Thread standard, e.g. ISO, ANSI etc.
                 "name":        None,  # Thread name
                 "diameter":    None,  # Nominal thread diameter
                 "pitch":       None,  # Thread pitch
                 "starts":      None,  # Number of thread starts
                 "taper":       None,  # Thread taper, e.g. for pipe threads
                 "angle":       None,  # Thread angle, e.g. 60 degrees for ISO
                 "leadangle":   None,  # Thread lead angle, e.g. 7 degrees for ANSI Buttress
                 "trailangle":  None,  # Thread trail angle, e.g. 45 degrees for ANSI Buttress
                 "height":      None,  # Thread height
                 "pitchoffset": None,  # Thread pitch offset from idealized profile center
                 "load":        None}  # Thread load
    # Tracking automatically created values' modification time
    self.__AD = {"profileheight":          None,
                 "_h1":                    None,
                 "_h2":                    None,
                 "_H1":                    None,
                 "_H2":                    None,
                 "m_crestwidth":           None,
                 "m_rootwidth":            None,
                 "m_rootarea":             None,
                 "f_crestwidth":           None,
                 "f_rootwidth":            None,
                 "f_crestarea":            None,
                 "threadloaddistribution": None,
                 "m_tau":                  None,
                 "f_tau":                  None,
                 "m_lsigma":               None,
                 "m_tsigma":               None,
                 "f_lsigma":               None,
                 "f_tsigma":               None,
                 "m_lvonmises":            None,
                 "m_tvonmises":            None,
                 "f_lvonmises":            None,
                 "f_tvonmises":            None}
    self.__DEFAULTS = {"starts":      1,
                       "taper":       0,
                       "pitchoffset": 0,}
    if pitch != None: self.pitch = pitch
    if diameter != None: self.diameter = diameter
    if starts != None: self.starts = starts
    if standard != None:
      if standard.lower() in ('iso', 'iso 261'):
        self.name          = name
        self.angle         = math.radians(60)
        self.pitchoffset   = lambda: (1/16) * self.profileheight
        self.height        = lambda: (5/8) * self.profileheight
      if standard.lower() in ('din 513', 'stub din 513', 'din 513 stub'):
        if 'stub' in standard.lower(): hf = (1/2)
        else:                       hf = (3/4)
        self.name          = name
        self.leadangle     = math.radians(3)
        self.trailangle    = math.radians(30)
        self.pitchoffset   = 0
        self.height        = lambda: hf * self.pitch
      if standard.lower() in ('acme stub', 'stub acme', 'acme'):
        self.name          = name
        if 'stub' in standard.lower(): hf = 0.3
        else:                       hf = 0.5
        self.angle         = math.radians(29)
        self.pitchoffset   = 0
        self.height        = lambda: hf * self.pitch
      if standard.lower() in ('ansi buttress'):
        if 'stub' in standard: hf = 0.4
        else:               hf = 0.6
        self.name          = name
        self.leadangle     = math.radians(7)
        self.trailangle    = math.radians(45)
        self.pitchoffset   = 0
        self.height        = lambda: hf * self.pitch
    else:
      pass
      # The parameter values below must be floats, integers or Pint units, except
      # for the handedness parameter. If Pint units are used, all values must
      # be pint units, including the values used in the screwed.Dim and 
      # screwed.Mat units.
#      self.name        = None   # Thread name
#      self.diameter    = None   # Nominal thread diameter
#      self.pitch       = None   # Thread pitch
#      self.length      = None   # Full thread engagement length
#      self.lead        = None   # Thread lead, int * pitch
#      self.height      = None   # Thread tooth height
#      self.angle       = None   # Thread tooth angle, exact sum of angles below
#      self.leadangle   = None   # Thread lead side angle, 0 <= x < 90
#      self.trailangle  = None   # Thread trail side angle, 0 <= x < 90
#      self.taper       = None   # Taper angle of thread
#      self.handedness  = 'r'    # Thread handedness, 'l' or 'r', usually 'r'.
#      self.pitchoffset = None   # Offset of tooth halfheight from pitch line
#      self.mdiameter   = None   # Inside diameter of male part, in case of threaded pipe.
#      self.fdiameter   = None   # Outside diameter of female part.
      
      # The dimensions below must be screwed.Dim units. Root always means
      # the inner part of the thread, and crest always the outer part of the
      # thread, unlike some thread nomenclature (e.g. ISO) dictates.
#      self.mroot      = None   # Root diameter of male part
#      self.mpitch     = None   # Pitch diameter of male part
#      self.mcrest     = None   # Crest diameter of male part
#      self.froot      = None   # Root diameter of female part
#      self.fpitch     = None   # Pitch diameter of female part
#      self.fcrest     = None   # Crest diameter of female part
      
      # The dimensions below must be screwed.Dim units. As above, root and
      # crest indicate the smallest and biggest diameters of the thread.
      # Lead indicates the right side of the male tooth, and trail the left
      # side, should the male part be pulled to the left, and the female part
      # pulled to the right.
#      self.mroot_leadradius    = None   # 
#      self.mroot_trailradius   = None   # 
#      self.mcrest_leadradius   = None   # 
#      self.mcrest_trailradius  = None   # 
#      self.froot_leadradius    = None   # 
#      self.froot_trailradius   = None   # 
#      self.fcrest_leadradius   = None   # 
#      self.fcrest_trailradius  = None   # 
      
      # The parameters below must be screwed.Mat units, with at least the yield
      # strength, ultimate tensile strength, and elasticity modulus provided.
#      self.bolt_material = None
#      self.nut_material = None
      
      # The safety factor is used to calculate the maximum load force of the
      # threaded connection. The safety factor type is set to which limit the
      # calculation is made. This can be 'y' or 'u' for yield strength or
      # ultimate tensile strength respectively.
#      self.sf      = None
#      self.sf_type = 'y'
  
#  if True:     # x property
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
  
  if True:     # FIXED UD name property
    @property
    def name(self):
      if self.__UD["name"] == None:
        try:
          return " - ".join([str(x) for x in [self.diameter, self.pitch, self.angle, self.leadangle] if x != None])
        except:
          return "Not enough information to construct a name. Supply more information, or a name."
      else:
        try:              return self.__name()
        except TypeError: return self.__name
        except:           raise
    @name.setter
    def name(self, val):
      self.__UD["global"] = datetime.datetime.utcnow()
      self.__UD["name"] = self.__UD["global"]
      self.__name = val
    @name.deleter
    def name(self):
      self.__UD["global"] = datetime.datetime.utcnow()
      self.__UD["name"] = None
      del(self.__name)
      pass
  if True:     # FIXED UD diameter property
    @property
    def diameter(self):
      if self.__UD["diameter"] != None:
        return self.__diameter
      else:
        raise AttributeError('\'diameter\' attribute not defined.')
    @diameter.setter
    def diameter(self, val):
      self.__UD["global"] = datetime.datetime.utcnow()
      self.__UD["diameter"] = self.__UD["global"]
      self.__diameter = val
    @diameter.deleter
    def diameter(self):
      self.__UD["global"] = datetime.datetime.utcnow()
      self.__UD["diameter"] = None
      del(self.__diameter)
  if True:     # FIXED UD pitch property
    @property
    def pitch(self):
      if self.__UD["pitch"] != None:
        return self.__pitch
      else:
        raise AttributeError('\'pitch\' attribute not defined.')
    @pitch.setter
    def pitch(self, val):
      self.__UD["global"] = datetime.datetime.utcnow()
      self.__UD["pitch"] = self.__UD["global"]
      self.__pitch = val
    @pitch.deleter
    def pitch(self):
      self.__UD["global"] = datetime.datetime.utcnow()
      self.__UD["pitch"] = None
      del(self.__pitch)
  if True:     # FIXED UD starts property
    @property
    def starts(self):
      if self.__UD["starts"] == None:
        warnings.warn('\'starts\' property not set. Using default value \'{}\'.'.format(self.__DEFAULTS["starts"]), SyntaxWarning)
        self.__starts = self.__DEFAULTS["starts"]
      return self.__starts
    @starts.setter
    def starts(self, val):
      if ((int(val) == val) and
          (val >= 1)):
        self.__UD["global"] = datetime.datetime.utcnow()
        self.__UD["starts"] = self.__UD["global"]
        self.__starts = int(val)
      else:
        raise AttributeError('\'starts\' attribute should be an integer larger or equal to 1')
    @starts.deleter
    def starts(self):
      self.__UD["global"] = datetime.datetime.utcnow()
      self.__UD["starts"] = None
      del(self.__starts)
  if True:     # FIXED -- lead property
    @property
    def lead(self):
      return self.starts * self.pitch
    @lead.setter
    def lead(self, val):
      warnings.warn('\'lead\' property should not be explicitly modified. Attempting to set Thread.starts property instead.', SyntaxWarning)
      self.starts = val / self.pitch
    @lead.deleter
    def lead(self):
      raise AttributeError('\'lead\' property cannot be explicitly deleted.')
  if True:     # FIXED UD angle property
    @property
    def angle(self):
      if self.__UD["angle"] != None:
        return self.__angle
      elif ((self.__UD["leadangle"] != None) and
            (self.__UD["trailangle"] != None)):
        return self.leadangle + self.trailangle
      else:
        raise AttributeError('\'angle\' attribute neither explicitly nor implicitly defined.')
    @angle.setter
    def angle(self, val):
      if ((self.__UD["leadangle"] != None) and
          (self.__UD["trailangle"] != None)):
        raise AttributeError('\'angle\' attribute already implicitly defined.')
      elif (val >= 0 and val < math.pi):
        self.__UD["global"] = datetime.datetime.utcnow()
        self.__UD["angle"] = self.__UD["global"]
        self.__angle = val
      else:
        raise ValueError('value out of bounds. 0 <= val < \u03c0')
    @angle.deleter
    def angle(self):
      self.__UD["global"] = datetime.datetime.utcnow()
      self.__UD["angle"] = None
      del(self.__angle)
  if True:     # FIXED UD leadangle property
    @property
    def leadangle(self):
      if self.__UD["leadangle"] != None:
        return self.__leadangle
      elif ((self.__UD["angle"] != None) and
            (self.__UD["trailangle"] != None)):
        return self.angle - self.trailangle
      elif self.__UD["angle"] != None:
        return self.angle / 2
      else:
        raise AttributeError('\'leadangle\' attribute neither explicitly nor implicitly defined.')
    @leadangle.setter
    def leadangle(self, val):
      if ((self.__UD["angle"] != None) and
          (self.__UD["trailangle"] != None)):
        raise AttributeError('\'leadangle\' attribute already implicitly defined.')
      elif (val >= 0 and val < math.pi/2):
        self.__UD["global"] = datetime.datetime.utcnow()
        self.__UD["leadangle"] = self.__UD["global"]
        self.__leadangle = val
      else:
        raise ValueError('value out of bounds. 0 <= val < \u03c0/2')
    @leadangle.deleter
    def leadangle(self):
      self.__UD["global"] = datetime.datetime.utcnow()
      self.__UD["leadangle"] = None
      del(self.__leadangle)
  if True:     # FIXED UD trailangle property
    @property
    def trailangle(self):
      if self.__UD["trailangle"] != None:
        return self.__trailangle
      elif ((self.__UD["angle"] != None) and
            (self.__UD["leadangle"] != None)):
        return self.angle - self.leadangle
      elif self.__UD["angle"] != None:
        return self.angle / 2
      else:
        raise AttributeError('\'trailangle\' attribute neither explicitly nor implicitly defined.')
    @trailangle.setter
    def trailangle(self, val):
      if ((self.__UD["angle"] != None) and
          (self.__UD["leadangle"] != None)):
        raise AttributeError('\'trailangle\' attribute already implicitly defined.')
      elif (val >= 0 and val < math.pi/2):
        self.__UD["global"] = datetime.datetime.utcnow()
        self.__UD["trailangle"] = self.__UD["global"]
        self.__trailangle = val
      else:
        raise ValueError('value out of bounds. 0 <= val < \u03c0/2')
    @trailangle.deleter
    def trailangle(self):
      self.__UD["global"] = datetime.datetime.utcnow()
      self.__UD["trailangle"] = None
      del( self.__trailangle)
  
  if True:     # FIXED AD profileheight property
    @property
    def profileheight(self):
      if ((self.__AD["profileheight"] == None) or
          (self.__AD["profileheight"] <= self.__UD["global"])):
        self.__AD["profileheight"] = datetime.datetime.utcnow()
        self.__profileheight = self.pitch / (math.tan(self.leadangle) + math.tan(self.trailangle))
      return self.__profileheight
    @profileheight.setter
    def profileheight(self, val):
      raise AttributeError('\'profileheight\' property cannot be explicitly set.')
    @profileheight.deleter
    def profileheight(self):
      raise AttributeError('\'profileheight\' property cannot be explicitly deleted.')
  if True:     # FIXED UD pitchoffset property
    @property
    def pitchoffset(self):
      """The pitch offset of the thread can be expressed as a pure dimension or a simple function without arguments"""
      if self.__UD["pitchoffset"] == None:
        warnings.warn('\'pitchoffset\' property not set. Using default value \'{}\'.'.format(self.__DEFAULTS["pitchoffset"]), SyntaxWarning)
        self.__pitchoffset = self.__DEFAULTS["pitchoffset"]
      try:              return self.__pitchoffset()
      except TypeError: return self.__pitchoffset
      except:           raise
    @pitchoffset.setter
    def pitchoffset(self, val):
      self.__UD["global"] = datetime.datetime.utcnow()
      self.__UD["pitchoffset"] = self.__UD["global"]
      self.__pitchoffset = val
    @pitchoffset.deleter
    def pitchoffset(self):
      self.__UD["global"] = datetime.datetime.utcnow()
      self.__UD["pitchoffset"] = None
      del(self.__pitchoffset)
  if True:     # FIXED UD height property
    @property
    def height(self):
      """The height of the thread can be expressed as a pure dimension or a simple function without arguments"""
      if self.__UD["height"] == None:
        raise AttributeError('\'height\' parameter not defined')
      try:              return self.__height()
      except TypeError: return self.__height
      except:           raise
    @height.setter
    def height(self, val):
      self.__UD["global"] = datetime.datetime.utcnow()
      self.__UD["height"] = self.__UD["global"]
      self.__height = val
    @height.deleter
    def height(self):
      self.__UD["global"] = datetime.datetime.utcnow()
      self.__UD["height"] = None
      del(self.__height)
  
  if True:     # FIXED AD _h1 property
    @property
    def _h1(self):
      """Distance between crest point of saw-tooth profile and crest of thread."""
      if ((self.__AD["_h1"] == None) or
          (self.__AD["_h1"] <= self.__UD["global"])):
        self.__AD["_h1"] = datetime.datetime.utcnow()
        self.__h1 = self.profileheight/2 - self.pitchoffset - self.height/2
      return self.__h1
    @_h1.setter
    def _h1(self, val):
      raise AttributeError('\'_h1\' property cannot be explicitly set.')
    @_h1.deleter
    def _h1(self):
      raise AttributeError('\'_h1\' property cannot be explicitly deleted.')
  if True:     # FIXED AD _h2 property
    @property
    def _h2(self):
      """Distance between crest point of saw-tooth profile and root of thread."""
      if ((self.__AD["_h2"] == None) or
          (self.__AD["_h2"] <= self.__UD["global"])):
        self.__AD["_h2"] = datetime.datetime.utcnow()
        self.__h2 = self.profileheight/2 - self.pitchoffset + self.height/2
      return self.__h2
    @_h2.setter
    def _h2(self, val):
      raise AttributeError('\'_h2\' property cannot be explicitly set.')
    @_h2.deleter
    def _h2(self):
      raise AttributeError('\'_h2\' property cannot be explicitly deleted.')
  if True:     # FIXED AD _H1 property
    @property
    def _H1(self):
      """Distance between root point of saw-tooth profile and crest of thread."""
      if ((self.__AD["_H1"] == None) or
          (self.__AD["_H1"] <= self.__UD["global"])):
        self.__AD["_H1"] = datetime.datetime.utcnow()
        self.__H1 = self.profileheight/2 + self.pitchoffset + self.height/2
      return self.__H1
    @_H1.setter
    def _H1(self, val):
      raise AttributeError('\'_H1\' property cannot be explicitly set.')
    @_H1.deleter
    def _H1(self):
      raise AttributeError('\'_H1\' property cannot be explicitly deleted.')
  if True:     # FIXED AD _H2 property
    @property
    def _H2(self):
      """Distance between root point of saw-tooth profile and root of thread."""
      if ((self.__AD["_H2"] == None) or
          (self.__AD["_H2"] <= self.__UD["global"])):
        self.__AD["_H2"] = datetime.datetime.utcnow()
        self.__H2 = self.profileheight/2 + self.pitchoffset - self.height/2
      return self.__H2
    @_H2.setter
    def _H2(self, val):
      raise AttributeError('\'_H2\' property cannot be explicitly set.')
    @_H2.deleter
    def _H2(self):
      raise AttributeError('\'_H2\' property cannot be explicitly deleted.')
  if True:     # FIXED AD m_crestwidth property
    @property
    def m_crestwidth(self):
      if ((self.__AD["m_crestwidth"] == None) or
          (self.__AD["m_crestwidth"] <= self.__UD["global"])):
        self.__AD["m_crestwidth"] = datetime.datetime.utcnow()
        self.__m_crestwidth = self._h1 * (math.tan(self.leadangle) + math.tan(self.trailangle))
      return self.__m_crestwidth
    @m_crestwidth.setter
    def m_crestwidth(self, val):
      raise AttributeError('\'m_crestwidth\' property cannot be explicitly set.')
    @m_crestwidth.deleter
    def m_crestwidth(self):
      raise AttributeError('\'m_crestwidth\' property cannot be explicitly deleted.')
  if True:     # FIXED AD m_rootwidth property
    @property
    def m_rootwidth(self):
      if ((self.__AD["m_rootwidth"] == None) or
          (self.__AD["m_rootwidth"] <= self.__UD["global"])):
        self.__AD["m_rootwidth"] = datetime.datetime.utcnow()
        self.__m_rootwidth = self._h2 * (math.tan(self.leadangle) + math.tan(self.trailangle))
      return self.__m_rootwidth
    @m_rootwidth.setter
    def m_rootwidth(self, val):
      raise AttributeError('\'m_rootwidth\' property cannot be explicitly set.')
    @m_rootwidth.deleter
    def m_rootwidth(self):
      raise AttributeError('\'m_rootwidth\' property cannot be explicitly deleted.')
  if True:     # FIXED AD m_rootarea property
    @property
    def m_rootarea(self):
      if ((self.__AD["m_rootarea"] == None) or
          (self.__AD["m_rootarea"] <= self.__UD["global"])):
        self.__AD["m_rootarea"] = datetime.datetime.utcnow()
        self.__m_rootarea = self.m_rootwidth * 2*math.pi * ((self.diameter - 2*self.height)/2)
      return self.__m_rootarea
    @m_rootarea.setter
    def m_rootarea(self, val):
      raise AttributeError('\'m_rootarea\' property cannot be explicitly set.')
    @m_rootarea.deleter
    def m_rootarea(self):
      raise AttributeError('\'m_rootarea\' property cannot be explicitly deleted.')
  if True:     # FIXED AD f_crestwidth property
    @property
    def f_crestwidth(self):
      if ((self.__AD["f_crestwidth"] == None) or
          (self.__AD["f_crestwidth"] <= self.__UD["global"])):
        self.__AD["f_crestwidth"] = datetime.datetime.utcnow()
        self.__f_crestwidth = self._H1 * (math.tan(self.leadangle) + math.tan(self.trailangle))
      return self.__f_crestwidth
    @f_crestwidth.setter
    def f_crestwidth(self, val):
      raise AttributeError('\'f_crestwidth\' property cannot be explicitly set.')
    @f_crestwidth.deleter
    def f_crestwidth(self):
      raise AttributeError('\'f_crestwidth\' property cannot be explicitly deleted.')
  if True:     # FIXED AD f_rootwidth property
    @property
    def f_rootwidth(self):
      if ((self.__AD["f_rootwidth"] == None) or
          (self.__AD["f_rootwidth"] <= self.__UD["global"])):
        self.__AD["f_rootwidth"] = datetime.datetime.utcnow()
        self.__f_rootwidth = self._H2 * (math.tan(self.leadangle) + math.tan(self.trailangle))
      return self.__f_rootwidth
    @f_rootwidth.setter
    def f_rootwidth(self, val):
      raise AttributeError('\'f_rootwidth\' property cannot be explicitly set.')
    @f_rootwidth.deleter
    def f_rootwidth(self):
      raise AttributeError('\'f_rootwidth\' property cannot be explicitly deleted.')
  if True:     # FIXED AD f_crestarea property
    @property
    def f_crestarea(self):
      if ((self.__AD["f_crestarea"] == None) or
          (self.__AD["f_crestarea"] <= self.__UD["global"])):
        self.__AD["f_crestarea"] = datetime.datetime.utcnow()
        self.__f_crestarea = self.f_crestwidth * 2*math.pi * (self.diameter/2)
      return self.__f_crestarea
    @f_crestarea.setter
    def f_crestarea(self, val):
      raise AttributeError('\'f_crestarea\' property cannot be explicitly set.')
    @f_crestarea.deleter
    def f_crestarea(self):
      raise AttributeError('\'f_crestarea\' property cannot be explicitly deleted.')

  if True:     # FIXED UD load property
    @property
    def load(self):
      if self.__UD["load"] != None:
        try:              return self.__load()
        except TypeError: return self.__load
        except:           raise
      else:
        raise AttributeError('\'load\' attribute not defined.')
    @load.setter
    def load(self, val):
      self.__UD["global"] = datetime.datetime.utcnow()
      self.__UD["load"] = self.__UD["global"]
      self.__load = val
    @load.deleter
    def load(self):
      self.__UD["global"] = datetime.datetime.utcnow()
      self.__UD["load"] = None
      del(self.__load)
  if True:     # INCOMPLETE AD threadloaddistribution property
    @property
    def threadloaddistribution(self):
      return (.6, .2, .1, .05, .025)
    @threadloaddistribution.setter
    def threadloaddistribution(self, val):
      raise AttributeError('\'threadloaddistribution\' property cannot be explicitly set.')
    @threadloaddistribution.deleter
    def threadloaddistribution(self):
      raise AttributeError('\'threadloaddistribution\' property cannot be explicitly deleted.')
  
  if True:     # AD m_tau property
    @property
    def m_tau(self):
      """"Shear stress on root of male tooth"""
      if ((self.__AD["m_tau"] == None) or
          (self.__AD["m_tau"] <= self.__UD["global"])):
        self.__AD["m_tau"] = datetime.datetime.utcnow()
        self.__m_tau = max(self.threadloaddistribution) * self.load / self.m_rootarea
      return self.__m_tau
    @m_tau.setter
    def m_tau(self, val):
      raise AttributeError('\'m_tau\' property cannot be explicitly set.')
    @m_tau.deleter
    def m_tau(self):
      raise AttributeError('\'m_tau\' property cannot be explicitly deleted.')
  if True:     # AD f_tau property
    @property
    def f_tau(self):
      if ((self.__AD["f_tau"] == None) or
          (self.__AD["f_tau"] <= self.__UD["global"])):
        self.__AD["f_tau"] = datetime.datetime.utcnow()
        self.__f_tau = max(self.threadloaddistribution) * self.load / self.f_crestarea
      return self.__f_tau
    @f_tau.setter
    def f_tau(self, val):
      raise AttributeError('\'f_tau\' property cannot be explicitly set.')
    @f_tau.deleter
    def f_tau(self):
      raise AttributeError('\'f_tau\' property cannot be explicitly deleted.')
  if True:     # AD m_lsigma property
    @property
    def m_lsigma(self):
      if ((self.__AD["m_lsigma"] == None) or
          (self.__AD["m_lsigma"] <= self.__UD["global"])):
        self.__AD["m_lsigma"] = datetime.datetime.utcnow()
        self.__m_lsigma = (-1 * self.load * math.sin(self.leadangle) / math.cos(self.leadangle) + self.load * self.height / ((2/3) * self.m_rootwidth)) / self.m_rootarea
      return self.__m_lsigma
    @m_lsigma.setter
    def m_lsigma(self, val):
      raise AttributeError('\'m_lsigma\' property cannot be explicitly set.')
    @m_lsigma.deleter
    def m_lsigma(self):
      raise AttributeError('\'m_lsigma\' property cannot be explicitly deleted.')
  if True:     # AD m_tsigma property
    @property
    def m_tsigma(self):
      if ((self.__AD["m_tsigma"] == None) or
          (self.__AD["m_tsigma"] <= self.__UD["global"])):
        self.__AD["m_tsigma"] = datetime.datetime.utcnow()
        self.__m_tsigma = (-1 * self.load * math.sin(self.leadangle) / math.cos(self.leadangle)) / self.m_rootarea
      return self.__m_tsigma
    @m_tsigma.setter
    def m_tsigma(self, val):
      raise AttributeError('\'m_tsigma\' property cannot be explicitly set.')
    @m_tsigma.deleter
    def m_tsigma(self):
      raise AttributeError('\'m_tsigma\' property cannot be explicitly deleted.')
  if True:     # AD f_lsigma property
    @property
    def f_lsigma(self):
      if ((self.__AD["f_lsigma"] == None) or
          (self.__AD["f_lsigma"] <= self.__UD["global"])):
        self.__AD["f_lsigma"] = datetime.datetime.utcnow()
        self.__f_lsigma = (-1 * self.load * math.sin(self.leadangle) / math.cos(self.leadangle) + self.load * self.height / ((2/3) * self.f_crestwidth)) / self.f_crestarea
      return self.__f_lsigma
    @f_lsigma.setter
    def f_lsigma(self, val):
      raise AttributeError('\'f_lsigma\' property cannot be explicitly set.')
    @f_lsigma.deleter
    def f_lsigma(self):
      raise AttributeError('\'f_lsigma\' property cannot be explicitly deleted.')
  if True:     # AD f_tsigma property
    @property
    def f_tsigma(self):
      if ((self.__AD["f_tsigma"] == None) or
          (self.__AD["f_tsigma"] <= self.__UD["global"])):
        self.__AD["f_tsigma"] = datetime.datetime.utcnow()
        self.__f_tsigma = (-1 * self.load * math.sin(self.leadangle) / math.cos(self.leadangle)) / self.f_crestarea
      return self.__f_tsigma
    @f_tsigma.setter
    def f_tsigma(self, val):
      raise AttributeError('\'f_tsigma\' property cannot be explicitly set.')
    @f_tsigma.deleter
    def f_tsigma(self):
      raise AttributeError('\'f_tsigma\' property cannot be explicitly deleted.')
  if True:     # AD m_lvonmises property
    @property
    def m_lvonmises(self):
      if ((self.__AD["m_lvonmises"] == None) or
          (self.__AD["m_lvonmises"] <= self.__UD["global"])):
        self.__AD["m_lvonmises"] = datetime.datetime.utcnow()
        self.__m_lvonmises = screwed_stresses.von_mises(sx=self.m_lsigma, txy=self.m_tau)
      return self.__m_lvonmises
    @m_lvonmises.setter
    def m_lvonmises(self, val):
      raise AttributeError('\'m_lvonmises\' property cannot be explicitly set.')
    @m_lvonmises.deleter
    def m_lvonmises(self):
      raise AttributeError('\'m_lvonmises\' property cannot be explicitly deleted.')
  if True:     # AD m_tvonmises property
    @property
    def m_tvonmises(self):
      if ((self.__AD["m_tvonmises"] == None) or
          (self.__AD["m_tvonmises"] <= self.__UD["global"])):
        self.__AD["m_tvonmises"] = datetime.datetime.utcnow()
        self.__m_tvonmises = screwed_stresses.von_mises(sx=self.m_tsigma, txy=self.m_tau)
      return self.__m_tvonmises
    @m_tvonmises.setter
    def m_tvonmises(self, val):
      raise AttributeError('\'m_tvonmises\' property cannot be explicitly set.')
    @m_tvonmises.deleter
    def m_tvonmises(self):
      raise AttributeError('\'m_tvonmises\' property cannot be explicitly deleted.')
  if True:     # AD f_lvonmises property
    @property
    def f_lvonmises(self):
      if ((self.__AD["f_lvonmises"] == None) or
          (self.__AD["f_lvonmises"] <= self.__UD["global"])):
        self.__AD["f_lvonmises"] = datetime.datetime.utcnow()
        self.__f_lvonmises = screwed_stresses.von_mises(sx=self.f_lsigma, txy=self.f_tau)
      return self.__f_lvonmises
    @f_lvonmises.setter
    def f_lvonmises(self, val):
      raise AttributeError('\'f_lvonmises\' property cannot be explicitly set.')
    @f_lvonmises.deleter
    def f_lvonmises(self):
      raise AttributeError('\'f_lvonmises\' property cannot be explicitly deleted.')
  if True:     # AD f_tvonmises property
    @property
    def f_tvonmises(self):
      if ((self.__AD["f_tvonmises"] == None) or
          (self.__AD["f_tvonmises"] <= self.__UD["global"])):
        self.__AD["f_tvonmises"] = datetime.datetime.utcnow()
        self.__f_tvonmises = screwed_stresses.von_mises(sx=self.f_tsigma, txy=self.f_tau)
      return self.__f_tvonmises
    @f_tvonmises.setter
    def f_tvonmises(self, val):
      raise AttributeError('\'f_tvonmises\' property cannot be explicitly set.')
    @f_tvonmises.deleter
    def f_tvonmises(self):
      raise AttributeError('\'f_tvonmises\' property cannot be explicitly deleted.')
  



  def check(self):
    if ((self._h1 < 0) or (self._h2 < 0) or
        (self._H1 < 0) or (self._H2 < 0)):
      warnings.warn("Impossible thread geometry provided.", UserWarning)
      return False
    else:
      return True
  
  # if True:     #  property
  # if True:     #  property
  # if True:     #  property
  # if True:     #  property
  # if True:     #  property
  # if True:     #  property
  # if True:     #  property
  # if True:     #  property
  # if True:     #  property
  # if True:     #  property
  # if True:     #  property
  # if True:     #  property
  
  def print_stresses(self):
    # self.mtau = self.maxthreadload() * load / self.m_rootarea
    # self.ftau = self.maxthreadload() * load / self.f_crestarea
    # self.mlsigma = (-1 * load * math.sin(self.leadangle) / math.cos(self.leadangle) + load * self.height / ((2/3) * self.m_rootwidth)) / self.m_rootarea
    # self.mtsigma = (-1 * load * math.sin(self.leadangle) / math.cos(self.leadangle)) / self.m_rootarea
    # self.flsigma = (-1 * load * math.sin(self.leadangle) / math.cos(self.leadangle) + load * self.height / ((2/3) * self.f_crestwidth)) / self.f_crestarea
    # self.ftsigma = (-1 * load * math.sin(self.leadangle) / math.cos(self.leadangle)) / self.f_crestarea
    # self.mlvonmises = screwed_stresses.von_mises(sx=self.mlsigma, txy=self.mtau)
    # self.mtvonmises = screwed_stresses.von_mises(sx=self.mtsigma, txy=self.mtau)
    # self.flvonmises = screwed_stresses.von_mises(sx=self.flsigma, txy=self.ftau)
    # self.ftvonmises = screwed_stresses.von_mises(sx=self.ftsigma, txy=self.ftau)
    try:
      print('\n{}'.format(self.name))
      print('outer diameter:    {:9.3f~P}'.format(self.diameter.to('mm')))
      print('inner diameter:    {:9.3f~P}'.format((self.diameter - 2*self.height).to('mm')))
      print('\nMale thread part:')
      print('shear:             {:9.3f~P}'.format(self.m_tau.to('MPa')))
      print('stress (lead):     {:9.3f~P}'.format(self.m_lsigma.to('MPa')))
      print('stress (trail):    {:9.3f~P}'.format(self.m_tsigma.to('MPa')))
      print('von mises (lead):  {:9.3f~P}'.format(self.m_lvonmises.to('MPa')))
      print('von mises (trail): {:9.3f~P}'.format(self.m_tvonmises.to('MPa')))
      print('\nFemale thread part:')
      print('shear:             {:9.3f~P}'.format(self.f_tau.to('MPa')))
      print('stress (lead):     {:9.3f~P}'.format(self.f_lsigma.to('MPa')))
      print('stress (trail):    {:9.3f~P}'.format(self.f_tsigma.to('MPa')))
      print('von mises (lead):  {:9.3f~P}'.format(self.f_lvonmises.to('MPa')))
      print('von mises (trail): {:9.3f~P}'.format(self.f_tvonmises.to('MPa')))
    except:
      pass
      





 
      