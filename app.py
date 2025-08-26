import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import tempfile

st.set_page_config(page_title="Gerador de Cronograma TJPE", layout="centered")

st.title("📚 Gerador de Cronograma")

# Inputs do usuário
titulo = st.text_input("Título do Documento", "")
subtitulo = st.text_input("Período e Horário", "")

st.markdown("### Nomes das Colunas")
col1 = st.text_input("Coluna 1", value="", placeholder="Ex: Data")
col2 = st.text_input("Coluna 2", value="", placeholder="Ex: Legislação")
col3 = st.text_input("Coluna 3", value="", placeholder="Ex: Artigos do Dia")
col4 = st.text_input("Coluna 4", value="", placeholder="Ex: Destaques IBFC")
col5 = st.text_input("Coluna 5", value="", placeholder="Ex: Concluído")

st.markdown("### Dados do Cronograma")
data_input = st.text_area(
    "Insira os dados separados por vírgula (uma linha por registro):",
    height=250,
    placeholder='Exemplo:\n06/08/2025, Fundamentos da AWS, Cap 1 ao 10, Cap 7 e 9, Sim'
)

if st.button("📄 Gerar PDF"):
    dados = [[col1, col2, col3, col4, col5]]
    linhas = data_input.strip().split("\n")

    for linha in linhas:
        partes = [parte.strip() for parte in linha.split(",")]
        if len(partes) == 5:
            dados.append(partes)
        else:
            st.warning(f"Linha ignorada (colunas inválidas): {linha}")

    styles = getSampleStyleSheet()
    flowables = [
        Paragraph(f"<b>{titulo}</b>", styles["Title"]),
        Spacer(1, 12),
        Paragraph(subtitulo, styles["Normal"]),
        Spacer(1, 12),
        Table(dados, repeatRows=1, style=TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
    ]

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmpfile:
        doc = SimpleDocTemplate(tmpfile.name, pagesize=A4)
        doc.build(flowables)
        st.success("✅ PDF gerado com sucesso!")
        with open(tmpfile.name, "rb") as file:
            st.download_button(label="📥 Baixar PDF", data=file, file_name="cronograma_tjpe.pdf")
