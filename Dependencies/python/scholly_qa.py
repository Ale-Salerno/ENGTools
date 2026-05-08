#!/usr/bin/env python3
"""
Scholly QA: Pixel QA Tool (Self-Contained).

- Finds all *.csv files.
- Generates interactive 'report_*.html' files.
- Embeds fonts directly into the HTML so reports are portable.
"""

import pandas as pd
import os
import re
import glob
import html
import base64

def get_font_base64_url(filename):
    """
    Reads a font file and returns a Base64 data URI for CSS embedding.
    Falls back to the filename (relative path) if the file is missing locally.
    """
    if not os.path.exists(filename):
        print(f"    Warning: Font '{filename}' not found for embedding. Report will use relative path fallback.")
        return filename

    # Determine format for CSS
    ext = os.path.splitext(filename)[1].lower()
    if ext == '.ttf':
        font_format = 'truetype'
    elif ext == '.otf':
        font_format = 'opentype'
    else:
        font_format = 'woff' # generic fallback

    try:
        with open(filename, "rb") as f:
            encoded_string = base64.b64encode(f.read()).decode('utf-8')
            return f"data:font/{font_format};charset=utf-8;base64,{encoded_string}"
    except Exception as e:
        print(f"    Error embedding font {filename}: {e}")
        return filename

def parse_single_csv(filepath):
    """Parses a single CSV file and returns its translation units."""
    
    print(f"  Parsing {filepath}...")
    units_data = []
    
    expected_columns = {
        'id_col': 'Variable Name',
        'bold_col': 'bold',
        'font_size_col': 'font size',
        'height_col': 'height in px',
        'lines_col': 'max no of lines',
        'width_col': 'max width in px',
        'text_col': 'Translation',
        'export_date_col': 'Export Date'
    }
    
    try:
        # Load the CSV
        df = pd.read_csv(filepath, sep=';')
        
        missing_cols = [col for col in expected_columns.values() if col not in df.columns]
        if missing_cols:
            print(f"    ERROR: CSV file '{filepath}' is missing expected columns: {missing_cols}.")
            return None

        for row in df.to_dict('records'):
            trans_data = {
                'id': str(row[expected_columns['id_col']]),
                'resname': str(row[expected_columns['id_col']]),
                'maxwidth': 'N/A', 
                'source': str(row[expected_columns['text_col']]),
                'target': str(row[expected_columns['text_col']]), 
                'target_state': 'n/a',
                'bold': str(row[expected_columns['bold_col']]),
                'font_size': str(row[expected_columns['font_size_col']]),
                'height': str(row[expected_columns['height_col']]),
                'width': str(row[expected_columns['width_col']]),
                'lines': str(row[expected_columns['lines_col']]),
                'export_date': str(row[expected_columns['export_date_col']])
            }
            units_data.append(trans_data)

    except pd.errors.EmptyDataError:
        print(f"    Warning: CSV file '{filepath}' is empty. Skipping.")
        return None
    except KeyError as e:
        print(f"    ERROR: CSV file '{filepath}' had a column mapping error: {e}.")
        return None
    except pd.errors.ParserError as e:
        print(f"    ERROR: Pandas could not parse the file. {e}")
        return None
    except Exception as e:
        print(f"    An error occurred with {filepath}: {e}")
        return None

    print(f"  Found {len(units_data)} translation units.")
    return units_data


