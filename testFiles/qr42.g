.name qr42
.inputs a d
.outputs b c x
.graph
a+/2 c+
c+ b+/1 d+

b+/1 a-/1
a-/1 x+

d+ x+

x+ b-/1
b-/1 a+/1
a+/1 c-

c- b+/2 d-
b+/2 a-/2

d- x-

a-/2 x-
x- b-/2
b-/2 a+/2
.end
