#! /usr/bin/python

import locale
import os,sys,inspect
import time, re
import datetime, socket
import argparse
import subprocess
import commands

from config import *
import ops as miOps

#	Goals:
#	1.	Allow user to select category to retrieve information from
#	2.	Allow user to select detail requests that they would like information from
#	3.	Allow user to select all detail requests in a given category
#	4.	Allow user to select all categories and specific detail requests in each
#	5.	Allow user to select all categories and all detail requests from each
#	6.	Run in prompt mode
#	7.	Run in quiet mode
#	8.	If called from command line and no further arguments are passed in then this script 
#			needs to ascertain which categories the user wants information from and what 
#			information they would like from each category
#	9.	This script can be provided all the information that the user wants and from which 
#			category, script will assume that user wants specified detail requests from each 
#			specified category, this functionality is available in quiet or prompt modes

def main():
	if (len(sys.argv) == 1):
		msg = 'Please enter a media file to get the information from it: '
		selection = miOps.getInput(msg)
		selection = selection.rstrip()
		selection = selection.lstrip()
		return mIWrap(False, selection)
	else:
		args, parser = usage()
		return detArgs(args, parser)

def detArgs( args, parser ):
	quiet = args.quiet
	file = None
	all = None
	category = None
	request = None
	if args.quiet == True:
		if not args.file:
			raise ArgumentException('Error: no file specified --> detArgs() line: ' + str(lineno()))
		else:
			file = args.file[0]
			if args.all == True:
				all = True
				if not args.category:
					if not args.request:
						category = MICATEGORIES
					else:
						#Don't forget that the user can also put in 'category';'request'
						check = checkForCatReq(args.request)
						if check == True:
							tempReq, noCatReq = getCatReq(args.request)
							for r in noCatReq:
								concat = 'All;' + r
								tempReq.append(concat)
							request = tempReq
						else:
							tempReq = []
							for r in args.request:
								concat = 'All;' + r
								tempReq.append(concat)
							request = tempReq
				else:
					category = args.category
			else:
				if not args.category:
					if not args.request:
						pass
					else:
						check = checkForCatReq(args.request)
						if check == True:
							request, noCatReq = getCatReq(args.request)
							if not noCatReq:
								pass
							else:
								raise ArgumentException('Error: partial list completion --> detArgs() line: ' + str(lineno()))
						else:
							raise ArgumentException('Error: no category specified --> detArgs() line: ' + str(lineno()))
				else:
					category = args.category
					if not args.request:
						pass
					else:
						check = checkForCatReq(args.request)
						if check == True:
							tempReq, noCatReq = getCatReq(args.request)
							for r in noCatReq:
								for c in category:
									concat = c + ';' + r
									tempReq.append(concat)
							request = tempReq
						else:
							tempReq = []
							for r in args.request:
								for c in category:
									concat = c + ';' + r
									tempReq.append(concat)
							request = tempReq
		return mIWrap(quiet, file, all, category, request)
	else:
		if not args.file:
			msg = 'Please enter a media file to get the information from it: '
			selection = miOps.getInput(msg)
			selection = selection.rstrip()
			selection = selection.lstrip()
			file = selection
		else:
			file = args.file[0]
		if args.all == True:
			all = True
			if not args.category:
				if not args.request:
					pass
				else:
					check = checkForCatReq(args.request)
					if check == True:
						tempReq, noCatReq = getCatReq(args.request)
						for r in noCatReq:
							concat = 'All;' + r
							tempReq.append(concat)
						request = tempReq
					else:
						tempReq = []
						for r in args.request:
							concat = 'All;' + r
							tempReq.append(concat)
						request = tempReq
			else:
				category = args.category
		else:
			if not args.category:
				if not args.request:
					pass
				else:
					check = checkForCatReq(args.request)
					if check == True:
						tempReq, noCatReq = getCatReq(args.request)
						for r in noCatReq:
							concat = 'None;' + r
							tempReq.append(concat)
						request = tempReq
					else:
						tempReq = []
						for r in args.request:
							concat = 'None;' + r
							tempReq.append(concat)
						request = tempReq
			else:
				category = args.category
				if not args.request:
					pass
				else:
					check = checkForCatReq(args.request)
					if check == True:
						tempReq, noCatReq = getCatReq(args.request)
						for r in noCatReq:
							for c in category:
								concat = c + ';' + r
								tempReq.append(concat)
						request = tempReq
					else:
						tempReq = []
						for r in args.request:
							for c in category:
								concat = c + ';' + r
								tempReq.append(concat)
						request = tempReq
		return mIWrap(quiet, file, all, category, request)