def generate_html_report(units_data, output_filename, source_filename):
    """Generates a single HTML report for a list of translation units."""
    
    if not units_data:
        print(f"  No units to report for {source_filename}.")
        return

    # --- EMBED FONTS ---
    # Convert local font files to Base64 strings to make the HTML self-contained
    print("    Embedding fonts into HTML...")
    font_bbraun_reg = get_font_base64_url('BBraunTypeDigital-Regular.otf')
    font_bbraun_bold = get_font_base64_url('BBraunTypeDigital-Bold.otf')
    font_source_reg = get_font_base64_url('SourceSans3-Regular.ttf')
    font_source_bold = get_font_base64_url('SourceSans3-Bold.ttf')
    # -------------------

    total_units = len(units_data)
    
    def wrap_variables_editor(text):
        variable_regex = r"(\{.*?\})"
        parts = re.split(variable_regex, str(text))
        processed_parts = []
        for part in parts:
            if re.match(variable_regex, part):
                processed_parts.append(f'<span class="variable" contenteditable="false">{html.escape(part)}</span>')
            else:
                processed_parts.append(html.escape(part))
        return "".join(processed_parts)
        
    def wrap_variables_preview(text):
        variable_regex = r"(\{.*?\})"
        parts = re.split(variable_regex, str(text))
        processed_parts = []
        counter = 1
        for part in parts:
            if re.match(variable_regex, part):
                processed_parts.append(f'<span class="variable" contenteditable="false">{{{counter}}}</span>')
                counter += 1
            else:
                processed_parts.append(html.escape(part))
        return "".join(processed_parts)

    html_template = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Pixel Report: {source_filename}</title>
        <style>
            html {{ scroll-padding-top: 150px; }}
            
            /* EMBEDDED FONTS */
            @font-face {{ 
                font-family: 'BBraunTypeDigital'; 
                font-weight: 400; 
                src: url('{font_bbraun_reg}') format('opentype'); 
            }}
            @font-face {{ 
                font-family: 'BBraunTypeDigital'; 
                font-weight: 700; 
                src: url('{font_bbraun_bold}') format('opentype'); 
            }}
            @font-face {{ 
                font-family: 'SourceSans3'; 
                font-weight: 400; 
                src: url('{font_source_reg}') format('truetype'); 
            }}
            @font-face {{ 
                font-family: 'SourceSans3'; 
                font-weight: 700; 
                src: url('{font_source_bold}') format('truetype'); 
            }}

            body {{ font-family: sans-serif; background-color: #F8F9FA; color: #333; margin: 0; padding: 0; }}
            p {{ margin: 5px 0; }}
            #summary {{ background: #fff; border-bottom: 1px solid #ccc; padding: 0; margin: 0 0 20px 0; position: sticky; top: 0; z-index: 1000; width: 100%; box-shadow: 0 4px 8px rgba(0,0,0,0.15); display: flex; flex-direction: column; }}
            .summary-content {{ max-width: 1200px; margin: 0 auto; padding: 15px 25px; display: flex; flex-direction: column; width: 100%; box-sizing: border-box; }}
            .summary-header {{ display: flex; justify-content: space-between; align-items: flex-start; border-bottom: 2px solid #eee; padding-bottom: 15px; margin-bottom: 15px; gap: 20px; }}
            .title-block {{ display: flex; flex-direction: column; }}
            #summary h2 {{ margin: 0; text-align: left; flex-shrink: 0; }}
            .filename-title {{ text-align: left; margin: 5px 0 0 0; font-family: sans-serif; font-weight: 400; font-size: 0.9em; color: #777; }}
            #summary-layout {{ display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 20px; }}
            #summary-counts {{ display: flex; justify-content: space-around; flex-basis: 400px; flex-grow: 1; text-align: center; }}
            #total-count {{ color: #537FFF; font-size: 1.5em; font-weight: bold; }}
            #compliant-count {{ color: #12B76A; font-size: 1.5em; font-weight: bold; }}
            #to-fix-count {{ color: #d9534f; font-size: 1.5em; font-weight: bold; }}
            #modified-count {{ color: #FE8523; font-size: 1.5em; font-weight: bold; }}
            #filter-controls {{ display: flex; flex-wrap: wrap; align-items: flex-start; gap: 20px 25px; flex-basis: 500px; flex-grow: 10; border-left: 2px solid #eee; padding-left: 25px; }}
            .filter-section, .navigation-section {{ display: flex; align-items: flex-start; gap: 15px; }}
            .filter-title {{ font-size: 1.1em; font-weight: bold; margin: 0; color: #333; flex-shrink: 0; padding-top: 8px; }}
            .filter-buttons {{ display: flex; flex-wrap: wrap; gap: 5px; }}
            .filter-buttons button {{ font-family: sans-serif; background-color: #f0f0f0; color: #333; border: 2px solid transparent; padding: 7px 11px; margin: 0; border-radius: 4px; cursor: pointer; font-size: 0.9em; font-weight: bold; transition: all 0.2s; }}
            .filter-buttons button:hover {{ background-color: #ddd; border-color: #bbb; }}
            .filter-buttons button#btn-all.active {{ border-color: #537FFF; background-color: #e6f0ff; }}
            .filter-buttons button#btn-compliant.active {{ border-color: #12B76A; background-color: #eafbf0; }}
            .filter-buttons button#btn-to-fix.active {{ border-color: #d9534f; background-color: #fdeeee; }}
            .filter-buttons button#btn-modified.active {{ border-color: #FE8523; background-color: #fefaf0; }}
            #btn-next-to-fix {{ background-color: #d9534f; color: white; border-color: #d9534f; }}
            #btn-next-to-fix:hover {{ background-color: #c9302c; border-color: #c9302c; }}
            #btn-next-modified {{ background-color: #FE8523; color: white; border-color: #FE8523; }}
            #btn-next-modified:hover {{ background-color: #F46E01; border-color: #F46E01; }}
            .summary-header .filter-buttons {{ flex-shrink: 0; }}
            #btn-export-json {{ background-color: #537FFF; color: white; border-color: #537FFF; }}
            #btn-export-json:hover {{ background-color: #4565D2; border-color: #4565D2; }}
            #report-container {{ padding: 0 20px; }}
            .unit {{ background-color: #ffffff; border: 1px solid #ccc; border-radius: 8px; padding: 15px; margin: 0 auto 20px auto; max-width: 1200px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); border-left: 5px solid #fff; }}
            .unit h2 {{ margin-top: 0; color: #537FFF; }}
            .meta {{ font-size: 0.9em; color: #555; background: #eee; padding: 8px; border-radius: 4px; line-height: 1.6; }}
            .source-text {{ font-style: italic; color: #777; border-bottom: 1px dashed #ddd; padding-bottom: 10px; margin-bottom: 10px; word-wrap: break-word; }}
            .font-header {{ font-weight: bold; margin-top: 15px; margin-bottom: 2px; color: #444; }}
            .font-block.second-font {{ margin-top: 15px; }}
            .constraint-box {{ background: #fafafa; overflow: hidden; word-wrap: break-word; padding: 0; border: 2px dashed #FE8523; }}
            .box-ok {{ border: 2px solid #12B76A; }}
            .box-fail {{ border: 2px solid #d9534f; }}
            .unit.status-compliant {{ border-left: 5px solid #12B76A; }}
            .unit.status-to-fix {{ background-color: #fffafaf0; border-color: #d9534f; border-left: 5px solid #d9534f; }}
            .unit.status-modified {{ background-color: #FFFFFF; }}
            .unit.status-modified.status-to-fix {{ background-color: #fff5f5; }}
            .unit.status-user-modified {{ border-left: 5px solid #FE8523; }}
            .live-edit-area {{ margin-top: 15px; }}
            .live-edit-area label {{ font-size: 0.9em; color: #555; font-weight: bold; }}
            .live-edit-div {{ width: 98%; min-height: 40px; padding: 5px; font-family: sans-serif; font-size: 14px; border: 1px solid #ccc; border-radius: 4px; margin-top: 5px; resize: vertical; overflow: auto; background-color: #fff; }}
            .variable {{ background-color: #f0f0f0; color: #444; border-radius: 3px; padding: 1px 3px; cursor: not-allowed; font-family: monospace; font-size: 0.95em; user-select: none; }}
            .target-text {{ margin: 0 !important; padding: 0 !important; line-height: 1.1; display: block; white-space: normal; word-wrap: break-word; overflow-wrap: break-word; }}
            .target-text[data-lines="1"] {{ white-space: nowrap; overflow: hidden; text-overflow: clip; }}
            .bbraun-font {{ font-family: 'BBraunTypeDigital', sans-serif; }}
            .source-sans-font {{ font-family: 'SourceSans3', sans-serif; }}
            .char-count b {{ font-weight: 700; }}
            .char-count.char-ok b {{ color: #12B76A; }}
            .char-count.char-exceeded b {{ color: #d9534f; }}
            @media (max-width: 900px) {{
                .summary-header {{ flex-direction: column; align-items: stretch; border-bottom: none; padding-bottom: 0; margin-bottom: 0; }}
                .summary-header .filter-buttons {{ margin-top: 15px; }}
                .summary-header .filter-buttons button {{ width: 100%; box-sizing: border-box; padding: 10px 12px; }}
                #summary-layout {{ flex-direction: column; align-items: stretch; }}
                #filter-controls {{ flex-direction: column; align-items: center; border-left: none; padding-left: 0; margin-top: 15px; border-top: 2px solid #eee; padding-top: 15px; text-align: center; }}
                .filter-title {{ padding-top: 0; text-align: center; }}
                .filter-section, .navigation-section {{ flex-direction: column; align-items: center; width: 100%; }}
            }}
            @media (max-width: 1250px) {{ .summary-content {{ padding: 15px 25px; }} }}
        </style>
    </head>
    <body>
        <div id="summary">
            <div class="summary-content">
                <div class="summary-header">
                    <div class="title-block">
                        <h2>Pixel Constraints QA</h2>
                        <h3 class="filename-title">{source_filename}</h3>
                    </div>
                    <div class="filter-buttons">
                        <button id="btn-export-json">Export Update</button>
                    </div>
                </div>
                <div id="summary-layout">
                    <div id="summary-counts">
                        <div><strong>Total</strong><br><span id="total-count">{total_units}</span></div>
                        <div><strong>Compliant</strong><br><span id="compliant-count">0</span></div>
                        <div><strong>To Fix</strong><br><span id="to-fix-count">0</span></div>
                        <div><strong>Modified</strong><br><span id="modified-count">0</span></div>
                    </div>
                    <div id="filter-controls">
                        <div class="filter-section">
                            <h3 class="filter-title">Filters:</h3>
                            <div class="filter-buttons">
                                <button id="btn-all" class="active">Show All</button>
                                <button id="btn-compliant">Compliant</button>
                                <button id="btn-to-fix">To Fix</button>
                                <button id="btn-modified">Modified</button>
                            </div>
                        </div>
                        <div class="navigation-section">
                            <div class="filter-buttons">
                                <button id="btn-next-to-fix">Next To Fix</button>
                                <button id="btn-next-modified">Next Modified</button>
                            </div>
                        </div>
                        </div>
                </div>
            </div>
        </div>
        <div id="report-container">
    """
    
    html_body = ""
    for unit in units_data:
        resname = html.escape(unit['resname'])
        uid = html.escape(unit['id'])
        export_date_escaped = html.escape(unit['export_date'])
        
        source_text_wrapped_preview = wrap_variables_preview(unit['source'])
        target_text_escaped = html.escape(unit['target'])
        target_text_wrapped_editor = wrap_variables_editor(unit['target'])
        target_text_wrapped_preview = wrap_variables_preview(unit['target'])
        
        target_state_escaped = html.escape(unit['target_state'])
        is_modified = target_state_escaped == 'translated'
        modified_class = "status-modified" if is_modified else "status-unmodified"
        safe_id = re.sub(r'[^a-zA-Z0-9_-]', '_', f"{uid}")

        font_weight = '700' if unit['bold'] == '1' else '400'
        font_weight_label = 'Bold' if unit['bold'] == '1' else 'Regular'
        font_size_px = f"{unit['font_size']}px"
        box_width_px = f"{unit['width']}px"
        box_height_px = f"{unit['height']}px"
        max_lines = unit['lines']
        max_width_chars = html.escape(unit['maxwidth'])
        initial_char_count = len(unit['target'])
        
        box_style = f"width: {box_width_px}; height: {box_height_px};"
        text_style = f"font-size: {font_size_px}; font-weight: {font_weight};"
        allowed_html = f" | Allowed: <b>{max_width_chars}</b>" if max_width_chars != 'N/A' else ""
            
        html_body += f"""
        <div class="unit {modified_class}" id="unit-{safe_id}">
            <h2 data-resname="{resname}">{resname}</h2>
            <p class="meta">
                <strong>ID:</strong> <b>{uid}</b><br>
                <strong>Export Date:</strong> <b>{export_date_escaped}</b><br> <strong>Pixel Constraints:</strong> 
                Width: <b>{box_width_px}</b> | Height: <b>{box_height_px}</b> | Font Size: <b>{font_size_px}</b> | 
                Weight: <b>{font_weight_label}</b> | Max Lines: <b>{max_lines}</b> <br>
                <strong>Characters:</strong> Current: <span id="char-count-{safe_id}" class="char-count" data-limit="{max_width_chars}"><b>{initial_char_count}</b></span>{allowed_html}
            </p>
            <p class="source-text"><strong>Source:</strong> {source_text_wrapped_preview}</p>
            <div class="live-edit-area">
                <label for="edit-{safe_id}">Live Edit Preview:</label>
                <div id="edit-{safe_id}" class="live-edit-div" contenteditable="true" data-original="{target_text_escaped}">{target_text_wrapped_editor}</div>
            </div>
            <div class="font-block">
                <h4 class="font-header">BBraunTypeDigital:</h4>
                <div class="constraint-box" id="box-bbraun-{safe_id}" style="{box_style}">
                    <p class="target-text bbraun-font" style="{text_style}" data-lines="{max_lines}">{target_text_wrapped_preview}</p>
                </div>
            </div>
            <div class="font-block second-font">
                <h4 class="font-header">SourceSans3:</h4>
                <div class="constraint-box" id="box-source-{safe_id}" style="{box_style}">
                    <p class="target-text source-sans-font" style="{text_style}" data-lines="{max_lines}">{target_text_wrapped_preview}</p>
                </div>
            </div>
        </div>
        """

    html_footer = f"""
        </div> 
        <script>
            const source_xlf_filename = "{html.escape(source_filename)}";
            let currentFilter = 'all'; 
            let currentToFixIndex = 0;
            let currentModifiedIndex = 0;

            function checkSingleUnit(unit) {{
                let unit_has_overflow = false;
                const boxes = unit.querySelectorAll('.constraint-box');
                boxes.forEach(box => {{
                    const text = box.querySelector('.target-text');
                    if (!text) return;
                    box.classList.remove('box-ok', 'box-fail');
                    const is_overflowing = (
                        (text.scrollHeight > box.clientHeight + 2) || 
                        (text.scrollWidth > box.clientWidth + 2)
                    );
                    if (is_overflowing) {{
                        box.classList.add('box-fail');
                        unit_has_overflow = true;
                    }} else {{
                        box.classList.add('box-ok');
                    }}
                }});
                unit.classList.remove('status-to-fix', 'status-compliant');
                if (unit_has_overflow) {{
                    unit.classList.add('status-to-fix');
                }} else {{
                    unit.classList.add('status-compliant');
                }}
                return unit_has_overflow;
            }}
            
            function checkAllConstraints() {{
                let compliant_units = 0;
                let to_fix_units = 0;
                let modified_units = 0; 
                const units = document.querySelectorAll('.unit');
                units.forEach(unit => {{
                    const has_overflow = checkSingleUnit(unit);
                    if (has_overflow) to_fix_units++; else compliant_units++;
                    if (unit.classList.contains('status-user-modified')) modified_units++;
                }});
                document.getElementById('compliant-count').innerText = compliant_units;
                document.getElementById('to-fix-count').innerText = to_fix_units;
                document.getElementById('modified-count').innerText = modified_units;
                applyCurrentFilter();
            }};

            function checkCharCount(span, current_length) {{
                if (!span) return;
                const limit_str = span.dataset.limit;
                span.classList.remove('char-ok', 'char-exceeded');
                if (limit_str && limit_str !== 'N/A' && /^\\d+$/.test(limit_str)) {{
                    const limit = parseInt(limit_str, 10);
                    if (current_length > limit) span.classList.add('char-exceeded'); else span.classList.add('char-ok');
                }} else {{
                    span.classList.add('char-ok');
                }}
            }}

            function checkAllCharCounts() {{
                document.querySelectorAll('.char-count').forEach(span => {{
                    const current_length = parseInt(span.querySelector('b').innerText, 10);
                    checkCharCount(span, current_length);
                }});
            }}
            
            function applyCurrentFilter() {{
                const all_units = document.querySelectorAll('.unit');
                all_units.forEach(unit => {{
                    if (currentFilter === 'all') unit.style.display = 'block';
                    else if (currentFilter === 'compliant') unit.style.display = unit.classList.contains('status-compliant') ? 'block' : 'none';
                    else if (currentFilter === 'to-fix') unit.style.display = unit.classList.contains('status-to-fix') ? 'block' : 'none';
                    else if (currentFilter === 'modified') unit.style.display = unit.classList.contains('status-user-modified') ? 'block' : 'none';
                }});
            }}

            function filterUnits(status_to_show) {{
                currentFilter = status_to_show;
                applyCurrentFilter();
                document.getElementById('btn-all').classList.toggle('active', currentFilter === 'all');
                document.getElementById('btn-compliant').classList.toggle('active', currentFilter === 'compliant');
                document.getElementById('btn-to-fix').classList.toggle('active', currentFilter === 'to-fix');
                document.getElementById('btn-modified').classList.toggle('active', currentFilter === 'modified');
                currentToFixIndex = 0;
                currentModifiedIndex = 0;
            }}

            function goToNextToFix() {{
                if (currentFilter !== 'all') filterUnits('all');
                const toFixUnits = document.querySelectorAll('.status-to-fix');
                if (toFixUnits.length > 0) {{
                    if (currentToFixIndex >= toFixUnits.length) currentToFixIndex = 0;
                    toFixUnits[currentToFixIndex].scrollIntoView({{ behavior: 'smooth', block: 'center' }});
                    currentToFixIndex++;
                }} else {{ currentToFixIndex = 0; }}
            }}
            
            function goToNextModified() {{
                if (currentFilter !== 'all') filterUnits('all');
                const modifiedUnits = document.querySelectorAll('.status-user-modified');
                if (modifiedUnits.length > 0) {{
                    if (currentModifiedIndex >= modifiedUnits.length) currentModifiedIndex = 0;
                    modifiedUnits[currentModifiedIndex].scrollIntoView({{ behavior: 'smooth', block: 'center' }});
                    currentModifiedIndex++;
                }} else {{ currentModifiedIndex = 0; }}
            }}

            function exportModifiedTranslations() {{
                let changes = {{}};
                const modifiedUnits = document.querySelectorAll('.unit.status-user-modified');
                if (modifiedUnits.length === 0) {{ alert("No modifications found to export."); return; }}
                modifiedUnits.forEach(unit => {{
                    const resname = unit.querySelector('h2').dataset.resname;
                    const newText = unit.querySelector('.live-edit-div').innerText; 
                    changes[resname] = newText;
                }});
                const exportData = {{ "source_xlf": source_xlf_filename, "modified_units": changes }};
                const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(exportData, null, 2));
                const downloadAnchorNode = document.createElement('a');
                downloadAnchorNode.setAttribute("href", dataStr);
                downloadAnchorNode.setAttribute("download", source_xlf_filename + ".json");
                document.body.appendChild(downloadAnchorNode); 
                downloadAnchorNode.click();
                downloadAnchorNode.remove();
            }}
            
            function generatePreviewHtml(editorHtml) {{
                const tempDiv = document.createElement('div');
                tempDiv.innerHTML = editorHtml;
                let previewHtml = "";
                let counter = 1;
                tempDiv.childNodes.forEach(node => {{
                    if (node.nodeType === Node.TEXT_NODE) {{
                        previewHtml += node.textContent;
                    }} else if (node.nodeType === Node.ELEMENT_NODE && node.classList.contains('variable')) {{
                        previewHtml += `<span class="variable" contenteditable="false">{{${{counter}}}}</span>`;
                        counter++;
                    }} else if (node.nodeType === Node.ELEMENT_NODE) {{
                        previewHtml += node.outerHTML;
                    }}
                }});
                return previewHtml;
            }}

            function setupLiveEditListeners() {{
                document.querySelectorAll('.live-edit-div').forEach(div => {{
                    const originalValue = div.dataset.original;
                    div.addEventListener('input', function(e) {{
                        const newEditorHtml = e.target.innerHTML; 
                        const newText = e.target.innerText; 
                        const unit = e.target.closest('.unit');
                        if (!unit) return;
                        const safe_id = e.target.id.substring(5); 
                        const charCountSpan = document.getElementById('char-count-' + safe_id);
                        if (charCountSpan) {{
                            charCountSpan.querySelector('b').innerText = newText.length;
                            checkCharCount(charCountSpan, newText.length); 
                        }}
                        if (newText !== originalValue) unit.classList.add('status-user-modified');
                        else unit.classList.remove('status-user-modified');
                        const newPreviewHtml = generatePreviewHtml(newEditorHtml);
                        unit.querySelectorAll('.target-text').forEach(target => {{ target.innerHTML = newPreviewHtml; }});
                        checkAllConstraints();
                    }});
                }});
            }}
            
            window.onload = function() {{
                checkAllConstraints();
                checkAllCharCounts(); 
                document.getElementById('btn-all').addEventListener('click', () => filterUnits('all'));
                document.getElementById('btn-compliant').addEventListener('click', () => filterUnits('compliant'));
                document.getElementById('btn-to-fix').addEventListener('click', () => filterUnits('to-fix'));
                document.getElementById('btn-modified').addEventListener('click', () => filterUnits('modified'));
                document.getElementById('btn-next-to-fix').addEventListener('click', goToNextToFix);
                document.getElementById('btn-next-modified').addEventListener('click', goToNextModified);
                document.getElementById('btn-export-json').addEventListener('click', exportModifiedTranslations);
                setupLiveEditListeners();
                filterUnits(currentFilter);
            }};
        </script>
    </body>
    </html>
    """
    
    try:
        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write(html_template + html_body + html_footer)
        print(f"  Success! Report generated: {output_filename}")
    except IOError as e:
        print(f"  Error writing HTML file: {e}")

def main():
    print("--- CSV Constraint Report Generator (Task: QA) ---")
    print("--- Mode: Self-Contained HTML (Embedded Fonts) ---")
    
    csv_files = glob.glob('*.csv')
    
    if not csv_files:
        print("Error: No .csv files found in this directory.")
        print("Please place this script in the same folder as your .csv and font files.")
        return

    print(f"Found {len(csv_files)} CSV file(s).")
    
    # Check for fonts locally just to warn the user if they are missing
    # The generation function handles the fallback, but it's good UX to warn here too.
    fonts_found = []
    for ext in ['*.otf', '*.ttf']:
        fonts_found.extend(glob.glob(ext))
    
    if not fonts_found:
        print("\n--- WARNING ---")
        print("No .otf or .ttf font files found in this directory.")
        print("The report will use relative paths, so it WON'T be portable/self-contained.")
        print("To fix: Place the font files in this folder and run the script again.")
        print("---------------\n")
    else:
        print(f"Found font files (will be embedded): {', '.join(fonts_found)}")

    for filepath in csv_files:
        if "report_" in filepath or "updated_" in filepath: 
            print(f"  Skipping generated file: {filepath}")
            continue
            
        units = parse_single_csv(filepath)
        
        if units:
            base_filename = os.path.basename(filepath)
            output_name = f"report_{base_filename}.html"
            generate_html_report(units, output_name, base_filename)
        else:
            print(f"  No valid translation units found in {filepath}.")

    print("\nAll reports generated.")

if __name__ == "__main__":
    main()