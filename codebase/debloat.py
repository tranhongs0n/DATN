import os
import tokenize
import io

def remove_comments_and_docstrings(source):
    io_obj = io.StringIO(source)
    out = ""
    prev_toktype = tokenize.INDENT
    last_lineno = -1
    last_col = 0
    
    for tok in tokenize.generate_tokens(io_obj.readline):
        token_type = tok[0]
        token_string = tok[1]
        start_line, start_col = tok[2]
        end_line, end_col = tok[3]
        
        if start_line > last_lineno:
            last_col = 0
        if start_col > last_col:
            out += (" " * (start_col - last_col))
            
        if token_type == tokenize.COMMENT:
            pass
        elif token_type == tokenize.STRING:
            if prev_toktype != tokenize.INDENT:
                if prev_toktype != tokenize.NEWLINE:
                    if start_col > 0:
                        out += token_string
        else:
            out += token_string
            
        prev_toktype = token_type
        last_col = end_col
        last_lineno = end_line
        
    return out

def debloat_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        source = f.read()
    
    # Very simple line-by-line approach for comments to avoid AST issues
    new_lines = []
    lines = source.split('\n')
    in_docstring = False
    
    for line in lines:
        stripped = line.strip()
        
        # Simple docstring removal (only standalone """ docstrings)
        if stripped.startswith('\"\"\"') and stripped.endswith('\"\"\"') and len(stripped) > 3:
            continue
        elif stripped == '\"\"\"':
            in_docstring = not in_docstring
            continue
            
        if in_docstring:
            continue
            
        # Comment removal (only standalone comment lines)
        if stripped.startswith('#') and not stripped.startswith('# ' + 'HƯỚNG DẪN'):
            continue
            
        # Inline comment removal (risky with urls/hashes, so we skip unless it's very clear)
        # Actually, let's just remove standalone comments for safety.
        
        new_lines.append(line)
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(new_lines))
    print(f"Processed {filepath}")

for root, _, files in os.walk(r"D:\DATN_FInal\codebase\src"):
    for file in files:
        if file.endswith('.py'):
            debloat_file(os.path.join(root, file))

