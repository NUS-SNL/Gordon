import os
import signal
import sys
import subprocess

windows=list()
counter=0

for i in range(int(sys.argv[2])):
    infile="../Data/windows"+str(i+1)+".csv"
    read = open(infile, 'r')
    length=int(subprocess.check_output(['wc','-l',infile]).split(' ')[0])
    if length >= int(sys.argv[1]):
        for j in range(0, length):
	        line = read.readline()
        windows.append(int(line.split(' ')[1]))
        counter=counter+1
    read.close()

print windows
windows.sort()
median=int(windows[counter-1])
print windows

outfile="../Data/windows.csv"
out = open(outfile, 'r')

length=int(subprocess.check_output(['wc','-l',outfile]).split(' ')[0])
for j in range(0, length):
    line = out.readline()
out.close()

out=open(outfile, 'a')

print median, line.split(' ')[0]
cap=median+int(line.split(' ')[0])
print cap

out.write(str(cap)+" "+str(median)+" "+str(sys.argv[1])+"\n")
out.close()

