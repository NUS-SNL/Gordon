import sys
import os
import signal
import subprocess

f = open('sanitized-links.csv', 'r')

for i in range(1000):
	line = f.readline().split(',')
	if i > 124:
		exe = 'cp ../Windows/' + line[1] + '.csv ../' + line[0] + '-' + line[1] + '.csv'
		print exe
		try:
			os.system(exe)
			print "================================", line[0]
		except:
			pass
f.close()
