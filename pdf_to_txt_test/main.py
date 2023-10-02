import PyPDF2 as pdf

pdf_file_name = "capsulas_sql"
pdf_file = open(f"pdf_files/{pdf_file_name}.pdf", "rb")
pdf_reader = pdf.PdfReader(pdf_file)

pages_number = len(pdf_reader.pages)
final_txt = ""

for page_number in range(pages_number):
    page_object = pdf_reader.pages[page_number]
    final_txt += page_object.extract_text()

text_file = open(f"{pdf_file_name}.txt", "w")
text_file.write(final_txt)
text_file.close()
