# pe-send-ifc
# HP controller, by K. Stevens
# Meat state encoding
.inputs reqsend treq rdiq adbldout ackpkt 
.outputs tack peack adbld y0_pesendifc y1_pesendifc 
.graph
# 0
reqsend+ y0_pesendifc+/1
treq+/1 y0_pesendifc+/1
rdiq+/1 y0_pesendifc+/1
y0_pesendifc+/1 adbld+/1
# -> 1
adbld+/1 place_1
place_1 adbldout+/1

# 1
adbldout+/1 y1_pesendifc+/1
y1_pesendifc+/1 peack+/1
# -> 2
peack+/1 rdiq-/1

# 2
rdiq-/1 y0_pesendifc-/1
y0_pesendifc-/1 adbld-/1 tack+/1 peack-/1
# -> 3
peack-/1 place_3_0 
adbld-/1 adbldout-/1
tack+/1 treq-/1
place_3_0 ackpkt+/1 rdiq+/2
adbldout-/1 place_3_1 
treq-/1 place_3_2 

# 3
rdiq+/2 y0_pesendifc+/2
place_3_1 y0_pesendifc+/2
place_3_2 y0_pesendifc+/2
y0_pesendifc+/2 adbld+/2

ackpkt+/1 y0_pesendifc+/3
place_3_1 y0_pesendifc+/3
place_3_2 y0_pesendifc+/3
y0_pesendifc+/3 peack+/2
# -> 4
adbld+/2 adbldout+/2
# -> 8
peack+/2 ackpkt-/1

# 4
adbldout+/2 y1_pesendifc-/1
y1_pesendifc-/1 peack+/3
# -> 5
peack+/3 rdiq-/2

# 5
rdiq-/2 y0_pesendifc-/2
y0_pesendifc-/2 peack-/3 adbld-/2 tack-/2
# -> 6
adbld-/2 adbldout-/3
tack-/2 treq+/2
peack-/3 place_5_2
adbldout-/3 place_5_0 
treq+/2 place_5_1 
place_5_2 ackpkt+/2 rdiq+/3

# 6
place_5_0 y0_pesendifc+/4
place_5_1 y0_pesendifc+/4
ackpkt+/2 y0_pesendifc+/4
y0_pesendifc+/4 peack+/4 tack+/3

place_5_0 y0_pesendifc+/5
place_5_1 y0_pesendifc+/5
rdiq+/3 y0_pesendifc+/5
y0_pesendifc+/5 adbld+/3
# -> 1
adbld+/3 place_1
# -> 7
peack+/4 ackpkt-/3
tack+/3 treq-/3

# 7
ackpkt-/3 y1_pesendifc+/2 
treq-/3 y1_pesendifc+/2
y1_pesendifc+/2 peack-/4 tack-/3
# -> 9
peack-/4 place_9_0
tack-/3 place_9_1
place_9_0 treq+/4 reqsend-
place_9_1 treq+/4 reqsend-

# 8
ackpkt-/1 tack-/4 peack-/5
# -> 9
peack-/5 place_9_0
tack-/4 place_9_1

# 9
treq+/4 tack+/5

# -> 0
# s4 conditions inputs... otherwise no USC !
reqsend- y0_pesendifc-/3 y1_pesendifc-/2
y0_pesendifc-/3 reqsend+ treq+/1 rdiq+/1
y1_pesendifc-/2 reqsend+ treq+/1 rdiq+/1
# -> 10
tack+/5 treq-/5

# 10
treq-/5 tack-/5
# -> 9
tack-/5 place_9_0 place_9_1

.marking { <reqsend-,y0_pesendifc-/3> <reqsend-,y1_pesendifc-/2> }
.end
