import tkinter as tk
from tkinter import filedialog, scrolledtext, Toplevel, PanedWindow
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from itertools import zip_longest
import re  # Importieren Sie das re-Modul für reguläre Ausdrücke

def load_chordpro_file():
    global file_path
    file_path = filedialog.askopenfilename(filetypes=[("ChordPro files", "*.pro"), ("Text files", "*.txt")])
    if file_path:
        with open(file_path, 'r') as file:
            text_area.delete('1.0', tk.END)
            text_area.insert(tk.END, file.read())

def save_chordpro_file():
    if file_path:
        with open(file_path, 'w') as file:
            file.write(text_area.get('1.0', tk.END))

def parse_chordpro(file_content):
    lines = file_content.split('\n')
    parsed_lines = []

    for line in lines:
        if '[' in line and ']' in line:  # Akkorde in dieser Zeile
            text_parts = []
            chord_parts = []
            current_chord = ''
            current_text = ''
            in_chord = False
            for char in line:
                if char == '[':
                    in_chord = True
                    text_parts.append(current_text)
                    current_text = ''
                elif char == ']':
                    in_chord = False
                    chord_parts.append(current_chord)
                    current_chord = ''
                elif in_chord:
                    current_chord += char
                else:
                    current_text += char
            text_parts.append(current_text)  # Füge den letzten Textteil hinzu

            parsed_lines.append((chord_parts, text_parts))
        else:
            parsed_lines.append(([], [line]))  # Nur Textzeile

    return parsed_lines

def format_chordpro_for_pdf(parsed_content):
    formatted_lines = []
    for chords, texts in parsed_content:
        chord_line = ' '.join(f'[{chord}]' for chord in chords)
        text_line = ''.join(texts)
        formatted_lines.append((chord_line, text_line))
    return formatted_lines

def export_to_pdf():
    parsed_content = parse_chordpro(text_area.get('1.0', tk.END))
    formatted_content = format_chordpro_for_pdf(parsed_content)

    pdf_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
    if pdf_path:
        c = canvas.Canvas(pdf_path, pagesize=letter)
        textobject = c.beginText(40, 750)
        textobject.setFont("Courier", 12)

        for chord_line, text_line in formatted_content:
            textobject.textLine(chord_line)
            textobject.moveCursor(0, -15)
            textobject.textLine(text_line)
            textobject.moveCursor(0, -15)

        c.drawText(textobject)
        c.save()

def parse_and_display_chordpro():
    raw_content = text_area.get('1.0', tk.END)
    parsed_content = parse_chordpro(raw_content)

    # Neues Fenster zum Anzeigen des formatierten Textes
    display_window = Toplevel(window)
    display_window.title("Formatierte ChordPro-Ansicht")
    formatted_text_area = scrolledtext.ScrolledText(display_window, wrap=tk.WORD, height=15, width=50)
    formatted_text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
    formatted_text_area['font'] = ('consolas', '12')

    # Formatieren und Anzeigen des Inhalts
    for chords, texts in parsed_content:
        chord_line = ' '.join(f'[{chord}]' for chord in chords)
        text_line = ''.join(texts)
        formatted_text_area.insert(tk.END, chord_line + '\n' + text_line + '\n\n')

def update_preview():
    raw_content = text_area.get('1.0', tk.END)
    parsed_content = parse_chordpro(raw_content)
    formatted_content = format_chordpro_for_pdf(parsed_content)

    # Leere die Vorschau und füge den formatierten Inhalt hinzu
    preview_area.delete('1.0', tk.END)
    for chord_line, text_line in formatted_content:
        # Wenn die Zeile Daten in geschwungenen Klammern enthält, überspringe sie
        if re.search(r'\{.*?\}', chord_line) or re.search(r'\{.*?\}', text_line):
            continue
        preview_area.insert(tk.END, chord_line + '\n' + text_line + '\n\n')
        
def create_start_screen():
    global window, text_area, preview_area
    window = tk.Tk()
    window.title("ChordPro Editor")

    # Erstellen eines PanedWindow für den Split-Screen-Effekt
    p_window = PanedWindow(window, orient=tk.HORIZONTAL)
    p_window.pack(fill=tk.BOTH, expand=True)

    # Linker Bereich: Textfeld und Buttons
    left_panel = tk.Frame(p_window)
    button_frame = tk.Frame(left_panel)
    button_frame.pack(pady=10)

    load_button = tk.Button(button_frame, text="ChordPro-Datei laden", command=load_chordpro_file)
    load_button.pack(side=tk.LEFT, padx=5)

    save_button = tk.Button(button_frame, text="Änderungen speichern", command=save_chordpro_file)
    save_button.pack(side=tk.LEFT, padx=5)

    export_button = tk.Button(button_frame, text="Als PDF exportieren", command=export_to_pdf)
    export_button.pack(side=tk.LEFT, padx=5)

    display_button = tk.Button(button_frame, text="ChordPro formatieren", command=update_preview)
    display_button.pack(side=tk.LEFT, padx=5)

    text_area = scrolledtext.ScrolledText(left_panel, wrap=tk.WORD, height=15, width=50)
    text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
    text_area['font'] = ('consolas', '12')

    p_window.add(left_panel)

    # Rechter Bereich: Vorschau
    right_panel = tk.Frame(p_window)
    preview_area = scrolledtext.ScrolledText(right_panel, wrap=tk.WORD, height=15, width=50)
    preview_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
    preview_area['font'] = ('consolas', '12')

    p_window.add(right_panel)

    window.mainloop()

if __name__ == "__main__":
    create_start_screen()
