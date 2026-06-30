"""Gera uma versão DOCX do relatório do estudo dirigido."""

from __future__ import annotations

from html import escape
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

from PIL import Image

from gradientes_conjugados import ResultadoCG, run_cases


AUTORA = "Kelly Pinheiro Soares"
REPO_URL = "https://github.com/Kellypsoares/algi_lin_comp"
DOCX = Path("relatorio_gradientes_conjugados.docx")


def titulo_caso(indice: int, resultado: ResultadoCG) -> str:
    multiplicador = round(resultado.k / (2 * 3.141592653589793))
    k_txt = "2π" if multiplicador == 1 else f"2π*{multiplicador}"
    return f"Caso {indice}: o = {resultado.o:.1f}, k = {k_txt}"


def paragrafo(texto: str = "", estilo: str | None = None, alinhamento: str | None = None) -> str:
    props = []
    if estilo:
        props.append(f'<w:pStyle w:val="{estilo}"/>')
    if alinhamento:
        props.append(f'<w:jc w:val="{alinhamento}"/>')
    ppr = f"<w:pPr>{''.join(props)}</w:pPr>" if props else ""
    linhas = texto.split("\n")
    conteudo = []
    for i, linha in enumerate(linhas):
        if i:
            conteudo.append("<w:br/>")
        conteudo.append(f'<w:t xml:space="preserve">{escape(linha)}</w:t>')
    return f"<w:p>{ppr}<w:r>{''.join(conteudo)}</w:r></w:p>"


def hyperlink(texto: str, rel_id: str) -> str:
    return (
        '<w:p><w:hyperlink r:id="'
        + rel_id
        + '" w:history="1"><w:r><w:rPr><w:color w:val="0563C1"/>'
        + '<w:u w:val="single"/></w:rPr><w:t>'
        + escape(texto)
        + "</w:t></w:r></w:hyperlink></w:p>"
    )


def imagem(rel_id: str, nome: str, largura_pol: float = 6.4) -> str:
    caminho = Path(nome)
    with Image.open(caminho) as img:
        largura_px, altura_px = img.size
    altura_pol = largura_pol * altura_px / largura_px
    cx = int(largura_pol * 914400)
    cy = int(altura_pol * 914400)
    doc_pr_id = rel_id.replace("rId", "")
    return f"""
<w:p>
  <w:r>
    <w:drawing>
      <wp:inline distT="0" distB="0" distL="0" distR="0"
        xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing">
        <wp:extent cx="{cx}" cy="{cy}"/>
        <wp:docPr id="{doc_pr_id}" name="{escape(caminho.name)}"/>
        <a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
          <a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">
            <pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">
              <pic:nvPicPr>
                <pic:cNvPr id="0" name="{escape(caminho.name)}"/>
                <pic:cNvPicPr/>
              </pic:nvPicPr>
              <pic:blipFill>
                <a:blip r:embed="{rel_id}"/>
                <a:stretch><a:fillRect/></a:stretch>
              </pic:blipFill>
              <pic:spPr>
                <a:xfrm><a:off x="0" y="0"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>
                <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
              </pic:spPr>
            </pic:pic>
          </a:graphicData>
        </a:graphic>
      </wp:inline>
    </w:drawing>
  </w:r>
</w:p>
"""


def tabela(resultados: list[ResultadoCG]) -> str:
    headers = ["caso", "sim.", "SPD", "iter.", "menor autovalor", "||r_final||"]
    linhas = [headers]
    for indice, resultado in enumerate(resultados, start=1):
        linhas.append(
            [
                titulo_caso(indice, resultado),
                "sim" if resultado.simetrica else "não",
                "sim" if resultado.definida_positiva else "não",
                str(resultado.iteracoes),
                f"{resultado.menor_autovalor:.6g}",
                f"{resultado.residuo_final:.6e}",
            ]
        )

    rows = []
    for linha in linhas:
        larguras = [3600, 800, 800, 800, 1700, 1700]
        cells = "".join(
            f"<w:tc><w:tcPr><w:tcW w:w=\"{largura}\" w:type=\"dxa\"/></w:tcPr>"
            f"<w:p><w:r><w:t>{escape(celula)}</w:t></w:r></w:p></w:tc>"
            for celula, largura in zip(linha, larguras)
        )
        rows.append(f"<w:tr>{cells}</w:tr>")
    return (
        "<w:tbl><w:tblPr><w:tblStyle w:val=\"TableGrid\"/>"
        "<w:tblW w:w=\"0\" w:type=\"auto\"/></w:tblPr>"
        + "".join(rows)
        + "</w:tbl>"
    )