def checkForCatReq( args ):
	a = re.compile(r'\w(;)\w')
	count = 0
	for req in args:
		b = re.search(a, req)
		if (b == None or str(b) == 'None'):
			length = len(args) - 1
			if count == length:
				return False
			else:
				count += 1
				continue
		else:
			return True

def getCatReq( args ):
	request = []
	noCatReq = []
	a = re.compile(r'\w(;)\w')
	for req in args:
		b = re.search(a, req)
		if (b == None or str(b) == 'None'):
			noCatReq.append(req)
		else:
			request.append(req)
	return request, noCatReq

def required_length(nmin,nmax):
    class RequiredLength(argparse.Action):
        def __call__(self, parser, args, values, option_string=None):
            if not nmin<=len(values)<=nmax:
                msg='argument "{f}" requires between {nmin} and {nmax} arguments'.format(
                    f=self.dest,nmin=nmin,nmax=nmax)
                raise argparse.ArgumentTypeError(msg)
            setattr(args, self.dest, values)
    return RequiredLength

def usage():
	parser = argparse.ArgumentParser(description='''MediaInfoWrapper is simply a wrapper application written
			in Python, its purpose is to allow any function to call the wrapper and extract the information 
			it needs from a media file in the form of variables that can then be used in other scripts and 
			programs''')
	parser.add_argument('-q', '--quiet', dest="quiet", action="store_true", help='''This flag specifies that 
			we do not want to run mediaInfoWrapper in verbose mode, so we will provide all of the necessary 
			information before hand to skip all of the prompts and still do what we want it to do''')
	parser.add_argument('-f', '--file', dest="file", nargs=1, help='''This flag specifies the file that we are 
			getting information from, this should be a media file (ie. music file, movie file, or image file)''')
	parser.add_argument('-a', '--all', action="store_true", dest='all', help='''This flag, if used alone, will 
			get all available information on the media file from every category, if it is used with the 
			category flag then it will get all information as pertains to that category''')
	parser.add_argument('-c', '--category', dest="category", nargs='*', action=required_length(0, 6), help='''
			This flag specifies which categories that you would like information to, this flag can be used 
			with the -a flag to give all information out of a single or multiple categories, or with the -r 
			flag to specify specific details from the categories specified''')
	parser.add_argument('-r', '--request', dest="request", nargs='*', help='''This flag will be treated 
			differently depending on how the -a flag is used, but otherwise it will specify which details 
			you would like from mediaInfo, if used alone the wrapper will gather these specific details from 
			all categories, otherwise the wrapper will gather specified details from specified categories, you 
			can also enter the requests by doing a 'category';'request' format, this will tell the parser 
			specifically what you want from what category.  The categories are as follows: General, Video, 
			Audio, Text, Other (currently unavailable), Image, Menu, All''')
	args = parser.parse_args()
	return args, parser

class ArgumentException(Exception):
	def __init__(self,value):
		self.value = value
	def __str__(self):
		return repr(self.value)

def lineno():
    '''Returns the current line number in the program'''
    return inspect.currentframe().f_back.f_lineno

def mIWrap( quiet, file, all=None, category=None, detailRequests=None ):
	general_array = {}
	video_array = {}
	audio_array = {}
	text_array = {}
