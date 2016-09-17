# tms2taxi write data handshake.
# this is the stg simulated with oesim.
# results from async are in wrdatb.out
# state = 
.name wrdatab
.inputs IOSTRB Aack Dack Ack
.outputs XRDY Areq Dreq STRB X Y
.graph

IOSTRB+ XRDY+
IOSTRB- XRDY-
XRDY+ IOSTRB- Areq+
XRDY- IOSTRB+ Areq-

Areq+ Aack+ XRDY-
Areq- Aack- Dreq+ STRB-/0
Aack+ STRB+/0
Aack- Areq+

Dreq+ Dack+
Dreq- Dack- STRB-/1
Dack+ STRB+/1
Dack- Dreq+

STRB+/0 Ack+/0 Y-
STRB-/0 Ack-/0
Ack+/0 Areq-
Ack-/0 X-

STRB+/1 Ack+/1 Y+
STRB-/1 Ack-/1 XRDY+
Ack+/1 Dreq- 
Ack-/1 X+

X+ STRB+/0
X- STRB+/1

Y+ Dreq-
Y- Areq-

.end
