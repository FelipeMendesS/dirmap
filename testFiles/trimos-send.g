# trimosbus specification
# sender component 1(Caltech Conf. on  VLSI, 1/79)
.inputs  r1 r2 r3
.outputs a b c t1 t2 t3
.graph
a- c+ t1+
c+ b- t1-
b- a+ t2+
a+ c- t2-
c- b+ t3+
b+ a- t3-

r1+ t1+ a-
t1+ r1- c+
r1- t1-
t1- r1+

r2+ t2+ b-
t2+ r2- a+
r2- t2-
t2- r2+

r3+ t3+ c-
t3+ r3- b+
r3- t3-
t3- r3+
.end