#	other_array = {}#This doesn't apply right now as it isn't working properly
	image_array = {}
	menu_array = {}
	allCat = False
	allDetReq = False
	if quiet == True:
		if not category:
			raise ArgumentException('Error: no category specified --> mIWrap() line: ' + str(lineno()))
		else:
			for c in category:
				if c in MICATEGORIES:
					pass
				else:
					raise ArgumentException('Error: invalid category --> mIWrap() line: ' + str(lineno()))
		if all == None:
			all = False
		else:
			if isinstance(all, bool):
				pass
			else:
				raise ArgumentException('Error: invalid variable type --> mIWrap() line: ' + str(lineno()))
		if not detailRequests:
			if all == False:
				raise ArgumentException('Error: no requests specified --> mIWrap() line: ' + str(lineno()))
			else:
				pass
		else:
			for dr in detailRequests:
				dSplit = dr.split(';')
				cat = dSplit[0]
				req = dSplit[1]
				if cat == 'all' or cat == 'All' or cat == 'ALL':
					drIndex = detailRequests.index(dr)
					newDr = remAllCategory(quiet, dr)
					del detailRequests[drIndex]
					for n in newDr:
						detailRequests.append(n)
				else:
					if cat in MICATEGORIES:
						valid = valid_detail_specifier(cat, req)
						if valid == True:
							pass
						else:
							raise ArgumentException('Error: invalid request specifier --> mIWrap() line: ' + str(lineno()))
					else:
						raise ArgumentException('Error: invalid category --> mIWrap() line: ' + str(lineno()))
	else:
		if not category:
			category = getCategory()
		else:
			for c in category:
				if c in MICATEGORIES:
					pass
				else:
					raise ArgumentException('Error: invalid category --> mIWrap() line: ' + str(lineno()))
		if all == None:
			allCat, allDetReq = detAll()
			if allCat == True or allDetReq == True:
				all = True
			else:
				all = False
		else:
			if isinstance(all, bool):
				pass
			else:
				if not category and not detailRequests:
					all = True
					allCat = True
					allDetReq = True
				elif not category and len(detailRequests) > 0:
					all = True
					allCat = False
					allDetReq = True
				elif len(category) > 0 and not detailRequests:
					all = False
					allCat = False
					allDetReq = False
				else:
					all = False
					allCat = False
					allDetReq = False
		if not detailRequests:
			if all == True:
				if allCat == True and allDetReq == True:
					pass
				elif allCat == False and allDetReq == True:
					detailRequests = getDetailRequests(True)
				else:
					pass
			else:
				if len(category) == 1:
					detailRequests = getDetailRequests(None, category[0])
				else:
					detailRequests = getDetailRequests()
		else:
			# If category is equal to all then this needs to pass to another function that will get rid of the 'all' category
			for dr in detailRequests:
				dSplit = dr.split(';')
				cat = dSplit[0]
				req = dSplit[1]
				if cat == 'all' or cat == 'All' or cat == 'ALL':
					drIndex = detailRequests.index(dr)
					newDr = remAllCategory(quiet, dr)
					del detailRequests[drIndex]
					for n in newDr:
						detailRequests.append(n)
				elif cat == 'none' or cat == 'None' or cat == 'NONE':
					drIndex = detailRequests.index(dr)
					newDr = remNoneCategory(dr)
					del detailRequests[drIndex]
					for n in newDr:
						detailRequests.append(n)
				else:
					if cat in MICATEGORIES:
						valid = valid_detail_specifier(cat, req)
						if valid == True:
							pass
						else:
							raise ArgumentException('Error: invalid request specifier --> mIWrap() line: ' + str(lineno()))
					else:
						raise ArgumentException('Error: invalid category --> mIWrap() line: ' + str(lineno()))
	if all == True:
		if allCat == True and allDetReq == True:
			general_array = compileDict(MICATEGORIES[0], GENERAL, file)
			video_array = compileDict(MICATEGORIES[1], VIDEO, file)
			audio_array = compileDict(MICATEGORIES[2], AUDIO, file)
			text_array = compileDict(MICATEGORIES[3], TEXT, file)
#			other_array = compileDict(MICATEGORIES[4], OTHER, file)
			image_array = compileDict(MICATEGORIES[5], IMAGE, file)
			menu_array = compileDict(MICATEGORIES[6], MENU, file)
		elif allCat == True and allDetReq == False:
			for c in category:
				if c == 'General':
					general_array = compileDict(MICATEGORIES[0], GENERAL, file)
				elif c == 'Video':
					video_array = compileDict(MICATEGORIES[1], VIDEO, file)
				elif c == 'Audio':
					audio_array = compileDict(MICATEGORIES[2], AUDIO, file)
				elif c == 'Text':
					text_array = compileDict(MICATEGORIES[3], TEXT, file)
				elif c == 'Other':
					continue
#					other_array = compileDict(MICATEGORIES[4], OTHER, file)
				elif c == 'Image':
					image_array = compileDict(MICATEGORIES[5], IMAGE, file)
				elif c == 'Menu':
					menu_array = compileDict(MICATEGORIES[6], MENU, file)
				else:
					raise ArgumentException('Error: invalid category --> mIWrap() line: ' + str(lineno()))
		else:#if allCat == False and allDetReq == True:
			requests = []
			for dr in detailRequests:
				drSplit = dr.split(';')
				cat = drSplit[0]
				req = drSplit[1]
				requests.append(req)
			for c in MICATEGORIES:
				if c == 'General':
					general_array = compileDict(c, requests, file)
				elif c == 'Video':
					video_array = compileDict(c, requests, file)
				elif c == 'Audio':
					audio_array = compileDict(c, requests, file)
				elif c == 'Text':
					text_array = compileDict(c, requests, file)
				elif c == 'Other':
					continue