def styles_xml() -> str:
    return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:style w:type="paragraph" w:default="1" w:styleId="Normal">
    <w:name w:val="Normal"/>
    <w:rPr><w:sz w:val="22"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Title">
    <w:name w:val="Title"/>
    <w:rPr><w:b/><w:sz w:val="36"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading1">
    <w:name w:val="heading 1"/>
    <w:rPr><w:b/><w:sz w:val="28"/></w:rPr>
  </w:style>
</w:styles>
"""


def document_xml(resultados: list[ResultadoCG]) -> str:
    corpo = [
        paragrafo("Estudo Dirigido - Gradientes Conjugados", "Title", "center"),
        paragrafo("Álgebra Linear Computacional", alinhamento="center"),
        paragrafo(AUTORA, alinhamento="center"),
        paragrafo(),
        paragrafo("Repositório GitHub:", "Heading1"),
        hyperlink(REPO_URL, "rIdRepo"),
        paragrafo("Objetivo", "Heading1"),
        paragrafo(
            "Implementar o método iterativo dos Gradientes Conjugados conforme o "
            "algoritmo do slide 23 da aula MIT 2.29 Lecture 8 e rodar os casos "
            "do exemplo vib_string.m dos slides 13 e 14."
        ),
        paragrafo("Algoritmo implementado", "Heading1"),
        paragrafo(
            "v0 = r0 = b - A x0\n\n"
            "alpha_i = (v_i^T r_i) / (v_i^T A v_i)\n"
            "x_{i+1} = x_i + alpha_i v_i\n"
            "r_{i+1} = r_i - alpha_i A v_i\n"
            "beta_i = -(v_i^T A r_{i+1}) / (v_i^T A v_i)\n"
            "v_{i+1} = r_{i+1} + beta_i v_i"
        ),
        paragrafo("Casos do exemplo", "Heading1"),
        paragrafo(
            "Foi gerada uma matriz A tridiagonal de ordem 99, com h = L/(n+1) = "
            "0.01, diagonal principal igual a (k*h)^2 - 2, diagonais superior e "
            "inferior iguais a o, e vetor de força f construído com uma janela "
            "de Hanning conforme o código MATLAB dos slides."
        ),
        paragrafo("Gráficos", "Heading1"),
        paragrafo("Caso 1: o = 1.0, k = 2π"),
        imagem("rIdImg1", "graficos/vib_string_caso_1_o_1p0_k_2pi_1.png"),
        paragrafo("Caso 2: o = 1.0, k = 2π*31"),
        imagem("rIdImg2", "graficos/vib_string_caso_2_o_1p0_k_2pi_31.png"),
        paragrafo("Caso 3: o = 1.0, k = 2π*33"),
        imagem("rIdImg3", "graficos/vib_string_caso_3_o_1p0_k_2pi_33.png"),
        paragrafo("Caso 4: o = 1.0, k = 2π*50"),
        imagem("rIdImg4", "graficos/vib_string_caso_4_o_1p0_k_2pi_50.png"),
        paragrafo("Caso 5: o = 0.5, k = 2π"),
        imagem("rIdImg5", "graficos/vib_string_caso_5_o_0p5_k_2pi_1.png"),
        paragrafo("Comparação das curvas de resíduo"),
        imagem("rIdImg6", "graficos/vib_string_residuos_comparacao.png"),
        paragrafo("Resumo numérico", "Heading1"),
        tabela(resultados),
        paragrafo("Conclusão", "Heading1"),
        paragrafo(
            "O exemplo vib_string.m gera matrizes simétricas em todos os casos, "
            "porém nem todas são definidas positivas. O método dos Gradientes "
            "Conjugados possui garantia teórica de convergência apenas para "
            "matrizes simétricas definidas positivas. Nos casos em que essa "
            "condição foi satisfeita (k = 2π*33 e k = 2π*50), o método convergiu "
            "em poucas iterações e reproduziu a solução direta com alta precisão. "
            "Nos demais casos, embora o algoritmo tenha produzido uma aproximação "
            "e reduzido o resíduo, esses resultados devem ser interpretados com "
            "cautela, pois a convergência não é garantida pela teoria."
        ),
    ]
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<w:document xmlns:wpc="http://schemas.microsoft.com/office/word/2010/wordprocessingCanvas" '
        'xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006" '
        'xmlns:o="urn:schemas-microsoft-com:office:office" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
        'xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math" '
        'xmlns:v="urn:schemas-microsoft-com:vml" '
        'xmlns:wp14="http://schemas.microsoft.com/office/word/2010/wordprocessingDrawing" '
        'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" '
        'xmlns:w10="urn:schemas-microsoft-com:office:word" '
        'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
        'xmlns:w14="http://schemas.microsoft.com/office/word/2010/wordml" '
        'xmlns:wpg="http://schemas.microsoft.com/office/word/2010/wordprocessingGroup" '
        'xmlns:wpi="http://schemas.microsoft.com/office/word/2010/wordprocessingInk" '
        'xmlns:wne="http://schemas.microsoft.com/office/word/2006/wordml" '
        'xmlns:wps="http://schemas.microsoft.com/office/word/2010/wordprocessingShape" '
        'mc:Ignorable="w14 wp14"><w:body>'
        + "".join(corpo)
        + '<w:sectPr><w:pgSz w:w="11906" w:h="16838"/><w:pgMar w:top="1134" '
        'w:right="1134" w:bottom="1134" w:left="1134" w:header="708" '
        'w:footer="708" w:gutter="0"/></w:sectPr></w:body></w:document>'
    )


def rels_xml() -> str:
    return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>
"""


