# sendr-done
# HP controller, by K. Stevens
# Meat state encoding
.inputs w8 reqsend
.outputs dones y0_sendrdone
.graph
# 0
w8+ y0_sendrdone+
reqsend+ y0_sendrdone+
# -> 1
y0_sendrdone+ w8-

# 1
w8- dones+
# -> 2
dones+ reqsend-

# 2
reqsend- y0_sendrdone-
y0_sendrdone- dones-
# -> 0
dones- w8+ reqsend+

.marking { <dones-,w8+> <dones-,reqsend+> }
.end
