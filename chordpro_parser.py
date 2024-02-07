import re

def parse_chordpro(file_content):
    # Logik zum Parsen der ChordPro-Dateien
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
    # Logik zur Formatierung der ChordPro-Zeilen für die Anzeige
    display_line = [" "] * (len(text) + max((pos for _, pos in chords), default=0))
    for chord, pos in chords:
        display_line[pos:pos+len(chord)] = chord
    return ''.join(display_line), text

def extract_and_format_title(file_content):
    # Extrahieren und Formatieren des Titels aus dem ChordPro-Inhalt
    title_match = re.search(r'\{title:\s*(.*?)\}', file_content)
    if title_match:
        return title_match.group(1)  # Gibt den Titel ohne "{title:" und "}" zurück
    return None

def extract_artist(file_content):
    match = re.search(r'\{artist:\s*(.*?)\}', file_content)
    return match.group(1) if match else None

def extract_key(file_content):
    match = re.search(r'\{key:\s*(.*?)\}', file_content)
    return match.group(1) if match else None

def extract_tempo(file_content):
    match = re.search(r'\{tempo:\s*(.*?)\}', file_content)
    return match.group(1) if match else None

def extract_ccli_info(file_content):
    ccli_license_match = re.search(r'\{ccli_license:\s*(.*?)\}', file_content)
    ccli_match = re.search(r'\{ccli:\s*(.*?)\}', file_content)
    ccli_license = ccli_license_match.group(1) if ccli_license_match else None
    ccli = ccli_match.group(1) if ccli_match else None
    return ccli_license, ccli

def extract_footer_info(file_content):
    copyright_match = re.search(r'\{copyright:\s*(.*?)\}', file_content)
    footer_match = re.search(r'\{footer:\s*(.*?)\}', file_content)
    copyright = copyright_match.group(1) if copyright_match else None
    footer = footer_match.group(1) if footer_match else None
    return copyright, footer
