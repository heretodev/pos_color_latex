#!/usr/bin/env python3
import nltk
import sys

def is_number(s):
	try:
		float(s)
		return True
	except ValueError:
		pass

# NP : noun phrase
# VP : verb phrase
# JJ : adjective
# CC : coordinating conjunction (i.e. and)
# RB : adverb
# IN : preposition
# NN : Noun
# TO : the word to
# DT : a, the, this, no
# NNS : Plural noun (i.e. examples)
# VB : verb
# VBP, VBG : present tense verb
# VBD : past tense verb (WANT A HARSH COLOR FOR THIS)
# VBZ : ?
# WRB : ?
# PRP$ : our
# WDT : which

color_dict = {
	'NP' : 'MidnightBlue',
	'NN' : 'MidnightBlue',
	'NNS' : 'MidnightBlue',
	'PRP' : 'MidnightBlue',
	'PRP$' : 'MidnightBlue',
	'NNP' : 'MidnightBlue', 
	'EX' : 'MidnightBlue', # there
	'VP' : 'Periwinkle',
	'VB' : 'Periwinkle',
	'VBP' : 'Periwinkle',
	'VBD' : 'red', # past tense verb red to remove!
	'VBG' : 'Periwinkle',
	'VBN' : 'Periwinkle',
	'VBZ' : 'Periwinkle',
	'MD' : 'red', # can.  it's a weak phrase that requires better proof so highlighting red.
	'RBS' : 'red', # most.  it's a strong modifier so it's red to verify and cite.
	'JJS' : 'red', # lowest.  it's a strong modifier so it's red to verify.
	'JJ' : 'Mahogany',
	'JJR' : 'Mahogany', # more
	'RB' : 'Mahogany',
	'RBR' : 'Mahogany',
	'RP' : 'Mahogany', # out
	'CC' : 'ForestGreen',
	'TO' : 'ForestGreen',
	'DT' : 'ForestGreen',
	'IN' : 'ForestGreen',
	'WDT' : 'ForestGreen',
	'WRB' : 'ForestGreen', # when
	'.' : 'black',
	',' : 'black',
	':' : 'black',
	'CD' : 'black', # a number
	'(' : 'black',
	')' : 'black',
	'$' : 'black', # TODO: it's an equation marker in latex as $...$
	'SYM' : 'black', # TOOD: it's an equation marker like a single letter inside $...$
	'POS' : 'black' # 's
}

# Usage: ./pos_color.py < yourfile.tex > yourfile_out.tex # remember to pdflatex your .tex out next.
if __name__ == "__main__":
#	lines = []
#	with open("<your file>.tex") as f1:
#		lines = f1.readlines()
	lines = sys.stdin.readlines() # takes a pipe of a .tex file input??

	lines2 = []
	ignore = False
	for line in lines:
		if((line[0] == '\\') or (line[0] == '%') or ignore):
			lines2.append(line)
			if(line.find("\\documentclass") != -1):
				lines2.append('\\usepackage[dvipsnames]{xcolor}\n') # add text color package TODO: check if it's already included
			# ignore everything between \begin{keywords} and \end{keywords}:
			if(line.find("\\begin{keywords}") != -1):
				ignore = True
			if(line.find("\\end{keywords}") != -1):
				ignore = False
			if(line.find("\\begin{equation}") != -1):
				ignore = True
			if(line.find("\\end{equation}") != -1):
				ignore = False
			if(line.find("\\begin{table}") != -1):
				ignore = True
			if(line.find("\\end{table}") != -1):
				ignore = False
			if(line.find("\\begin{figure}") != -1):
				ignore = True
			if(line.find("\\end{figure}") != -1):
				ignore = False
			continue
		words = nltk.word_tokenize(line)
		pos_tags = nltk.pos_tag(words)
		line2 = ''
		word_ignore = False
		prev_word = ''
		for word, pos in pos_tags:
			if word[-1] == '\\':
				line2 = line
				break
			elif (word.find("_") != -1): # parser splits at _, so don't add space.
				line2 += word
			elif (word == "\\cite" or word == "\\ref" or word[0] == "$" or word_ignore):
				word_ignore = True
				line2 += word
				if(word == "}" or word.find("$") != -1): # found closing tag on cite
					word_ignore = False
			elif (word.find('\\') != -1):
				line2 += word # don't add space after \ 
			elif (color_dict[pos] == 'black') or (word.find('{') != -1) or (word.find('}') != -1) or (word == "$") or (word == ":") or (word == ",") or (word == "."):# or (word == '%'):
				line2 += word + ' '
			else:
				if word == '%':
					if is_number(prev_word):
						line2 += word +  " "
					else:
						word_ignore = True
				else:
					color_word = '\\textcolor{' + color_dict[pos] + '}{' + word + '} '
					line2 += color_word
			prev_word = word
		lines2.append(line2)

	#with open("<your new file>.tex", "w") as f:
	#	f.writelines(lines2)
	#	f.close()
	sys.stdout.writelines(lines2)
