
T = readtable('lWristPoints.csv');

T = T{:,1:3}; 

plot(T(:,1),T(:,2),'r.')