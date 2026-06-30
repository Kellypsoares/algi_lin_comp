"""Gera o relatório em PDF do estudo dirigido."""

from __future__ import annotations

import os
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", str(Path(".matplotlib_cache").resolve()))

import matplotlib

matplotlib.use("Agg")
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

from gradientes_conjugados import ResultadoCG, run_cases


REPO_URL = "https://github.com/Kellypsoares/algi_lin_comp"
AUTORA = "Kelly Pinheiro Soares"


def titulo_caso(indice: int, resultado: ResultadoCG) -> str:
    multiplicador = round(resultado.k / (2 * 3.141592653589793))
    k_txt = "2π" if multiplicador == 1 else f"2π*{multiplicador}"
    return f"Caso {indice}: o = {resultado.o:.1f}, k = {k_txt}"


def adicionar_texto(ax: plt.Axes, x: float, y: float, texto: str, **kwargs) -> None:
    ax.text(x, y, texto, transform=ax.transAxes, **kwargs)


def configurar_pagina() -> tuple[plt.Figure, plt.Axes]:
    fig, ax = plt.subplots(figsize=(8.27, 11.69), dpi=160)
    ax.axis("off")
    return fig, ax


def pagina_capa(pdf: PdfPages) -> None:
    fig, ax = configurar_pagina()
    adicionar_texto(
        ax,
        0.5,
        0.86,
        "Estudo Dirigido\nGradientes Conjugados",
        ha="center",
        va="top",
        fontsize=24,
        fontweight="bold",
    )
    adicionar_texto(
        ax,
        0.5,
        0.72,
        "Álgebra Linear Computacional",
        ha="center",
        va="top",
        fontsize=15,
    )
    adicionar_texto(
        ax,
        0.5,
        0.66,
        AUTORA,
        ha="center",
        va="top",
        fontsize=13,
    )
    adicionar_texto(
        ax,
        0.12,
        0.55,
        "Objetivo\n"
        "Implementar o método iterativo dos Gradientes Conjugados conforme o "
        "algoritmo do slide 23 da aula MIT 2.29 Lecture 8 e rodar os casos "
        "do exemplo vib_string.m dos slides 13 e 14.",
        ha="left",
        va="top",
        fontsize=12,
        linespacing=1.5,
        wrap=True,
    )
    adicionar_texto(
        ax,
        0.12,
        0.35,
        f"Repositório GitHub:\n{REPO_URL}",
        ha="left",
        va="top",
        fontsize=12,
        color="#1f5fbf",
        linespacing=1.5,
        url=REPO_URL,
    )
    adicionar_texto(
        ax,
        0.12,
        0.20,
        "Arquivos principais: gradientes_conjugados.py, gerar_graficos.py e "
        "ESTUDO_DIRIGIDO.md.",
        ha="left",
        va="top",
        fontsize=11,
        color="#333333",
        wrap=True,
    )
    pdf.savefig(fig)
    plt.close(fig)


def pagina_algoritmo(pdf: PdfPages) -> None:
    fig, ax = configurar_pagina()
    adicionar_texto(
        ax,
        0.08,
        0.94,
        "Algoritmo implementado",
        ha="left",
        va="top",
        fontsize=18,
        fontweight="bold",
    )
    texto = (
        "Para resolver Ax = b, com A simétrica definida positiva, o método usa "
        "direções A-conjugadas e atualiza a solução aproximada a cada iteração.\n\n"
        "v0 = r0 = b - A x0\n\n"
        "alpha_i = (v_i^T r_i) / (v_i^T A v_i)\n"
        "x_{i+1} = x_i + alpha_i v_i\n"
        "r_{i+1} = r_i - alpha_i A v_i\n"
        "beta_i = -(v_i^T A r_{i+1}) / (v_i^T A v_i)\n"
        "v_{i+1} = r_{i+1} + beta_i v_i"
    )
    adicionar_texto(
        ax,
        0.08,
        0.84,
        texto,
        ha="left",
        va="top",
        fontsize=12,
        linespacing=1.6,
        family="monospace",
        wrap=True,
    )
    casos = (
        "Casos do exemplo\n\n"
        "- n = 99;\n"
        "- L = 1.0 e h = L/(n+1) = 0.01;\n"
        "- matriz tridiagonal A;\n"
        "- diagonal principal igual a (k*h)^2 - 2;\n"
        "- diagonais superior e inferior iguais a o;\n"
        "- vetor de força f com janela de Hanning;\n"
        "- chute inicial x0 = 0;\n"
        "- casos: k = 2π, 2π*31, 2π*33, 2π*50 e o = 0.5."
    )
    adicionar_texto(
        ax,
        0.08,
        0.42,
        casos,
        ha="left",
        va="top",
        fontsize=12,
        linespacing=1.5,
        wrap=True,
    )
    pdf.savefig(fig)
    plt.close(fig)


