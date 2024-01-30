from tkinter import Tk, filedialog, scrolledtext, messagebox
import tkinter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from chordpro_parser import extract_and_format_title, extract_ccli_info, extract_footer_info, extract_key, format_line_for_display, parse_chordpro, extract_artist
from chordpro_parser import extract_ccli_info

def extract_info(file_content):
    # Extrahieren Sie die erforderlichen Informationen aus dem ChordPro-Text
    title = extract_and_format_title(file_content)
    artist = extract_artist(file_content)
    key = extract_key(file_content)
    ccli_license, ccli = extract_ccli_info(file_content)
    copyright, footer = extract_footer_info(file_content)
    return title, artist, key, ccli_license, ccli, copyright, footer

def export_to_pdf(text_area):
    # Initialisiere Variablen
    line_count = 0
    y_position = letter[0] - 40
    x_position = 40
    right_align_x_position = letter[1] - 100

    file_content = text_area.get('1.0', tkinter.END)
    parsed_content = parse_chordpro(file_content)

    # Extrahiere die benötigten Informationen aus dem Inhalt
    title, artist, key, ccli_license, ccli, copyright, footer = extract_info(file_content)

    pdf_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
    if not pdf_path:
        return

    c = canvas.Canvas(pdf_path, pagesize=letter)
    c.setPageSize((letter[1], letter[0]))  # Setzt das PDF auf Querformat

    # Titel und Künstler darstellen
    if title:
        c.setFont("Helvetica-Bold", 14)
        c.drawString(x_position, y_position, title)
        y_position -= 30

    if artist:
        c.setFont("Helvetica-Oblique", 12)
        c.drawString(x_position, y_position, artist)
        y_position -= 20

    if key:
        c.setFont("Helvetica", 12)
        c.drawString(right_align_x_position, letter[0] - 40, f"Key: {key}")

    # Setze die Seitenfußzeilen
    footer_height = 20
    c.setFont("Helvetica", 9)
    c.drawString(letter[1] / 2, footer_height, f"{ccli_license}, {ccli}")
    c.drawString(letter[1] / 2, footer_height * 2, copyright)
    c.drawString(letter[1] / 2, footer_height * 3, footer)

    # Gehe durch den geparsten Inhalt und zeichne ihn auf das PDF
    for chords, text in parsed_content:
        max_lines_per_column = 17  # Define the maximum number of lines per column
        column_width = 400  # Define the width of each column

        if line_count >= max_lines_per_column:
            x_position += column_width
            y_position = letter[0] - 40
            line_count = 0

            if x_position >= letter[1] - 40:
                c.showPage()
                x_position = 40

        chord_line, text_line = format_line_for_display(chords, text)

        textobject = c.beginText(x_position, y_position)
        textobject.setFont("Courier", 12)
        textobject.textOut(chord_line)
        c.drawText(textobject)

        textobject = c.beginText(x_position, y_position - 15)
        textobject.setFont("Courier", 11)
        textobject.textOut(text_line)
        c.drawText(textobject)

        y_position -= 30
        line_count += 1
        print(line_count)
    c.save()
