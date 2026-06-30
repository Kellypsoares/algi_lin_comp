"""Estudo dirigido: método dos Gradientes Conjugados.

O caso principal reproduz o exemplo ``vib_string.m`` dos slides 13 e 14 da
aula MIT 2.29 Lecture 8. O experimento antigo com matrizes aleatórias e tau foi
mantido apenas como teste adicional, separado do fluxo principal.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import pi

import numpy as np


@dataclass
class ResultadoCG:
    caso: str
    o: float
    k: float
    h: float
    simetrica: bool
    definida_positiva: bool
    menor_autovalor: float
    iteracoes: int
    residuo_final: float
    x_grid: np.ndarray
    A: np.ndarray
    f: np.ndarray
    solucao_direta: np.ndarray
    solucao_cg: np.ndarray
    residuos: list[float]


@dataclass
class ResultadoTau:
    tau: float
    iteracoes: int
    nao_zeros: int
    condicao: float | None
    menor_autovalor: float
    x: np.ndarray
    residuos: list[float]


def conjugate_gradient(
    A: np.ndarray,
    b: np.ndarray,
    x0: np.ndarray | None = None,
    max_iter: int | None = None,
    tolerancia: float = 1e-10,
) -> tuple[np.ndarray, list[float]]:
    """Resolve Ax = b pelo algoritmo dos Gradientes Conjugados do slide 23."""
    n = b.shape[0]
    limite = n if max_iter is None else max_iter
    x = np.zeros(n, dtype=float) if x0 is None else x0.astype(float).copy()
    r = b - A @ x
    v = r.copy()
    residuos = [float(np.linalg.norm(r))]

    for _ in range(limite):
        Av = A @ v
        denominador = float(v @ Av)
        if abs(denominador) < np.finfo(float).eps:
            break

        alpha = float(v @ r) / denominador
        x = x + alpha * v
        r_novo = r - alpha * Av
        residuos.append(float(np.linalg.norm(r_novo)))

        if residuos[-1] <= tolerancia:
            break

        beta = -float(v @ (A @ r_novo)) / denominador
        v = r_novo + beta * v
        r = r_novo

    return x, residuos


def gradientes_conjugados(
    A: np.ndarray,
    b: np.ndarray,
    x0: np.ndarray | None = None,
    max_iter: int | None = None,
    tolerancia: float = 1e-10,
) -> tuple[np.ndarray, list[float]]:
    """Alias em portugues para manter compatibilidade com a versao anterior."""
    return conjugate_gradient(A, b, x0=x0, max_iter=max_iter, tolerancia=tolerancia)


def build_vib_string_case(
    o: float,
    k: float,
    n: int = 99,
    L: float = 1.0,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, float]:
    """Recria o sistema linear do exemplo MATLAB ``vib_string.m``.

    Retorna a malha x, a matriz tridiagonal A, o vetor de força f e o passo h.
    """
    h = L / (n + 1)
    x = np.arange(h, L, h)
    diagonal = (k * h) ** 2 - 2.0

    A = np.zeros((n, n), dtype=float)
    np.fill_diagonal(A, diagonal)
    np.fill_diagonal(A[1:], o)
    np.fill_diagonal(A[:, 1:], o)

    f = np.zeros(n, dtype=float)
    nf = round((n + 1) / 3)
    nw = round((n + 1) / 6)
    nw = min(min(nw, nf - 1), n - nf)
    nw1 = nf - nw
    nw2 = nf + nw
    tamanho_janela = nw2 - nw1 + 1
    f[nw1 - 1 : nw2] = h**2 * np.hanning(tamanho_janela)

    return x, A, f, h


def matriz_eh_simetrica(A: np.ndarray, atol: float = 1e-12) -> bool:
    return bool(np.allclose(A, A.T, atol=atol))


def matriz_eh_definida_positiva(autovalores: np.ndarray, tol: float = 1e-12) -> bool:
    return bool(np.all(autovalores > tol))


def run_cases(max_iter: int = 300, tolerancia: float = 1e-10) -> list[ResultadoCG]:
    """Executa os cinco casos solicitados dos slides 13 e 14."""
    casos = [
        ("o = 1.0, k = 2*pi", 1.0, 2 * pi),
        ("o = 1.0, k = 2*pi*31", 1.0, 2 * pi * 31),
        ("o = 1.0, k = 2*pi*33", 1.0, 2 * pi * 33),
        ("o = 1.0, k = 2*pi*50", 1.0, 2 * pi * 50),
        ("o = 0.5, k = 2*pi", 0.5, 2 * pi),
    ]

    resultados: list[ResultadoCG] = []
    for nome, o, k in casos:
        x_grid, A, f, h = build_vib_string_case(o=o, k=k)
        autovalores = np.linalg.eigvalsh(A)
        solucao_direta = np.linalg.solve(A, f)
        solucao_cg, residuos = conjugate_gradient(
            A,
            f,
            max_iter=max_iter,
            tolerancia=tolerancia,
        )

        resultados.append(
            ResultadoCG(
                caso=nome,
                o=o,
                k=k,
                h=h,
                simetrica=matriz_eh_simetrica(A),
                definida_positiva=matriz_eh_definida_positiva(autovalores),
                menor_autovalor=float(autovalores[0]),
                iteracoes=len(residuos) - 1,
                residuo_final=residuos[-1],
                x_grid=x_grid,
                A=A,
                f=f,
                solucao_direta=solucao_direta,
                solucao_cg=solucao_cg,
                residuos=residuos,
            )
        )

    return resultados


def formatar_resultado(resultado: ResultadoCG) -> str:
    return "\n".join(
        [
            resultado.caso,
            f"  h: {resultado.h:.5g}",
            f"  matriz simétrica: {'sim' if resultado.simetrica else 'não'}",
            "  definida positiva: "
            f"{'sim' if resultado.definida_positiva else 'não'}",
            f"  menor autovalor: {resultado.menor_autovalor:.6e}",
            f"  iterações CG: {resultado.iteracoes}",
            f"  norma final do resíduo: {resultado.residuo_final:.6e}",
        ]
    )


def matriz_do_exemplo_tau(n: int, tau: float, rng: np.random.Generator) -> np.ndarray:
    """Gera a matriz do experimento adicional antigo com parametro tau."""
    superior = rng.uniform(-1.0, 1.0, size=(n, n))
    superior = np.triu(superior, k=1)
    A = superior + superior.T
    A[np.abs(A) > tau] = 0.0
    np.fill_diagonal(A, 1.0)
    return A


def rodar_caso_tau(n: int, tau: float, seed: int, max_iter: int) -> ResultadoTau:
    """Executa o experimento adicional antigo com matriz aleatoria."""
    rng = np.random.default_rng(seed)
    A = matriz_do_exemplo_tau(n, tau, rng)
    b = rng.uniform(-1.0, 1.0, size=n)
    x, residuos = conjugate_gradient(A, b, max_iter=max_iter)

    autovalores = np.linalg.eigvalsh(A)
    menor = float(autovalores[0])
    maior = float(autovalores[-1])
    condicao = maior / menor if menor > 0 else None

    return ResultadoTau(
        tau=tau,
        iteracoes=len(residuos) - 1,
        nao_zeros=int(np.count_nonzero(A)),
        condicao=condicao,
        menor_autovalor=menor,
        x=x,
        residuos=residuos,
    )


def main() -> None:
    for i, resultado in enumerate(run_cases()):
        print(formatar_resultado(resultado))
        if i != 4:
            print()


if __name__ == "__main__":
    main()
