"""Gera gráficos para o relatório do estudo dirigido."""

from __future__ import annotations

import os
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", str(Path(".matplotlib_cache").resolve()))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from gradientes_conjugados import ResultadoCG, run_cases


def titulo_caso(indice: int, resultado: ResultadoCG) -> str:
    multiplicador = round(resultado.k / (2 * 3.141592653589793))
    k_txt = "2π" if multiplicador == 1 else f"2π*{multiplicador}"
    return f"Caso {indice}: o = {resultado.o:.1f}, k = {k_txt}"


def nome_arquivo_caso(indice: int, resultado: ResultadoCG) -> str:
    o_txt = str(resultado.o).replace(".", "p")
    k_txt = round(resultado.k / (2 * 3.141592653589793))
    return f"vib_string_caso_{indice}_o_{o_txt}_k_2pi_{k_txt}.png"


def plot_results(resultados: list[ResultadoCG], pasta_saida: Path) -> list[Path]:
    """Gera gráficos comparando solução direta, CG e resíduo por caso."""
    pasta_saida.mkdir(exist_ok=True)
    plt.style.use("seaborn-v0_8-whitegrid")
    arquivos: list[Path] = []

    for indice, resultado in enumerate(resultados, start=1):
        fig, (ax_sol, ax_res) = plt.subplots(2, 1, figsize=(8, 7), dpi=160)

        ax_sol.plot(
            resultado.x_grid,
            resultado.solucao_direta,
            label="Solução direta",
            linewidth=2,
        )
        ax_sol.plot(
            resultado.x_grid,
            resultado.solucao_cg,
            "--",
            label="Gradientes Conjugados",
            linewidth=2,
        )
        ax_sol.set_title(titulo_caso(indice, resultado))
        ax_sol.set_xlabel("x")
        ax_sol.set_ylabel("Deslocamento")
        ax_sol.legend()

        iteracoes = range(len(resultado.residuos))
        ax_res.semilogy(iteracoes, resultado.residuos, marker="o", linewidth=1.8)
        ax_res.set_xlabel("Iteração")
        ax_res.set_ylabel("Norma do resíduo ||r_n||")
        ax_res.set_title("Convergência do resíduo")

        fig.tight_layout()
        caminho = pasta_saida / nome_arquivo_caso(indice, resultado)
        fig.savefig(caminho)
        plt.close(fig)
        arquivos.append(caminho)

    fig, ax = plt.subplots(figsize=(8, 5), dpi=160)
    for indice, resultado in enumerate(resultados, start=1):
        ax.semilogy(
            range(len(resultado.residuos)),
            resultado.residuos,
            marker="o",
            linewidth=1.8,
            markersize=4,
            label=titulo_caso(indice, resultado),
        )
    ax.set_title("Comparação das curvas de resíduo - vib_string.m")
    ax.set_xlabel("Iteração")
    ax.set_ylabel("Norma do resíduo ||r_n||")
    ax.legend(fontsize=8)
    fig.tight_layout()
    caminho = pasta_saida / "vib_string_residuos_comparacao.png"
    fig.savefig(caminho)
    plt.close(fig)
    arquivos.append(caminho)

    return arquivos


def main() -> None:
    arquivos = plot_results(run_cases(), Path("graficos"))
    for arquivo in arquivos:
        print(arquivo)


if __name__ == "__main__":
    main()
