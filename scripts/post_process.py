#! /usr/bin/env python

#
# rm_integer.py
# Zac Staples
# zhstaple(at)nps(dot)edu
# directer NPS-DAZL group
# github: https://github.com/NPS-DAZL
#
# Usage:
#   G -code files produced by PC-Board Cam will not load onto the Roland
#   MDX-40A mill we use to cut PCB's because of formatting issues
#   in the files.
#
#   G_final.py processes the filenames provided as command line
#   arguments to so they will load into the Roland mill
#   
#   Specific issues are:
#     - Feed rates and X, Y and Z axis coordinates cannot be
#       integer values(i.e. F60 X20 will cause and error).
#       Integer valued quantities must include a trailing
#       zero(i.e. F60.0 X20.0).  
#     - I've tried most combinations of settings in PC-Board 
#       Mill to get a non-integer output in the code, but it 
#       seems that some post processing is going to be necessary.
#     - Circular interpolation used for cutting holes larger than
#       biggest drill bit are being cut ON the program line.  With
#       a wide bit this results in holes that are too wide.
#     - Commands that include circular interpolation need to be
#       adjusted for tool diameter offset with G41 and/or G42 codes.
#       See the NC code reference in the references folder for more.

import sys

# conduct argument checking
if(len(sys.argv) != 2):
    print("Usage: rm_integer <filename>")
    print("\t<filename> must point to the G-code file output from PC-Board Mill.")
    sys.exit()

# ensure the argument connects to a file that be opened
try:
    fp = open(sys.argv[1], 'r')
except IOError:
    print("Error: unable to open file " + str(sys.argv[1]))
    sys.exit()


##############################################
#                 MAIN
##############################################

# Read the input file
lines = fp.readlines()

# Create the intermediate and outfile name
inter_name = sys.argv[1]
name_tokens = inter_name.split('.')
name_tokens[0] = name_tokens[0]+"_inter"
inter_name = ".".join(name_tokens)

outfile_name = sys.argv[1]
name_tokens = outfile_name.split('.')
name_tokens[0] = name_tokens[0]+"_final"
outfile_name = ".".join(name_tokens)

# We need to make sure there is a decimal point in 
# commands for the feed rate and all axes
first_letters = ("F", "Z", "X", "Y", "I", "J")

# We need to keep track of x and y axis maximums
xy = ("X", "Y")
num_char = (".", "+", "-")
x_max = "Null"
x_min = "Null"
y_max = "Null"
y_min = "Null"

# Correct for integers in the intermediate file
interfile = open(inter_name, 'w')

for line in lines:
	adjusted_line = ""

	# Tokenize
	tokens = line.split()
	for token in tokens:
		# Make corrections
		if token.startswith(first_letters):
			if '.' not in token:
				token = token + ".0"
		
		#Track maximum dims
		if token.startswith(xy):
			num = ""
			for char in token:
				# print(char)
				if char.isdigit() or (char in num_char):
					num = num + char
		
			try:
				num = float(num)
				if(token[0] == "X"):
					if(x_max == "Null"): 
						x_max = num
						x_min = num
					elif num > x_max:
						x_max = num
					elif num < x_min:
						x_min = num
				
				if(token[0] == "Y"):
					if(y_max == "Null"): 
						y_max = num
						y_min = num
					elif num > y_max:
						y_max = num
					elif num < y_min:
						y_min = num
			
			except ValueError:
				pass
				
		# Rejoin
		adjusted_line = adjusted_line + token + " "

	#Format line
	adjusted_line = adjusted_line + "\n"
	
	# Write the line
	interfile.write(adjusted_line)
	
fp.close()
interfile.close()

# We need to correct for tool offset diameter in any line
# that contains circular interpolation which has commands 
# along the I and J axes.
interpolation_axes = ("I", "J")

# Correct for tool diameter offset
interfile = open(inter_name, 'r')
outfile = open(outfile_name, 'w')

lines = interfile.readlines()
line_before = lines[0]
index = 1
for line in lines[1:]:
	# Initialize the loop control variable
	already_corrected = False
	
	# Tokenize
	tokens = line.split()
	for token in tokens:
		# Control the loop for efficiency
		if not already_corrected:
			# Make corrections
			if token.startswith(interpolation_axes):
				#print("----------")
				#print("found an interp axis");
				#print(token)
				
				# The line with circular interpolation is PRECEEDED by 
				# a line that moves the bit from the center of the hole
				# to the path of edge of the hole.  This is the line
				# where we need to add comments for tool diameter offset.
				# The original line looks something along the lines of
				#     G01 X46.64
				# and we need to modify it to look like this
				#     G17 G42 D01 G01 X46.64
				# so that offset will comments moving to the right which
				# complements the G02 clockwise circular interpolation
				# useed in the PC-Board Cam software.
				#FYI - G17 directs the machine to conduct circular interp
				#in the X-Y plane.
				lines[index-1] = "G17 G42 D01 " + lines[index-1]
				
				# The line with circular interpolation is PROCEEDED by
				# a line that moves the mill back to center after it 
				# completes the circular cut.  This line also needs to
				# be modified because we must cancel the use of tool
				# diameter offset.  The original line looks something like
				#     G01 X45.05
				# and we need to modify by adding the G40 command
				#     G40 G01 X45.05 
				# so that offset will cease.
				# NOTE: the +1 index SHOULDN'T go past the lines array index
				# because a file with an interpolation command as the last line
				# is an error to start with.
				line_after = lines[index+1]
				line_after = "G40 " + line_after
				lines[index+1] = line_after
				#print(lines)
				
				# Set the loop control for a little efficiency
				already_corrected = True
	
	# Write the output and set up for the next loop
	outfile.write(lines[index-1])
	# print("-------"+str(index))
	# print(lines[index-1])
	index = index + 1

# The loop always writes the line_before so we must write the final
# line from the input to the output manually
outfile.write(lines[-1]) 
	
print("Output written to: " + outfile_name)
print("X max/min are: " + str(x_max) + " / " + str(x_min))
print("Y max/min are: " + str(y_max) + " / " + str(y_min))
