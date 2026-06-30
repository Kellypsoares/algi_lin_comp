# algi_lin_comp

Estudo dirigido de Álgebra Linear Computacional sobre o método dos Gradientes
Conjugados.

O caso principal reproduz o exemplo `vib_string.m` dos slides 13 e 14 da aula
`MIT2_29S15_Lecture8 - Iterative.pdf`. O experimento antigo com matrizes
aleatórias e parâmetro `tau` foi mantido apenas como teste adicional, separado
do fluxo principal.

## Como rodar

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python gradientes_conjugados.py
.venv/bin/python gerar_graficos.py
.venv/bin/python gerar_relatorio_pdf.py
.venv/bin/python gerar_relatorio_docx.py
```

Os resultados já calculados estão em `ESTUDO_DIRIGIDO.md`.
O relatório está disponível em `relatorio_gradientes_conjugados.pdf` e
`relatorio_gradientes_conjugados.docx`.

Repositório GitHub: https://github.com/Kellypsoares/algi_lin_comp
