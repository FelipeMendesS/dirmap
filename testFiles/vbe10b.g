# Fig 10b, from VBE Tau '90 paper
.name vbe10b
.inputs R1 R2 R3 R4
.outputs A1 A2 A3 A4 X0 X1 X2
.graph
A1+ R1- X0+
R1- A1-
A1- R1+ A2+
R1+ A1+
X0+ A1-

A2+ R2- X1+ X0-
X0- A2-
R2- A2-
A2- R2+ A3+
R2+ A2+
X1+ A2-

A3+ R3- X2+ X1-
X1- A3-
R3- A3-
A3- R3+ A4+
R3+ A3+
X2+ A3-

A4+ R4- X2-
R4- A4-
A4- R4+ A1+
R4+ A4+
X2- A4-
.end
