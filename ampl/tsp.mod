### PARAMETERS ###
param n integer > 0;
param distance_matrix{1..n, 1..n} >=0 ;

### VARIABLES ###
var x{1..n,1..n} >= 0, <= 1;

### OBJECTIVE FUNCTION ###
minimize Length_Objective:
    sum{i in 1..n, j in 1..n} x[i,j]*c[i,j];

### CONSTRAINTS ###
subject to Integrality_Constraints {i in 1..n, j in 1..n}:
    x[i,j] = 0 or x[i,j] = 1
;

subject to Two_Degree_Constraints {i in 1..n}:
    sum{j in 1..n} x[i,j] = 2
;


### PROBLEM DEFINITION ###
problem Problem_A:
    x,                          
    Length_Objective,           
    Two_Degree_Constraints;

problem Problem_B:
    x,                          
    Length_Objective,
    Integrality_Constraints,           
    Two_Degree_Constraints;