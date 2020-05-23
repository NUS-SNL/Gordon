# Gordon
Localised bottlenecks for server transport layer protocol analysis.  

## Dependancies:
```Scripts/quick_dependancies.sh```

## Runnning tests:
-----------------
### Single runs 
1. Launch a delay shell  
```$ mm-delay 50```  
2. The scripts for running the necessary tests are in *Scripts/*  
```mm-delay 50 $ cd Scripts/```  
3. Launching the test  
```mm-delay 50 $ ./launch.sh <target_URL>```  
4. Ending all processes *(not necessary)*
```mm-delay 50 $ ./clean.sh```

## Running tests with multiple trials per RTT (for cleaner results)
1. Launch a delay shell  
```$ mm-delay 50```  
2. The scripts for running the necessary tests are in *Scripts/*  
```mm-delay 50 $ cd Scripts/```  
3. Launching the test  
```mm-delay 50 $ ./multi-launch.sh <target_URL> <number of trials per RTT>```  
each trial's data will be stored in Gordon/Data/windows<trail_num>.csv  
cleaned data is stored in Gordon/Data/windows.csv  
4. Ending all processes *(not necessary)*
```mm-delay 50 $ ./clean.sh```

## Analyzing the data  
The final data at the end of either of the above tests are stored in ```windows.csv```. The individual trials for 'multiple-trails-per-RTT' test type are stored as ```windows1.csv```, ```windows2.csv```, ... ```windowsn.csv``` for 'n' trials.
Plot the results using ``` gnuplot plot.plt --persist ``` for multiple-trials tests.  

For single trial tests, you can simply open a ``` gnuplpot ``` shell and plot as ``` plot 'windows.csv' u 3:2 w lines ```

