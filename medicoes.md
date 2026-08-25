
[win]
Empresas1:   4.494.860 linhas →  13,42s  →  335 mil linhas/s
Empresas0:  29.069.564 linhas →  91,39s  →  318 mil linhas/s

Empresas1 — 4.494.860 — 13,4s (loop inline) → 16,6s (generator) — +23%, custo aceitável pelo desacoplamento.

commit por linha:   ~3.500 linhas/s  →  projeção de ~2h20min
commit por lote:    72.700 linhas/s  →  6min40s real
commit por lote + executemany:  336,3s → 86,4 mil l/s   (-16%)

                   sem índice    com índice    ganho
comum  (20,3 mi)     22,023s       1,403s       15,7x
raro   (278 mil)      4,161s       0,016s      260,0x

[linux] Empresas0 — 29.069.564 linhas
  dict:                25,96s
  dataclass:           31,80s   (+22% — custo aceitável: tipagem verificada)
  dataclass slots:     32,90s   (+3% pior — slots otimiza acesso a atributo,
                                 e o loop não acessa atributo nenhum)