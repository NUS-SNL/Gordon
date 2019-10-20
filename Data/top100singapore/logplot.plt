#set terminal svg size 1300, 600
#set rmargin 5

#dimensions are in screen units
width_left = 0.48
width_right = 0.10 #0.25
eps_v = 0.12
eps_h_left = 0.1
eps_h_right = 0.3 # 0.05

set multiplot layout 2, 2 title 'TCP variants used by Alexa ranked websites (Singapore)'

#set nonlinear x via log10(x) inverse 10**x 
#'' u 1:(($7+$8+$9+$10)/$1)*100.0 w filledcurves above y1=0  title 'Interesting variants' lc rgb"#FF00FF",\

set xlabel 'Sample size'
set ylabel 'Percentage share (%)'
set xrange [1:100]

unset key

set lmargin at screen 0.1
set rmargin at screen eps_h_left + width_left

plot 'logchart.csv' u 1:(($2+$3+$4+$5+$6+$7+$8+$9+$10)/$1)*100.0 w filledcurves above y1=0 title 'Unknown' lc rgb"#FF0000",\
'' u 1:(($2+$3+$5+$7+$8+$9+$10)/$1)*100.0 w filledcurves above y1=0  title 'Cubic' lc rgb"#A82200",\
'' u 1:(($3+$5+$7+$8+$9+$10)/$1)*100.0 w filledcurves above y1=0  title 'BBR' lc rgb"#82004B",\
'' u 1:(($5+$7+$8+$9+$10)/$1)*100.0 w filledcurves above y1=0  title 'HTCP' lc rgb"#D30094",\
'' u 1:(($7+$8+$9+$10)/$1)*100.0 w filledcurves above y1=0  title 'Westwood' lc rgb"#9400D3",\
'' u 1:(($8+$9+$10)/$1)*100.0 w filledcurves above y1=0  title 'Reno' lc rgb"#4B0082",\
'' u 1:(($9+$10)/$1)*100.0 w filledcurves above y1=0  title 'Illinois' lc rgb"#0022A8",\
'' u 1:(($10)/$1)*100.0 w filledcurves above y1=0  title 'Compound' lc rgb"#0000FF" 

#unset nonlinear x
unset xlabel
unset ylabel
unset ytics
unset xrange

set xtics (100)
set xlabel 'Aggregated CC share'

set key outside
set key top right

set boxwidth 2


set lmargin at screen 1. - (width_right + eps_h_right)
set rmargin at screen 1. - eps_h_right

plot 'final100perc.csv' u 1:(($2+$3+$4+$5+$6+$7+$8+$9+$10)/$1)*100.0 w boxes fs solid title 'Unknown (26.0%)' lc rgb"#FF0000",\
'' u 1:(($2+$3+$5+$7+$8+$9+$10)/$1)*100.0 w boxes fs solid  title 'Cubic (36.0%)' lc rgb"#A82200",\
'' u 1:(($3+$5+$7+$8+$9+$10)/$1)*100.0 w boxes fs solid title 'BBR (22.0%)' lc rgb"#82004B",\
'' u 1:(($5+$7+$8+$9+$10)/$1)*100.0 w boxes fs solid title 'HTCP (6.0%)' lc rgb"#D30094",\
'' u 1:(($7+$8+$9+$10)/$1)*100.0 w boxes fs solid title 'Westwood (2.0%)' lc rgb"#9400D3",\
'' u 1:(($8+$9+$10)/$1)*100.0 w boxes fs solid title 'Reno (2.0%)' lc rgb"#4B0082",\
'' u 1:(($9+$10)/$1)*100.0 w boxes fs solid title 'Illinois (1.0%)' lc rgb"#0022A8",\
'' u 1:(($10)/$1)*100.0 w boxes fs solid title 'Compound (1.0%)' lc rgb"#0000FF" 


set xrange [100:5000]
set xtics (100, 200, 500, 1000, 2500, 5000)
set xlabel 'Sample size'
set ylabel 'Percentage share (%)'

set nonlinear x via log10(x) inverse 10**x 

set ytics
set xtics

#unset nonlinear x
unset key

set lmargin at screen 0.1
set rmargin at screen eps_h_left + width_left

plot 'logchart.csv' u 1:(($2+$3+$4+$5+$6+$7+$8+$9+$10)/$1)*100.0 w filledcurves above y1=0 title 'Unknown' lc rgb"#FF0000",\
'' u 1:(($2+$3+$5+$7+$8+$9+$10)/$1)*100.0 w filledcurves above y1=0  title 'Cubic' lc rgb"#A82200",\
'' u 1:(($3+$5+$7+$8+$9+$10)/$1)*100.0 w filledcurves above y1=0  title 'BBR' lc rgb"#82004B",\
'' u 1:(($5+$7+$8+$9+$10)/$1)*100.0 w filledcurves above y1=0  title 'HTCP' lc rgb"#D30094",\
'' u 1:(($7+$8+$9+$10)/$1)*100.0 w filledcurves above y1=0  title 'Westwood' lc rgb"#9400D3",\
'' u 1:(($8+$9+$10)/$1)*100.0 w filledcurves above y1=0  title 'Reno' lc rgb"#4B0082",\
'' u 1:(($9+$10)/$1)*100.0 w filledcurves above y1=0  title 'Illinois' lc rgb"#0022A8",\
'' u 1:(($10)/$1)*100.0 w filledcurves above y1=0  title 'Compound' lc rgb"#0000FF" 



unset nonlinear x
unset xlabel
unset ylabel
unset ytics
unset xrange

set xtics (124)
set xlabel 'Aggregated CC share'

set key outside
set key top right

set boxwidth 2


set lmargin at screen 1. - (width_right + eps_h_right)
set rmargin at screen 1. - eps_h_right

plot 'final5000perc.csv' u 1:(($2+$3+$4+$5+$6+$7+$8+$9+$10)/$1)*100.0 w boxes fs solid title 'Unknown (24.9%)' lc rgb"#FF0000",\
'' u 1:(($2+$3+$5+$7+$8+$9+$10)/$1)*100.0 w boxes fs solid  title 'Cubic (34.7%)' lc rgb"#A82200",\
'' u 1:(($3+$5+$7+$8+$9+$10)/$1)*100.0 w boxes fs solid title 'BBR (30.6%)' lc rgb"#82004B",\
'' u 1:(($5+$7+$8+$9+$10)/$1)*100.0 w boxes fs solid title 'HTCP (4.8%)' lc rgb"#D30094",\
'' u 1:(($7+$8+$9+$10)/$1)*100.0 w boxes fs solid title 'Westwood (1.6%)' lc rgb"#9400D3",\
'' u 1:(($8+$9+$10)/$1)*100.0 w boxes fs solid title 'Reno (1.6%)' lc rgb"#4B0082",\
'' u 1:(($9+$10)/$1)*100.0 w boxes fs solid title 'Illinois (0.8%)' lc rgb"#0022A8",\
'' u 1:(($10)/$1)*100.0 w boxes fs solid title 'Compound (0.8%)' lc rgb"#0000FF" 

unset multiplot
