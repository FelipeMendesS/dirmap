# ram-read-sbuf
# HP controller, by K. Stevens
# Meat state encoding
.inputs req precharged prnotin wenin wsldin 
.outputs ack wsen prnot wen wsld y0_ramreadsbuf
.graph
# 0
req+ prnot+
precharged+ prnot+
# -> 1
prnot+ prnotin+

# 1
prnotin+ wen+
# -> 2
wen+ precharged- wenin+

# 2
precharged- ack+
wenin+ ack+
# -> 3
ack+ req-

# 3
req- wen- wsen-
# -> 4
wen- wenin-
wsen- wenin-

# 4
wenin- y0_ramreadsbuf+
y0_ramreadsbuf+ wsld+ prnot-
# -> 5
wsld+ wsldin+ precharged+
prnot- prnotin- precharged+

# 5
wsldin+ y0_ramreadsbuf-
prnotin- y0_ramreadsbuf-
y0_ramreadsbuf- wsld- 
# -> 6
wsld- wsldin-

# 6
wsldin- ack- wsen+
# -> 0
ack- req+
wsen+ req+

.marking { <req+,prnot+> <precharged+,prnot+> }
.end
