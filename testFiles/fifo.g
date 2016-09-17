.inputs a b
.outputs c
.graph
a+ b+/1
b+/1 c+
c+ b-/1
b-/1 a-
a- b+/2
b+/2 c-
c- b-/2
b-/2 a+
.end
