import tkinter as tk
from tkinter import PanedWindow, filedialog, scrolledtext, messagebox
from chordpro_parser import parse_chordpro, format_line_for_display, extract_and_format_title
from pdf_exporter import export_to_pdf
from word_operations import add_landscape_page_to_word

def create_start_screen():
    global text_area, preview_area

    window = tk.Tk()
    window.title("ChordPro Editor")

    p_window = PanedWindow(window, orient=tk.HORIZONTAL)
    p_window.pack(fill=tk.BOTH, expand=True)

    left_panel = tk.Frame(p_window)
    button_frame = tk.Frame(left_panel)
    button_frame.pack(pady=10)

    # Bestehende Buttons
    load_button = tk.Button(button_frame, text="ChordPro-Datei laden", command=lambda: load_chordpro_file())
    load_button.pack(side=tk.LEFT, padx=5)

    save_button = tk.Button(button_frame, text="Änderungen speichern", command=lambda: save_chordpro_file())
    save_button.pack(side=tk.LEFT, padx=5)

    export_button = tk.Button(button_frame, text="Als PDF exportieren", command=lambda: export_to_pdf(text_area))
    export_button.pack(side=tk.LEFT, padx=5)

    display_button = tk.Button(button_frame, text="ChordPro formatieren", command=lambda: update_preview())
    display_button.pack(side=tk.LEFT, padx=5)

    # Neuer Button für das Hinzufügen einer Seite im Querformat zu einem Word-Dokument
    add_page_button = tk.Button(button_frame, text="Seite zu Word", command=lambda: add_page_to_word())
    add_page_button.pack(side=tk.LEFT, padx=5)

    text_area = scrolledtext.ScrolledText(left_panel, wrap=tk.WORD, height=15, width=50)
    text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
    text_area['font'] = ('consolas', '12')

    p_window.add(left_panel)

    right_panel = tk.Frame(p_window)
    preview_area = scrolledtext.ScrolledText(right_panel, wrap=tk.WORD, height=15, width=50)
    preview_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
    preview_area['font'] = ('consolas', '12')

    p_window.add(right_panel)

    window.mainloop()

def add_page_to_word():
    file_path = filedialog.askopenfilename(filetypes=[("Word documents", "*.docx")])
    if file_path:
        add_landscape_page_to_word(file_path)
        messagebox.showinfo("Erfolg", "Eine Seite im Querformat wurde hinzugefügt.")


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

def update_preview():
    file_content = text_area.get('1.0', tk.END)
    parsed_content = parse_chordpro(file_content)
    title = extract_and_format_title(file_content)

    preview_area.delete('1.0', tk.END)
    if title:
        preview_area.insert(tk.END, title + '\n\n')

    for chords, text in parsed_content:
        chord_line, text_line = format_line_for_display(chords, text)
        preview_area.insert(tk.END, chord_line + '\n')
        preview_area.insert(tk.END, text_line + '\n\n')