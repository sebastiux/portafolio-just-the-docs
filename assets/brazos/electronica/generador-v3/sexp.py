"""Utilidades minimas para S-expressions de KiCad."""
import re


def extract_block(text, start):
    """Devuelve el bloque balanceado que empieza en text[start] == '('."""
    depth = 0
    i = start
    in_str = False
    while i < len(text):
        c = text[i]
        if in_str:
            if c == '\\':
                i += 2
                continue
            if c == '"':
                in_str = False
        else:
            if c == '"':
                in_str = True
            elif c == '(':
                depth += 1
            elif c == ')':
                depth -= 1
                if depth == 0:
                    return text[start:i + 1]
        i += 1
    raise ValueError('bloque sin cerrar')


def lib_symbol(lib_path, name, lib_nick):
    """Bloque (symbol "Lib:Name" ...) listo para lib_symbols de un .kicad_sch."""
    t = open(lib_path).read()
    m = re.search(r'\n  \(symbol "%s"' % re.escape(name), t)
    if not m:
        raise KeyError(name)
    blk = extract_block(t, m.start() + 3)
    assert '(extends' not in blk[:400], f'{name} usa extends'
    return blk.replace(f'(symbol "{name}"', f'(symbol "{lib_nick}:{name}"', 1)


def pins_of(block):
    """[(numero, nombre, x, y, angulo, tipo)] en coordenadas de simbolo (y hacia arriba)."""
    out = []
    for m in re.finditer(r'\(pin (\w+) \w+ \(at ([-\d.]+) ([-\d.]+) (\d+)\) \(length [\d.]+\)', block):
        rest = block[m.end():m.end() + 400]
        name = re.search(r'\(name "([^"]*)"', rest).group(1)
        num = re.search(r'\(number "([^"]*)"', rest).group(1)
        out.append((num, name, float(m.group(2)), float(m.group(3)), int(m.group(4)), m.group(1)))
    return out
