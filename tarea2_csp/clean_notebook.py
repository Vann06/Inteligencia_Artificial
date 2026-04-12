"""
Limpia Tarea2_CSP.ipynb:
  - Quita emojis y caracteres de dibujo de caja (box-drawing)
  - Simplifica separadores y headers de secciones
  - Deja el codigo limpio y directo
"""
import json
import re

SRC  = "Tarea2_CSP.ipynb"
DEST = "Tarea2_CSP.ipynb"

# ── 1. Cargar notebook ────────────────────────────────────────
with open(SRC, encoding="utf-8") as f:
    nb = json.load(f)

# ── 2. Tablas de sustituciones ────────────────────────────────

# Caracteres individuales a reemplazar
CHAR_MAP = {
    # Box-drawing simple
    "─": "-",
    "━": "-",
    "═": "=",
    "│": "|",
    "┃": "|",
    "├": "+",
    "└": "+",
    "┘": "+",
    "┐": "+",
    "┌": "+",
    "┤": "+",
    "┬": "+",
    "┴": "+",
    "┼": "+",
    # Box-drawing doble
    "╔": "+",
    "╗": "+",
    "╚": "+",
    "╝": "+",
    "╠": "+",
    "╣": "+",
    "╦": "+",
    "╩": "+",
    "╬": "+",
    "║": "|",
    # Block elements (barras visuales)
    "█": "#",
    "░": ".",
    "▓": "#",
    "▒": ".",
    # Flechas y bullets
    "•": "-",
    "→": "->",
    "←": "<-",
    "↓": "v",
    "·": ".",
    "≡": "==",
    "≠": "!=",
    "∈": "in",
    "∪": "U",
    "←": "<-",
    # Emojis comunes usados en el notebook
    "✅": "[OK]",
    "❌": "[FAIL]",
    "⚠️": "[WARN]",
    "⏱️": "[TIME]",
    "📊": "",
    "📝": "",
    "🔬": "",
}

# Regex: elimina cualquier emoji restante (rangos Unicode)
EMOJI_RE = re.compile(
    "["
    "\U0001F300-\U0001F9FF"   # Misc symbols, pictographs, emoticons, transport
    "\U00002600-\U000027BF"   # Misc technical, dingbats
    "\U0000FE00-\U0000FE0F"   # Variation selectors
    "\U00002702-\U000027B0"
    "]",
    flags=re.UNICODE,
)

# Simplificar lineas de separacion largas generadas por "*70" o "*58" etc.
# Ejemplo:  "========================================================================"
# → "=" * 60 queda como una linea larga, la acortamos a 58 chars max
SEP_RE = re.compile(r"([=\-+|]{10,})")


def clean_line(line: str) -> str:
    """Aplica todas las sustituciones a una linea de texto."""
    # 1. Reemplazar caracteres del mapa
    for old, new in CHAR_MAP.items():
        line = line.replace(old, new)
    # 2. Eliminar emojis restantes
    line = EMOJI_RE.sub("", line)
    # 3. Acortar separadores muy largos (mas de 60 chars consecutivos)
    def shorten_sep(m):
        ch  = m.group(0)[0]
        lng = min(len(m.group(0)), 58)
        return ch * lng
    line = SEP_RE.sub(shorten_sep, line)
    # 4. Quitar espacios al final
    line = line.rstrip()
    return line


def clean_source(source: str) -> str:
    """Limpia el contenido completo de una celda."""
    lines = source.split("\n")
    cleaned = [clean_line(l) for l in lines]
    # Colapsar lineas de solo separadores consecutivas (> 2 seguidas)
    result = []
    sep_count = 0
    for l in cleaned:
        stripped = l.strip()
        is_sep = stripped and all(c in "=-+" for c in stripped)
        if is_sep:
            sep_count += 1
            if sep_count <= 1:
                result.append(l)
        else:
            sep_count = 0
            result.append(l)
    return "\n".join(result)


# ── 3. Procesar celdas ────────────────────────────────────────
modified = 0
for cell in nb["cells"]:
    src = cell.get("source", "")
    if not isinstance(src, str):
        src = "".join(src)
    new_src = clean_source(src)
    if new_src != src:
        cell["source"] = new_src
        modified += 1
    # Limpiar outputs tambien (por si hay emojis en texto impreso)
    for output in cell.get("outputs", []):
        for key in ("text", "traceback"):
            raw = output.get(key)
            if isinstance(raw, list):
                output[key] = [clean_source(l) for l in raw]
            elif isinstance(raw, str):
                output[key] = clean_source(raw)

# ── 4. Guardar ────────────────────────────────────────────────
with open(DEST, "w", encoding="utf-8") as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

print(f"[OK] Notebook limpiado: {DEST}")
print(f"     Celdas modificadas : {modified}/{len(nb['cells'])}")
