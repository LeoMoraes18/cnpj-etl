
[win]
Empresas1:   4.494.860 linhas →  13,42s  →  335 mil linhas/s
Empresas0:  29.069.564 linhas →  91,39s  →  318 mil linhas/s

Empresas1 — 4.494.860 — 13,4s (loop inline) → 16,6s (generator) — +23%, custo aceitável pelo desacoplamento.

[linux] Empresas0 — 29.069.564 linhas
  dict:                25,96s
  dataclass:           31,80s   (+22% — custo aceitável: tipagem verificada)
  dataclass slots:     32,90s   (+3% pior — slots otimiza acesso a atributo,
                                 e o loop não acessa atributo nenhum)