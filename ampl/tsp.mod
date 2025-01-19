### PARAMETERS ###
param n integer > 0;
param distance_matrix{1..n, 1..n} >=0 ;

### VARIABLES ###
var x{i in 1..n, j in i+1..n} >= 0, <= 1;  # Only upper triangular part

### OBJECTIVE FUNCTION ###
minimize Length_Objective:
    sum{i in 1..n, j in i+1..n} x[i,j]*distance_matrix[i,j];

### CONSTRAINTS ###
#subject to Integrality_Constraints {i in 1..n, j in i+1..n}:
#    x[i,j] = 0 or x[i,j] = 1;

subject to Degree_Constraints {i in 1..n}:
    sum{j in 1..i-1} x[j,i] + sum{j in i+1..n} x[i,j] = 2;

### PROBLEM DEFINITION ###
problem Problem_A:
    x,                          
    Length_Objective,           
    Degree_Constraints;

#problem Problem_B:
#    x,                          
#    Length_Objective,
#    Integrality_Constraints,           
#    Degree_Constraints;