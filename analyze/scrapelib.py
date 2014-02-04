# coding: utf-8

import types
import re
import logging
import os

logger=logging.getLogger(os.path.split(__file__)[1])


class AddToEditorChainClass :
	
	
	def __init__(self) :
		self._debug=False

    
	def __add__(self,o) :
        	def a(*args,**kwargs) :
            		return self(o(*args,**kwargs))
        	return a


	def makestring(self,a) :
		if type(a)==types.ListType :
			a="".join([unicode(b) for b in a])
		elif a is None :
			a=""
		return a
		
		
	def debug(self,state=None) :
		if state is not None :
			self._debug=state
		return self._debug


class TextEditor(AddToEditorChainClass):
	"""
	Takes List of Search / Replace Expressions
	d=TextEditor([("a","b"),("c","d")])

	d.process("maca") -> "mbdb"
	"""
	
	def __init__(self, ruleset) :
		AddToEditorChainClass.__init__(self)
		self.ruleset=[(re.compile(a[0]),a[1]) for a in ruleset]


	def edit(self,i) :
		i=self.makestring(i)
		if self.debug() :
			logger.debug("Start: %s" % repr(i))
		for r in self.ruleset :
			i=r[0].sub(r[1],i)
			if self.debug() :
				logger.debug("%s->%s : %s" % (r[0].pattern,r[1],repr(i))) 
			
		return i 

	def __call__(self,i) :
		return self.edit(i)




class TextParser(AddToEditorChainClass) :
	"""
	Takes List of Regexp. Will return combined groupdict() of matches
	
	"""


	def __init__(self, *ruleset) :
		AddToEditorChainClass.__init__(self)
		self.ruleset=[re.compile(a) for a in ruleset]


	def parse(self,i) :
		i=self.makestring(i)
		res={}
		for r in self.ruleset :
			m=r.search(i)
			if m :
				res.update(m.groupdict())
		return res 


	def __call__(self,i) :
		return self.parse(i)


