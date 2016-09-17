# alloc-outbound
# HP controller, by K. Stevens
# Meat state encoding
.inputs req ackctl ackbus nakbus
.outputs ack busctl reqbus y1_allocoutbound y0_allocoutbound
.graph
# 0
req+ busctl+/1
# -> 1
busctl+/1 p1
p1 ackctl+

# 1 
ackctl+ reqbus+
# -> 2
reqbus+ p2
p2 ackbus+ nakbus+

# 2
ackbus+ y1_allocoutbound+
y1_allocoutbound+ reqbus-/1

nakbus+ y0_allocoutbound+
y0_allocoutbound+ reqbus-/2
# -> 3
reqbus-/1 ackbus-
# -> 5
reqbus-/2 nakbus-

# 3
ackbus- busctl-/1
# -> 4
busctl-/1 ackctl-/1

# 4
ackctl-/1 ack+
# -> 7
ack+ req-

# 7
req- y1_allocoutbound-
y1_allocoutbound- ack-
# -> 0
ack- req+

# 5
nakbus- busctl-/2
# -> 6
busctl-/2 ackctl-/2

# 6
ackctl-/2 y0_allocoutbound-
y0_allocoutbound- busctl+/2
# -> 1
busctl+/2 p1

.marking { <ack-,req+> }
.end
