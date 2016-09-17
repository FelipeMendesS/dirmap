# A to D converter controller 
# From Tam-Anh Chu's PhD Thesis
# Page 133  (CSC version) 
.inputs la da za
.outputs lr dr zr
.internal x
.graph
la+ dr+

dr+ da+ lr-
da+ zr+
zr+ za+
za+ x+
x+ zr-
zr- za- dr-
za- lr+

lr- zr+ la-
la- dr-
dr- da-
da- x-
x- lr+

lr+ la+
.end
