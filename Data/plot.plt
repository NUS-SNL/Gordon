reset
set term postscript eps enhanced color 25
#set terminal eps enhanced color
set output "some.eps"

set size 1, 0.75

###### Pretty formatting ######
# put the border more to the background by applying it only on the left and bottom part 
set border 3 back
set tics nomirror

# add a slight grid to make it easier to follow the exact position of the curves
set style line 12 lc rgb '#808080' lt 0 lw 1
set grid back ls 12

set ylabel 'Number of packets'
set xlabel 'RTTs'

plot 'windows2.csv' u 3:2 w points pt 7 ps 0.75 lc rgb "red" notitle,\
'windows2.csv' u 3:2 w points pt 7 ps 0.75 lc rgb "red" notitle,\
'windows3.csv' u 3:2 w points pt 7 ps 0.75 lc rgb "red" notitle,\
'windows4.csv' u 3:2 w points pt 7 ps 0.75 lc rgb "red" notitle,\
'windows5.csv' u 3:2 w points pt 7 ps 0.75 lc rgb "red" notitle,\
'windows6.csv' u 3:2 w points pt 7 ps 0.75 lc rgb "red" notitle,\
'windows7.csv' u 3:2 w points pt 7 ps 0.75 lc rgb "red" notitle,\
'windows8.csv' u 3:2 w points pt 7 ps 0.75 lc rgb "red" notitle,\
'windows9.csv' u 3:2 w points pt 7 ps 0.75 lc rgb "red" notitle,\
'windows10.csv' u 3:2 w points pt 7 lc rgb "red" notitle,\
'windows.csv' u 3:2 w lines lw 3 lc rgb"blue" title "Maximum measurement"


