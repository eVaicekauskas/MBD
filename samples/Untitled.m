
T = readtable('chairTest/lWristPoints_10.csv');

T = T{:,1:3}; 

plot(T(:,1),T(:,2),color = [1 0 0])