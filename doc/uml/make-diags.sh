#!/bin/sh

## ver como instalar scruffy en https://github.com/aivarsk/scruffy/
## ahí esta tambien la doc de como se hacen los diagramas
## NO PONER las imagenes en la raiz de AGIS

OUT_DIR="../../../agis_diag"
mkdir -p "$OUT_DIR"
suml --png --scruffy --shadow -i todos.txt -o "$OUT_DIR/todos.png"
