import urllib2
import time

available_chars = " abcdefghijklmnopqrstuvwxyz0123456789"
save_file = "names2.txt"

def is_name_avail(name):
	# make names with spaces URL compliant by replacing spaces with their hex value %20
	name = name.replace(' ', '%20')
	# this is a URL that was gotten by reverse engineering a name checking service, it takes in a name to check 
	# and the current time in a format often refered to as 'unix time'. 'unix time' is just a count of how many
	# seconds have passed since Jan 1st 1970 and is used by basicly every computer. anytime there is a string with 
	# the symbol {} in it, the symbol {} is just a placeholder for a variable value, and the function .format() is
	# used to replace the {} with a variable value of our choice. In this case we have {} in two places of our string, 
	# and are going to replace the first one with the name we want to check and the second with the current unix time
	url = "http://lolnamecheck.jj.ai/main/check?username={}&region_name=na&_={}".format(name, int(time.time()) * 1000)

	# sometimes errors occur when trying to access URL's, try: except: blocks just help defend us against errors
	try:
		# using the URL we created above, call the server and see if it responds with a value of "avail-yes", which
		# woudl indicate that the name is available to use
		if urllib2.urlopen(url).read()[24:33] == "avail-yes":
			return True
		else:
			return False
	except urllib2.HTTPError as err:
		# we got one of the URL errors, assume the name is not available. Ideally you would want to pause and retry but
		# this is just easier for now
		return False

def get_next_name(name):
	# take the variable 'name' and convert it into a list of symbols. The reason for doing this is because it allows us
	# to iterate through each symbol individually, and change them if we so desire!
	NL = list(name)
	# get a variable that is equal to 1 less than the number of symbols in our 'name' variable. This will be used to keep 
	# track of where we are currently looking in our name
	i = len(NL) - 1
	# loop through, incrementing as necessary to get the next name we will try. If you visualize our name as a number this 
	# is just like counting, trying every possible name using every combination of available_chars that it can
	while i != -1:
		# find how far we are through our list of available_chars
		ind = available_chars.index(NL[i])

		# check if there is another character in our available_chars list we can try, else switch to the first character
		# in available_chars and 'increment' the next symbol in our name. Same idea behind counting from 09 to 10. 
		# if you are using all letters, numbers, and space you can really think of our name mathematically as a base 37 number
		if ind == len(available_chars) - 1:
			# we have tried all our symbols in available_chars, so reset and increment next symbol in our name
			NL[i] = available_chars[0]
			i -= 1
		else:
			# we have another symbol in available_chars we can try, increment the current symbol to the next one in the list of available_chars
			NL[i] = list(available_chars)[ind + 1]
			i = -1
	# join all the symbols in the list back into a string 
	return ''.join(NL)

# the first name we will check. First character can't be a space, and must only include symbols thar are in available_chars
name = 'a   '

# just a little message to let you know it is working :) 
print "Finding all available LOL names"

# while True just literally means loop forever and ever
while True:
	# check if the name is currently available by calling the function is_name_avail() that we made above
	if is_name_avail(name):
		# the symbol {} is a place holder for a variable value, the .format() picks what variable
		print('{}'.format(name))
		# append the name onto our save file, "a" means append, different letters here can do different things
		with open(save_file, "a") as f:
			f.write("{}\r\n".format(name))
	# get the next name we want to test by calling the function get_next_name() that we made above
	name = get_next_name(name)
