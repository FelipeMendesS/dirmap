# RLM module
.name RLM_module
.inputs Sr La Cr
.outputs Sa Lr Ca
.graph
Ca- Sr+/1
Sr+/1 Lr+
Lr+ La+
La+ p1
p1 Sa+
Sa+ Sr-
Sr- Sa-
Sa- p2
p2 Sr+/2 Cr+
Sr+/2 p1
Cr+ Lr-
Lr- La-
La- Ca+
Ca+ Cr-
Cr- Ca-
.marking {p2}
.end
