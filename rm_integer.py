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

# Create the outfile name
outfile_name = sys.argv[1]
name_tokens = outfile_name.split('.')
name_tokens[0] = name_tokens[0]+"_final"
outfile_name = ".".join(name_tokens)

outfile = open(outfile_name, 'w')

# We need to make sure there is a decimal point in 
# commands for the feed rate and all axes
first_letters = ("F", "Z", "X", "Y", "I", "J")

# Look at all lines
for line in lines:
	adjusted_line = ""

	# Tokenize
	tokens = line.split()
	for token in tokens:
		# Make corrections
		if token.startswith(first_letters):
			if '.' not in token:
				token = token + ".0"

		# Rejoin
		adjusted_line = adjusted_line + token + " "

	#Format line
	adjusted_line = adjusted_line + "\n"
	
	# Write the line
	outfile.write(adjusted_line)

print("Output written to: " + outfile_name)
