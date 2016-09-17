# version got by e-mail on Oct 28 1991
.name master_read
.inputs ari pri bprn xack di pack
.outputs aro pro breq busy mrdc do pdo x
.graph
ari+ pro-
ari- pro+
pri+ breq+
pri- aro+ breq-
bprn+ breq-
bprn- x+
xack+ mrdc-
xack- x-
di+ pdo- mrdc+
di- pdo+ mrdc-
pack+ pdo-
pack- pdo+
aro+ ari+
aro- ari-
pro+ pri-
pro- aro- pri+
breq+ pro+ busy+ bprn+
breq- pro- bprn-
busy+ breq-
busy- mrdc- breq+
mrdc+ do- busy+ xack+
mrdc- xack-
do+ di+
do- di-
pdo+ x- pack+
pdo- do- pack-
x+ busy-
x- do+
.marking { <aro+,ari+> <breq-,pro-> <busy-,breq+> <pdo+,pack+> <x-,do+> }
.end
