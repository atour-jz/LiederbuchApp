import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib.units import inch
import re  # Importieren Sie das re-Modul für reguläre Ausdrücke
from tkinter import PanedWindow


def create_start_screen():
    global text_area, preview_area

    window = tk.Tk()
    window.title("ChordPro Editor")

    # Erstellen eines PanedWindow für den Split-Screen-Effekt
    p_window = PanedWindow(window, orient=tk.HORIZONTAL)
    p_window.pack(fill=tk.BOTH, expand=True)

    # Linker Bereich: Textfeld und Buttons
    left_panel = tk.Frame(p_window)
    button_frame = tk.Frame(left_panel)
    button_frame.pack(pady=10)

    load_button = tk.Button(button_frame, text="ChordPro-Datei laden", command=lambda: load_chordpro_file())
    load_button.pack(side=tk.LEFT, padx=5)

    save_button = tk.Button(button_frame, text="Änderungen speichern", command=lambda: save_chordpro_file())
    save_button.pack(side=tk.LEFT, padx=5)

    export_button = tk.Button(button_frame, text="Als PDF exportieren", command=lambda: export_to_pdf())
    export_button.pack(side=tk.LEFT, padx=5)

    display_button = tk.Button(button_frame, text="ChordPro formatieren", command=lambda: update_preview())
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

# Globale Variablen 
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
    parsed_lines = []
    for line in file_content.split('\n'):
        chord_positions = []
        text_line = ""
        pos = 0
        while line:
            if line.startswith('['):
                line = line[1:]
                chord = line[:line.index(']')]
                line = line[line.index(']')+1:]
                chord_positions.append((chord, pos))
            else:
                text_line += line[0]
                pos += 1
                line = line[1:]
        parsed_lines.append((chord_positions, text_line))
    return parsed_lines

def format_line_for_display(chords, text):
    display_line = [" "] * (len(text) + max((pos for _, pos in chords), default=0))
    for chord, pos in chords:
        display_line[pos:pos+len(chord)] = chord
    return ''.join(display_line), text


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

        button_frame = tk.Frame(master)
        export_button = tk.Button(button_frame, text="Als PDF exportieren", command=export_to_pdf)

def parse_and_display_chordpro():
    raw_content = text_area.get('1.0', tk.END)
    parsed_content = parse_chordpro(raw_content)

    # Neues Fenster zum Anzeigen des formatierten Textes
    display_window = Toplevel(root)
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
    parsed_content = parse_chordpro(text_area.get('1.0', tk.END))
    preview_area.delete('1.0', tk.END)
    for chords, text in parsed_content:
        chord_line, text_line = format_line_for_display(chords, text)
        preview_area.insert(tk.END, chord_line + '\n' + text_line + '\n\n')
        
if __name__ == "__main__":
    create_start_screen()
