"""Estudo dirigido: metodo dos Gradientes Conjugados.

Implementa o algoritmo do slide 23 da aula MIT 2.29 Lecture 8 e roda
os casos do exemplo para tau = 0.01, 0.05, 0.1 e 0.2.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass
class ResultadoCG:
    tau: float
    iteracoes: int
    nao_zeros: int
    condicao: float | None
    menor_autovalor: float
    x: np.ndarray
    residuos: list[float]


def gradientes_conjugados(
    A: np.ndarray,
    b: np.ndarray,
    x0: np.ndarray | None = None,
    max_iter: int = 20,
    tolerancia: float = 1e-14,
) -> tuple[np.ndarray, list[float]]:
    """Resolve Ax = b por Gradientes Conjugados.

    A implementacao segue o algoritmo do slide 23:
    v0 = r0 = b - A x0
    alpha_i = (v_i^T r_i) / (v_i^T A v_i)
    x_{i+1} = x_i + alpha_i v_i
    r_{i+1} = r_i - alpha_i A v_i
    beta_i = -(v_i^T A r_{i+1}) / (v_i^T A v_i)
    v_{i+1} = r_{i+1} + beta_i v_i
    """
    n = b.shape[0]
    x = np.zeros(n, dtype=float) if x0 is None else x0.astype(float).copy()
    r = b - A @ x
    v = r.copy()
    residuos = [float(np.linalg.norm(r))]

    for _ in range(max_iter):
        Av = A @ v
        denominador = float(v @ Av)
        if abs(denominador) < np.finfo(float).eps:
            break

        alpha = float(v @ r) / denominador
        x = x + alpha * v
        r_novo = r - alpha * Av
        residuos.append(float(np.linalg.norm(r_novo)))

        if residuos[-1] < tolerancia:
            break

        beta = -float(v @ (A @ r_novo)) / denominador
        v = r_novo + beta * v
        r = r_novo

    return x, residuos


def matriz_do_exemplo(n: int, tau: float, rng: np.random.Generator) -> np.ndarray:
    """Gera a matriz 500x500 descrita no exemplo.

    Primeiro cria entradas fora da diagonal uniformes em [-1, 1], mantendo
    simetria. Depois zera as entradas com |a_ij| > tau e mantem a diagonal em 1.
    Assim, a densidade esperada fora da diagonal fica aproximadamente tau.
    """
    superior = rng.uniform(-1.0, 1.0, size=(n, n))
    superior = np.triu(superior, k=1)
    A = superior + superior.T
    A[np.abs(A) > tau] = 0.0
    np.fill_diagonal(A, 1.0)
    return A


def rodar_caso(n: int, tau: float, seed: int, max_iter: int) -> ResultadoCG:
    rng = np.random.default_rng(seed)
    A = matriz_do_exemplo(n, tau, rng)
    b = rng.uniform(-1.0, 1.0, size=n)
    x, residuos = gradientes_conjugados(A, b, max_iter=max_iter)

    autovalores = np.linalg.eigvalsh(A)
    menor = float(autovalores[0])
    maior = float(autovalores[-1])
    condicao = maior / menor if menor > 0 else None

    return ResultadoCG(
        tau=tau,
        iteracoes=len(residuos) - 1,
        nao_zeros=int(np.count_nonzero(A)),
        condicao=condicao,
        menor_autovalor=menor,
        x=x,
        residuos=residuos,
    )


def formatar_resultado(resultado: ResultadoCG) -> str:
    condicao = (
        f"{resultado.condicao:.6g}"
        if resultado.condicao is not None
        else "indefinida (matriz nao SPD)"
    )
    linhas = [
        f"tau = {resultado.tau}",
        f"  iteracoes executadas: {resultado.iteracoes}",
        f"  nao zeros em A: {resultado.nao_zeros}",
        f"  menor autovalor: {resultado.menor_autovalor:.6g}",
        f"  numero de condicao: {condicao}",
        "  ||r_n|| por iteracao:",
    ]
    linhas.extend(
        f"    n={i:02d}: {residuo:.6e}"
        for i, residuo in enumerate(resultado.residuos)
    )
    return "\n".join(linhas)


def main() -> None:
    n = 500
    max_iter = 20
    seed_base = 22915
    taus = [0.01, 0.05, 0.1, 0.2]

    for i, tau in enumerate(taus):
        resultado = rodar_caso(n=n, tau=tau, seed=seed_base + i, max_iter=max_iter)
        print(formatar_resultado(resultado))
        if i != len(taus) - 1:
            print()


if __name__ == "__main__":
    main()
