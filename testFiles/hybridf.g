# hybrid stg between full handshake and straight handshake.
# one src, two dest, one intermediate handshake pairs.
.name hybridf

.inputs Ri A1i A2i 
.outputs Rx Ax Ao R1o R2o

.graph

Ri+ Ao+
Ri- Ao-
Ao+ Ri- Rx+
Ao- Ri+ Rx-

Rx+ Ao- Ax+ R1o+ R2o+
Rx- Ao+ Ax- R1o- R2o- 
Ax+ Rx-
Ax- Rx+

R1o+ A1i+
R1o- A1i-
A1i+ Ax+
A1i- Ax- R1o+

R2o+ A2i+
R2o- A2i-
A2i+ Ax+
A2i- Ax- R2o+

.end
