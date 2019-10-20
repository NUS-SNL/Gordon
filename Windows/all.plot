FILES = system("ls -1 *.csv")
plot for [data in FILES] data u 3:2 w lines lc rgb 'black' notitle