#					other_array = compileDict(c, requests, file)
				elif c == 'Image':
					image_array = compileDict(c, requests, file)
				elif c == 'Menu':
					menu_array = compileDict(c, requests, file)
	else:
		for dr in detailRequests:
			drSplit = dr.split(';')
			cat = drSplit[0]
			req = drSplit[1]
			if cat == 'General':
				general_array[req] = runMediaInfo(cat, req, file)
			elif cat == 'Video':
				video_array[req] = runMediaInfo(cat, req, file)
			elif cat == 'Audio':
				audio_array[req] = runMediaInfo(cat, req, file)
			elif cat == 'Text':
				text_array[req] = runMediaInfo(cat, req, file)
			elif cat == 'Other':
				continue
#				other_array[req] = runMediaInfo(cat, req, file)
			elif cat == 'Image':
				image_array[req] = runMediaInfo(cat, req, file)
			elif cat == 'Menu':
				menu_array[req] = runMediaInfo(cat, req, file)
	return general_array, video_array, audio_array, text_array, image_array, menu_array

def remAllCategory( quiet, input ):
	newDetailRequests = []
	req = input
	for x in MICATEGORIES:
		valid = valid_detail_specifier(x, req)
		if valid == True:
			concat = x + ';' + req
			newDetailRequests.append(concat)
		else:
			if quiet == True:
				pass
			else:
				print 'This request: ' + req + ' is not available for this category: ' + x
	return newDetailRequests

def remNoneCategory( input ):
	request = []
	tempCat = []
	count = 0
	while count < len(MICATEGORIES):
		if MICATEGORIES[count] == 'Other':
			count += 1
			continue
		else:
			valid = valid_detail_specifier(MICATEGORIES[count], req)
			if valid == False:
				doContinue = False
				count += 1
			else:
				tempCat.append(MICATEGORIES[count])
				count += 1
	for req in input:
		msg = 'This request: ' + req + ' is available from the following categories, which one(s) would you like to get this request from?\n'
		selection = miOps.multiOptionsRange(msg, tempCat)
		for s in selection:
			concat = tempCat[s] + ';' + req
			detailRequests.append(concat)
	return request

def getCategory():
	category = []
	catMArry = ['Get all categories', 'Get specific categories']
	cmsg = 'Would you like to get information from all categories or specific ones?'
	opt = miOps.multiOptions(cmsg, catMArry)
	if opt == 0:
		for x in MICATEGORIES:
			category.append(x)
	else:
		nmsg = 'Which categories would you like information from?'
		selection = miOps.multiOptionsRange(nmsg, MICATEGORIES)
		for s in selection:
			category.append(MICATEGORIES[s])
	return category

def detAll():
	print 'Please answer the following questions:'
	question_one = 'Do you want all information from all of the categories available?'
	question_two = 'Do you want all of the information from specific categories that you have or will select?'
	question_three = 'Do you want the information you have or will select from all of the categories available?'
	first_pass = miOps.yOrN(question_one)
	if first_pass == True:
		return True, False
	else:
		second_pass = miOps.yOrN(question_two)
		if second_pass == True:
			return True, False
		else:
			third_pass = miOps.yOrN(question_three)
			if third_pass == True:
				return False, True
			else:
				return False, False

