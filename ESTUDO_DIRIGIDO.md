# Estudo Dirigido - Gradientes Conjugados

## Objetivo

Implementar o metodo iterativo dos Gradientes Conjugados conforme o algoritmo
do slide 23 do arquivo `MIT2_29S15_Lecture8 - Iterative.pdf` e rodar os casos
do exemplo fornecido.

## Algoritmo implementado

Para resolver o sistema linear `Ax = b`, com `A` simetrica definida positiva,
o metodo usa:

```text
v0 = r0 = b - A x0

alpha_i = (v_i^T r_i) / (v_i^T A v_i)
x_{i+1} = x_i + alpha_i v_i
r_{i+1} = r_i - alpha_i A v_i
beta_i = -(v_i^T A r_{i+1}) / (v_i^T A v_i)
v_{i+1} = r_{i+1} + beta_i v_i
```

A implementacao esta em `gradientes_conjugados.py`.

## Casos do exemplo

Foi gerada uma matriz `A` de ordem `500 x 500` da seguinte forma:

- diagonal inicialmente igual a `1`;
- entradas fora da diagonal sorteadas uniformemente em `[-1, 1]`;
- simetria mantida por `A = A^T`;
- entradas fora da diagonal com `|a_ij| > tau` zeradas;
- vetor `b` aleatorio;
- chute inicial `x0 = 0`;
- maximo de `20` iteracoes.

Foram testados `tau = 0.01, 0.05, 0.1, 0.2`.

## Resultados

### tau = 0.01

- Iteracoes executadas: `5`
- Nao zeros em `A`: `2950`
- Menor autovalor: `0.970828`
- Numero de condicao: `1.06121`
- Norma final do residuo: `9.880736e-09`

```text
n=00: 1.306794e+01
n=01: 1.732439e-01
n=02: 2.806844e-03
n=03: 4.180213e-05
n=04: 6.536367e-07
n=05: 9.880736e-09
```

### tau = 0.05

- Iteracoes executadas: `11`
- Nao zeros em `A`: `12876`
- Menor autovalor: `0.709467`
- Numero de condicao: `1.82018`
- Norma final do residuo: `1.001639e-08`

```text
n=00: 1.319380e+01
n=01: 1.907714e+00
n=02: 2.868020e-01
n=03: 3.889846e-02
n=04: 5.759658e-03
n=05: 8.938165e-04
n=06: 1.369885e-04
n=07: 1.981979e-05
n=08: 2.896206e-06
n=09: 4.258781e-07
n=10: 6.355864e-08
n=11: 1.001639e-08
```

### tau = 0.1

- Iteracoes executadas: `20`
- Nao zeros em `A`: `25266`
- Menor autovalor: `0.194962`
- Numero de condicao: `9.28538`
- Norma final do residuo: `1.026161e-05`

```text
n=00: 1.289377e+01
n=01: 5.035053e+00
n=02: 2.387999e+00
n=03: 1.230754e+00
n=04: 6.131873e-01
n=05: 3.024890e-01
n=06: 1.572073e-01
n=07: 7.975460e-02
n=08: 4.376530e-02
n=09: 2.314012e-02
n=10: 1.268692e-02
n=11: 6.593406e-03
n=12: 3.100859e-03
n=13: 1.497706e-03
n=14: 7.806607e-04
n=15: 3.871031e-04
n=16: 1.996427e-04
n=17: 9.198420e-05
n=18: 4.337151e-05
n=19: 2.007807e-05
n=20: 1.026161e-05
```

### tau = 0.2

- Iteracoes executadas: `20`
- Nao zeros em `A`: `51320`
- Menor autovalor: `-1.30607`
- Numero de condicao: indefinido, pois a matriz nao e definida positiva
- Norma final do residuo: `1.008427e+01`

```text
n=00: 1.304608e+01
n=01: 1.591742e+01
n=02: 4.668125e+01
n=03: 1.226645e+01
n=04: 2.136212e+01
n=05: 2.007965e+01
n=06: 1.123531e+01
n=07: 3.982454e+01
n=08: 1.412165e+01
n=09: 1.214162e+01
n=10: 2.104907e+02
n=11: 1.162143e+01
n=12: 1.313681e+01
n=13: 9.406954e+01
n=14: 1.183475e+01
n=15: 1.357886e+01
n=16: 5.087964e+01
n=17: 1.047491e+01
n=18: 1.604124e+01
n=19: 1.974649e+01
n=20: 1.008427e+01
```

## Conclusao

Quanto maior o valor de `tau`, mais entradas fora da diagonal permanecem na
matriz. Isso aumenta o numero de elementos nao nulos, piora o condicionamento
e torna a convergencia mais lenta. Para `tau = 0.2`, a matriz gerada deixou de
ser definida positiva, pois apresentou menor autovalor negativo. Como o metodo
dos Gradientes Conjugados pressupoe matriz simetrica definida positiva, nao ha
convergencia adequada nesse caso.