def document_rels_xml() -> str:
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rIdRepo" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink" Target="{REPO_URL}" TargetMode="External"/>
  <Relationship Id="rIdImg1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/vib_string_caso_1_o_1p0_k_2pi_1.png"/>
  <Relationship Id="rIdImg2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/vib_string_caso_2_o_1p0_k_2pi_31.png"/>
  <Relationship Id="rIdImg3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/vib_string_caso_3_o_1p0_k_2pi_33.png"/>
  <Relationship Id="rIdImg4" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/vib_string_caso_4_o_1p0_k_2pi_50.png"/>
  <Relationship Id="rIdImg5" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/vib_string_caso_5_o_0p5_k_2pi_1.png"/>
  <Relationship Id="rIdImg6" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/vib_string_residuos_comparacao.png"/>
</Relationships>
"""


def content_types_xml() -> str:
    return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Default Extension="png" ContentType="image/png"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
</Types>
"""


def main() -> None:
    resultados = run_cases()

    imagens = [
        (
            "graficos/vib_string_caso_1_o_1p0_k_2pi_1.png",
            "word/media/vib_string_caso_1_o_1p0_k_2pi_1.png",
        ),
        (
            "graficos/vib_string_caso_2_o_1p0_k_2pi_31.png",
            "word/media/vib_string_caso_2_o_1p0_k_2pi_31.png",
        ),
        (
            "graficos/vib_string_caso_3_o_1p0_k_2pi_33.png",
            "word/media/vib_string_caso_3_o_1p0_k_2pi_33.png",
        ),
        (
            "graficos/vib_string_caso_4_o_1p0_k_2pi_50.png",
            "word/media/vib_string_caso_4_o_1p0_k_2pi_50.png",
        ),
        (
            "graficos/vib_string_caso_5_o_0p5_k_2pi_1.png",
            "word/media/vib_string_caso_5_o_0p5_k_2pi_1.png",
        ),
        (
            "graficos/vib_string_residuos_comparacao.png",
            "word/media/vib_string_residuos_comparacao.png",
        ),
    ]

    with ZipFile(DOCX, "w", ZIP_DEFLATED) as docx:
        docx.writestr("[Content_Types].xml", content_types_xml())
        docx.writestr("_rels/.rels", rels_xml())
        docx.writestr("word/_rels/document.xml.rels", document_rels_xml())
        docx.writestr("word/styles.xml", styles_xml())
        docx.writestr("word/document.xml", document_xml(resultados))
        for origem, destino in imagens:
            docx.write(origem, destino)

    print(DOCX)


if __name__ == "__main__":
    main()