def getDetailRequests( all=None, category=None ):
	detailRequests = []
	msg = 'What information are you hoping to get from the file you provided?'
	#HINT: This isn't in use yet!! ---^
	#Use that message with a prompt to get keywords when you build that into this script
	doContinue = False
	while doContinue == False:
		rmsg = 'Please enter the detail request you would like now or enter \'-list\' to see a comprehensive list or \'-done\' to indicate you have entered all the requests you would like\n'
		warn = 'Note - the comprehensive list is quite large and long:\n'
		req = miOps.getInput(rmsg + warn)
		if req == '-list' or req == '-List' or req == '-LIST' or req == '-l' or req == '-L':
			printDetailRequestList()
		elif req == 'list' or req == 'List' or req == 'LIST' or req == 'l' or req == 'L':
			printDetailRequestList()
		elif req == '-done' or req == '-Done' or req == '-DONE' or req == '-d' or req == '-D':
			doContinue = True
		elif req == 'done' or req == 'Done' or req == 'DONE' or req == 'd' or req == 'D':
			doContinue = True
		else:
			if all == True:
				for c in MICATEGORIES:
					valid = valid_detail_specifier(c, req)
					if valid == False:
						print 'This request: ' + req + ' is not available for this category: ' + c
					else:
						concat = c + ';' + req
						detailRequests.append(concat)
			else:
				if not category:
					tempCat = []
					count = 0
					while count < len(MICATEGORIES):
						if MICATEGORIES[count] == 'Other':
							count += 1
							continue
						else:
							valid = valid_detail_specifier(MICATEGORIES[count], req)
							if valid == False:
								print 'This request: ' + req + ' is not available for this category: ' + MICATEGORIES[count]
								doContinue = False
								count += 1
							else:
								tempCat.append(MICATEGORIES[count])
								count += 1
					msg = 'This request: ' + req + ' is available from the following categories, which one(s) would you like to get this request from?\n'
					selection = miOps.multiOptionsRange(msg, tempCat)
					for s in selection:
						concat = tempCat[s] + ';' + req
						detailRequests.append(concat)
				else:
					valid = valid_detail_specifier(category, req)
					if valid == False:
						print 'This request: ' + req + ' is not available for this category: ' + category
					else:
						concat = category + ';' + req
						detailRequests.append(concat)
	return detailRequests

def printDetailRequestList():
	colList = miOps.columnedList(3)
	count = 0
	while count < len(NODUPLICATES):
		row = ()
		rowCount = 0
		while rowCount <= 2:
			if rowCount == 2:
				rowCount = 0
				count += 1
				temp = (NODUPLICATES[count],)
				row = row + temp
				colList.addRow(row)
				row = ()
			elif count == len(NODUPLICATES) - 1:
				temp = (NODUPLICATES[count],)
				row = row + temp
				colList.addRow(row)
				row = ()
				count += 1
				break
			else:
				temp = (NODUPLICATES[count],)
				row = row + temp
				count += 1
				rowCount += 1
	print colList
	return

def compileDict( category, request, file ):
	retDict = {}
	for r in request:
		valid = valid_detail_specifier(category, r)
		if valid == True:
			value = runMediaInfo(category, r, file)
			retDict[r] = str(value)
		else:
			print 'Sorry, that is not a valid detail specifier, skipping this one and moving on to the next.'
			continue
	return retDict

def runMediaInfo( category, value, file ):
	output = None
	cmd = 'mediainfo '
	cmd += '--Output=\"' + category + ';%' + value + '%\" ' + file
	out = commands.getstatusoutput(cmd)
	output = out[1]
	return output

def valid_detail_specifier( category, input ):
	valid = False
	if category == MICATEGORIES[0]:
		count = 0
		length = len(GENERAL) - 1
		for x in GENERAL:
			if input in x:
				valid = True
				break
			elif count == length:
				valid = False
				break
			else:
				count += 1
				continue
	elif category == MICATEGORIES[1]:
		count = 0
		length = len(VIDEO) - 1
		for x in VIDEO:
			if input in x:
				valid = True
				break
			elif count == length:
				valid = False
				break
			else:
				count += 1
				continue
	elif category == MICATEGORIES[2]:
		count = 0
		length = len(AUDIO) - 1
		for x in AUDIO:
			if input in x:
				valid = True
				break
			elif count == length:
				valid = False
				break
			else:
				count += 1
				continue
	elif category == MICATEGORIES[3]:
		count = 0
		length = len(TEXT) - 1
		for x in TEXT:
			if input in x:
				valid = True
				break
			elif count == length:
				valid = False
				break
			else:
				count += 1
				continue
	elif category == MICATEGORIES[4]:
		count = 0
		length = len(OTHER) - 1
		for x in OTHER:
			if input in x:
				valid = True
				break
			elif count == length:
				valid = False
				break
			else:
				count += 1
				continue
	elif category == MICATEGORIES[5]:
		count = 0
		length = len(IMAGE) - 1
		for x in IMAGE:
			if input in x:
				valid = True
				break
			elif count == length:
				valid = False
				break
			else:
				count += 1
				continue
	elif category == MICATEGORIES[6]:
		count = 0
		length = len(MENU) - 1
		for x in MENU:
			if input in x:
				valid = True
				break
			elif count == length:
				valid = False
				break
			else:
				count += 1
				continue
	else:
		raise ArgumentException('Error: category not allowed --> valid_detail_specifier() line: ' + str(lineno()))
	return valid

if __name__=='__main__':
	main()