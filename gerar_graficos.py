"""Gera graficos para o relatorio do estudo dirigido."""

from __future__ import annotations

import os
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", ".matplotlib_cache")

import matplotlib.pyplot as plt

from gradientes_conjugados import rodar_caso


def main() -> None:
    n = 500
    max_iter = 20
    seed_base = 22915
    taus = [0.01, 0.05, 0.1, 0.2]
    saida = Path("graficos")
    saida.mkdir(exist_ok=True)

    resultados = [
        rodar_caso(n=n, tau=tau, seed=seed_base + i, max_iter=max_iter)
        for i, tau in enumerate(taus)
    ]

    plt.style.use("seaborn-v0_8-whitegrid")

    fig, ax = plt.subplots(figsize=(8, 5), dpi=160)
    for resultado in resultados:
        iteracoes = range(len(resultado.residuos))
        ax.semilogy(
            iteracoes,
            resultado.residuos,
            marker="o",
            linewidth=1.8,
            markersize=4,
            label=f"tau = {resultado.tau}",
        )
    ax.set_title("Convergencia do Metodo dos Gradientes Conjugados")
    ax.set_xlabel("Iteracao")
    ax.set_ylabel("Norma do residuo ||r_n||")
    ax.set_xlim(0, max_iter)
    ax.legend()
    fig.tight_layout()
    fig.savefig(saida / "convergencia_residuo.png")
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(8, 5), dpi=160)
    for resultado in resultados:
        r0 = resultado.residuos[0]
        residuos_relativos = [r / r0 for r in resultado.residuos]
        iteracoes = range(len(residuos_relativos))
        ax.semilogy(
            iteracoes,
            residuos_relativos,
            marker="o",
            linewidth=1.8,
            markersize=4,
            label=f"tau = {resultado.tau}",
        )
    ax.set_title("Residuo Relativo por Iteracao")
    ax.set_xlabel("Iteracao")
    ax.set_ylabel("Residuo relativo ||r_n|| / ||r_0||")
    ax.set_xlim(0, max_iter)
    ax.legend()
    fig.tight_layout()
    fig.savefig(saida / "convergencia_residuo_relativo.png")
    plt.close(fig)

    fig, ax1 = plt.subplots(figsize=(8, 5), dpi=160)
    x = [str(resultado.tau) for resultado in resultados]
    nao_zeros = [resultado.nao_zeros for resultado in resultados]
    condicoes = [
        resultado.condicao if resultado.condicao is not None else float("nan")
        for resultado in resultados
    ]

    ax1.bar(x, nao_zeros, color="#4C78A8", alpha=0.8, label="Nao zeros")
    ax1.set_xlabel("tau")
    ax1.set_ylabel("Quantidade de elementos nao zeros", color="#4C78A8")
    ax1.tick_params(axis="y", labelcolor="#4C78A8")

    ax2 = ax1.twinx()
    ax2.plot(
        x,
        condicoes,
        color="#F58518",
        marker="o",
        linewidth=2,
        label="Numero de condicao",
    )
    ax2.set_ylabel("Numero de condicao", color="#F58518")
    ax2.tick_params(axis="y", labelcolor="#F58518")

    ax1.set_title("Efeito de tau na Esparsidade e no Condicionamento")
    ax1.text(3, nao_zeros[-1] * 0.84, "matriz nao SPD", ha="center", fontsize=9)
    fig.tight_layout()
    fig.savefig(saida / "esparsidade_condicionamento.png")
    plt.close(fig)

    for arquivo in sorted(saida.glob("*.png")):
        print(arquivo)


if __name__ == "__main__":
    main()