def pagina_grafico(pdf: PdfPages, titulo: str, caminho: Path) -> None:
    fig, ax = configurar_pagina()
    adicionar_texto(
        ax,
        0.08,
        0.95,
        titulo,
        ha="left",
        va="top",
        fontsize=18,
        fontweight="bold",
    )
    imagem = mpimg.imread(caminho)
    ax.imshow(imagem, extent=(0.07, 0.93, 0.20, 0.84), aspect="auto")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    pdf.savefig(fig)
    plt.close(fig)


def pagina_tabela(pdf: PdfPages, resultados: list[ResultadoCG]) -> None:
    fig, ax = configurar_pagina()
    adicionar_texto(
        ax,
        0.08,
        0.95,
        "Resumo numérico",
        ha="left",
        va="top",
        fontsize=18,
        fontweight="bold",
    )
    colunas = [
        "caso",
        "sim.",
        "SPD",
        "iter.",
        "menor autovalor",
        "||r_final||",
    ]
    linhas = []
    for resultado in resultados:
        linhas.append(
            [
                titulo_caso(len(linhas) + 1, resultado),
                "sim" if resultado.simetrica else "não",
                "sim" if resultado.definida_positiva else "não",
                str(resultado.iteracoes),
                f"{resultado.menor_autovalor:.6g}",
                f"{resultado.residuo_final:.6e}",
            ]
        )

    tabela = ax.table(
        cellText=linhas,
        colLabels=colunas,
        loc="center",
        cellLoc="center",
        colLoc="center",
        colWidths=[0.35, 0.10, 0.10, 0.10, 0.18, 0.17],
        bbox=[0.02, 0.47, 0.96, 0.30],
    )
    tabela.auto_set_font_size(False)
    tabela.set_fontsize(7.5)
    for (linha, _), celula in tabela.get_celld().items():
        celula.set_edgecolor("#666666")
        if linha == 0:
            celula.set_facecolor("#e8eef7")
            celula.set_text_props(fontweight="bold")

    conclusao = (
        "Conclusão\n\n"
        "O exemplo vib_string.m gera matrizes simétricas em todos os casos, mas "
        "nem todas são definidas positivas. O método dos Gradientes Conjugados "
        "tem garantia teórica para matrizes simétricas definidas positivas; por "
        "isso, os casos com menor autovalor negativo devem ser interpretados "
        "com cuidado. Nos casos k = 2π*33 e k = 2π*50, a matriz é definida "
        "positiva e o método converge em poucas iterações."
    )
    adicionar_texto(
        ax,
        0.08,
        0.36,
        conclusao,
        ha="left",
        va="top",
        fontsize=11.5,
        linespacing=1.5,
        wrap=True,
    )
    pdf.savefig(fig)
    plt.close(fig)


def main() -> None:
    saida = Path("relatorio_gradientes_conjugados.pdf")
    graficos = Path("graficos")
    resultados = run_cases()
    arquivos_graficos = [
        graficos / "vib_string_caso_1_o_1p0_k_2pi_1.png",
        graficos / "vib_string_caso_2_o_1p0_k_2pi_31.png",
        graficos / "vib_string_caso_3_o_1p0_k_2pi_33.png",
        graficos / "vib_string_caso_4_o_1p0_k_2pi_50.png",
        graficos / "vib_string_caso_5_o_0p5_k_2pi_1.png",
        graficos / "vib_string_residuos_comparacao.png",
    ]

    with PdfPages(saida) as pdf:
        pagina_capa(pdf)
        pagina_algoritmo(pdf)
        for indice, arquivo in enumerate(arquivos_graficos[:5], start=1):
            pagina_grafico(pdf, titulo_caso(indice, resultados[indice - 1]), arquivo)
        pagina_grafico(pdf, "Comparação das curvas de resíduo", arquivos_graficos[-1])
        pagina_tabela(pdf, resultados)

    print(saida)


if __name__ == "__main__":
    main()
