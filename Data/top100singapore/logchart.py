f = open('top-100.csv', 'r')

bbr = 0
cubic = 0
reno = 0
htcp = 0
unknown = 0
interest = 0
westwood = 0
illinois = 0
compound = 0

print "# bbr, cubic, reno, htcp, unknown, interest, westwood, illinois, compound"

for i in range(124): 
	line=f.readline()
	d = line.split(',')
	#print d
	a = d[2][:-1]
	if  a == 'cubic':
		cubic += 1
	elif a == 'bbr':
		bbr += 1
	elif a == 'reno':
		reno += 1
	elif a == 'htcp':
		htcp += 1
	elif a == 'unknown':	
		unknown += 1
	elif a == 'interest':
		interest += 1
	elif a == 'westwood':
		westwood += 1
	elif a == 'illinois':
		illinois += 1
	else:
		compound += 1
	print i+1, cubic, bbr, unknown, htcp, interest, westwood, reno, illinois, compound
