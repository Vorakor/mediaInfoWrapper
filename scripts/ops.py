#! /usr/bin/python

import os,sys,inspect
import time, datetime
import re
from os.path import split

def startEndTimer( format=None ):
	'''
	startEndTimer gives us the current time with the format that is specified within the 
		function, it gives us this time to use as either the start or end time for the 
		timer function
	'''
	if (format == None):
		timeFormat = '%Y-%m-%d %H:%M:%S'
	else:
		timeFormat = format
	time = datetime.datetime.now().strftime(timeFormat)
	return time

def timerPrintout( start, end ):
	'''
	timerPrintout subtracts the start time from the end time to give us a total time that 
		the task took to run, eventually it will print in human readable format...
	'''
	startTime = datetime.datetime.strptime(start, '%Y-%m-%d %H:%M:%S')
	endTime = datetime.datetime.strptime(end, '%Y-%m-%d %H:%M:%S')
	totalTime = endTime - startTime
	msg = "Your task took " + str(totalTime) + " minutes to complete"
	print msg
	return totalTime

def yOrN( msg ):
	print "\n" + msg + "\n"
	message = "Enter 'Y' or 'N' for yes or no:\n"
	option = getInput(message)
	if (option == 'Y' or option == 'y' or option == 'Yes' or option == 'yes'):
		return True
	elif (option == 'N' or option == 'n' or option == 'No' or option == 'no'):
		return False
	else:
		print "Invalid option, returning 'false'."
		return False

def getInput( msg ):
	print msg
	userInputVar = raw_input()
	return userInputVar

def printList( msg, arry ):
	print "\n" + msg + "\n"
	for i in arry:
		print "\t- " + i
	return

def printNumList( msg, arry ):
	print "\n" + msg + "\n"
	count = 1
	for i in arry:
		print "\t" + str(count) + "- " + i
		count += 1
	return

def multiOptions( msg, arry ):
	print "\n" + msg + "\n"
	count = 1
	for i in arry:
		print "\t" + str(count) + "- " + i
		count += 1
	message = "\nEnter the number of the option you want:\n"
	try:
		option = getInput(message)
		num = int(option)
		num -= 1
	except:
		num = 0
	return num

def findMatches( first, second ):
	'''
	findMatches is a function whose only purpose is to check if a value in the first array is 
		in the second array, if it finds them then it adds the matching items to two different 
		arrays and returns them
	'''
	arryOne = []
	arryTwo = []
	for i in first:
		for j in second:
			if i in j:
				arryOne.append(i)
				arryTwo.append(j)
	return arryOne, arryTwo

def removeDuplicates( first, second ):
	noDuplicatesArray = []
	for a in first:
		if a in noDuplicatesArray:
			continue
		else:
			noDuplicatesArray.append(a)
	for b in second:
		if b in noDuplicatesArray:
			continue
		else:
			noDuplicatesArray.append(b)
	return noDuplicatesArray

def curTime( format ):
	return datetime.datetime.now().strftime(format)

def getServer():
	vols = os.listdir('/Volumes/')
	if 'yellow' in vols:
		return 'yellow'
	elif 'Congo' in vols:
		return 'Congo'
	else:
		print 'Server not mounted'
		sys.exit(2)

def submitTractor( alfFileName ):
	command = "/Applications/Pixar/tractor-blade-1.6.5/tractor-spool.py " + alfFileName
	os.system(command)
	return

def multiOptionsRange( msg, arry ):
	'''
	multiOptionsRange allows the user to select a range from a printed list and it sends back 
		a list of indexes that were chosen
	Uses the following functions:	mpsinput.rangeList
	'''
	print "\n" + msg + "\n"
	count = 1
	for i in arry:
		print "\t" + str(count) + "- " + i
		count += 1
	message = "\nEnter the numbers of the options you want:\n"
	num = []
	try:
		option = rangeList(message)
		for o in option:
			tempnum = int(o)
			tempnum -= 1
			num.append(tempnum)
	except:
		num.append(0)
	return num

def rangeList(prompt=''):
	'''verifies the input from the user
	calls buildRange to return the list'''
	
	loop = True
	input = ''
	append = '\n\tYou can give a range description like "1-3, 5"\n'\
			 '\tand the following described indexes (1, 2, 3, 5) will be used \n'
	while loop:
		input = raw_input(prompt)
		loop = not vRangeList(input)
	return buildRangeList(input)

def buildRangeList(list_str):
	'''builds a list of numbers base on range description list (RDL)
	
		RDL: describes an index of numbers
		
			for example: "1-3, 5, 7-9" would return the list [1,2,3,5,7,8,9]
			
	:param list_str: must follow syntax <beg>[-<end>][, ... ]*
	:type list_str: string
	:rtype: list of type int'''
	
	rlist = []
	comma = list_str.split(',')
	for i in comma:
		beg = 0
		end = 0
		
		dash = i.split('-')
		if len(dash) == 1:
			beg = int(dash[0])
			end = int(dash[0])
		else:
			beg = int(dash[0])
			end = int(dash[1])
		
		for j in range(beg, end+1):
			rlist.append(j)
	
	return rlist

def vRangeList(arg):
	dash = '\d+(-\d+)?'
	reg = '^\s*' + dash + '(,\s*' + dash + ')*\s*$'
	#print reg
	check = re.compile(reg)
	return check.match(arg) != None

def stripColor(s):
	import re
	t = s[:]
	pat = re.compile('(\033\[(\d*;?)*m)')
	for r in pat.findall(s):
		s = s.replace(r[0],'')
	return s

class columnedList:
	'''stores strings and prints them out in neat columns'''
	def __init__(self, colNum, header=[]):
		''' give the number of columns to initialize'''
		self.rows = []
		self.colNum = colNum
		self.maxColWidths = []
		for i in range(colNum):
			self.maxColWidths.append(0)
		self.header = header
		for i,h in enumerate(header):
			self.maxColWidths[i] = max(self.maxColWidths[i], len(h))
			
	def size(self):
		return len(self.rows)
	
	def addRow(self, row, colored=False):
		''' add a row to the columned list
		:param row: a tuple of all strings
		:type row: tuple
		'''
		self.rows.append(row)
		for i, c in enumerate(row):
			clen = self.colLen(c)
			self.maxColWidths[i] = max(clen, self.maxColWidths[i])

	def addBlankRow(self):
		row = []
		for i in range(len(self.maxColWidths)):
			row.append(('',False))
		self.addRow(row)
	
	def width(self):
		return sum(self.maxColWidths) + len(self.maxColWidths)*3
	
	def listColumn(self, colNum):
		ret = []
		for row in self.rows:
			s = row[colNum]
			s = color.stripColor(s)
			ret.append(s)
		ret.sort()
		return ret
	
	def __str__(self):

		# Center the headers according to the maximum column width
		header_str = ''
		for i, h in enumerate(self.header):
			h_len = self.colLen(h)
			r_pad = (self.maxColWidths[i] - h_len)/2
			l_pad = self.maxColWidths[i] - h_len - r_pad

			header_str += ' '*l_pad + h + ' '*r_pad + '   '

# 		self.rows.sort()
		# Left justify the columns
		ret = header_str + '\n'
		for row in self.rows:
			row_str = ''
			for i, col in enumerate(row):
				col_len = self.colLen(col)
				self.maxColWidths[i]
				sPad = self.maxColWidths[i] - col_len
				row_str += col + ' '*sPad + '   '
			ret += row_str + '\n'
		return ret
	
	def colLen(self,c):
			return len(stripColor(str(c)))