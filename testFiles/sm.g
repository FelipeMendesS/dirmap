# sm-latch (refer to p. 135 of my notebook)
.inputs s m
.outputs q
.graph
p1 s+/1 m+/1
s+/1 q+/1
q+/1 p2
p2 s-/1 m+/2
s-/1 p4
m+/2 p3
p3 s-/2
m- p4
p4 q-
m+/1 s+/2
s+/2 q+/2
q+/2 p3
s-/2 m-
q- p1
.end
