import os
import sys
import re
import traceback
import xml.etree.ElementTree as ET
import platform

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QListWidget, QListWidgetItem, QFileDialog, QLabel,
    QLineEdit, QMessageBox, QCheckBox, QScrollArea, QFrame, QGridLayout
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPalette, QColor

##############################################################################
# CUSTOM FILE LIST WIDGET (DRAG & DROP)
##############################################################################
class FileListWidget(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setSelectionMode(QListWidget.ExtendedSelection)
        self.setDropIndicatorShown(True)
    
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()
    
    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()
    
    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            files = []
            for url in event.mimeData().urls():
                file_path = url.toLocalFile()
                if os.path.isfile(file_path):
                    files.append(file_path)
            if hasattr(self.window(), "handleDroppedFiles"):
                self.window().handleDroppedFiles(files)
            event.acceptProposedAction()
        else:
            event.ignore()

##############################################################################
# THEME DETECTION
##############################################################################
def detect_system_theme():
    if platform.system().lower() == "windows":
        try:
            import winreg
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize"
            )
            value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
            winreg.CloseKey(key)
            return "light" if value == 1 else "dark"
        except Exception:
            pass
    return "light"

##############################################################################
# REMOVE ALL NAMESPACES
##############################################################################
def remove_all_namespaces(root):
    for el in root.iter():
        if isinstance(el.tag, str) and el.tag.startswith("{"):
            el.tag = el.tag.split("}", 1)[1]
        new_attrib = {}
        for k, v in el.attrib.items():
            if not k.startswith("{"):
                new_attrib[k] = v
        el.attrib = new_attrib

##############################################################################
# HELPER FUNCTION: GET INNER XML (without outer tag)
##############################################################################
def get_inner_xml(elem):
    """
    Returns the inner XML (all text including child tags) of an element.
    """
    parts = []
    if elem.text:
        parts.append(elem.text)
    for child in elem:
        parts.append(ET.tostring(child, encoding="unicode", method="xml"))
        if child.tail:
            parts.append(child.tail)
    return "".join(parts)

##############################################################################
# HELPER FUNCTION: STRIP ALL TAGS
##############################################################################
def strip_tags(text):
    """
    Remove all XML/HTML tags from text.
    This function removes:
      - Literal tags: <...>
      - Escaped tags: &lt;...&gt;
      - Double-escaped tags: &amp;lt;...&amp;gt;
    """
    text = re.sub(r'<.*?>', '', text, flags=re.DOTALL)
    text = re.sub(r'&lt;.*?&gt;', '', text, flags=re.DOTALL)
    text = re.sub(r'&amp;lt;.*?&amp;gt;', '', text, flags=re.DOTALL)
    return text

##############################################################################
# MODELS
##############################################################################
class SegmentData:
    def __init__(self, segment_id, raw_text, xml_element, current_maxlen=""):
        self.id = segment_id
        self.raw_text = raw_text  # EXACT raw <source> or <seg-source> block
        self.xml_element = xml_element
        self.check_box = None
        self.maxlen_label = None
        self.current_maxlen = current_maxlen

class TranslationFileData:
    def __init__(self, file_path, segments, xml_tree):
        self.file_path = file_path
        self.segments = segments
        self.xml_tree = xml_tree

##############################################################################
# MAIN WINDOW
##############################################################################
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Static Maxlen Setter")
        self.resize(1000, 600)

        self.current_theme = detect_system_theme()
        self.apply_stylesheet(self.current_theme)
        self.theme_timer = QTimer(self)
        self.theme_timer.timeout.connect(self.check_system_theme)
        self.theme_timer.start(2000)

        # Main layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)

        # LEFT PANEL: file list + controls
        left_panel = QVBoxLayout()
        main_layout.addLayout(left_panel, stretch=1)

        file_controls = QHBoxLayout()
        self.browse_button = QPushButton("Browse Folder")
        self.browse_button.clicked.connect(self.browse_folder)
        file_controls.addWidget(self.browse_button)

        self.remove_button = QPushButton("Remove Selected")
        self.remove_button.clicked.connect(self.remove_selected_files)
        file_controls.addWidget(self.remove_button)
        left_panel.addLayout(file_controls)

        self.file_list_widget = FileListWidget(self)
        self.file_list_widget.itemClicked.connect(self.on_file_selected)
        left_panel.addWidget(self.file_list_widget)

        # RIGHT PANEL
        right_panel = QVBoxLayout()
        main_layout.addLayout(right_panel, stretch=3)

        top_controls = QHBoxLayout()
        self.btn_select_all = QPushButton("Select All")
        self.btn_select_all.setFixedWidth(80)
        self.btn_select_all.clicked.connect(self.select_all_segments)
        top_controls.addWidget(self.btn_select_all)

        self.btn_clear_all = QPushButton("Clear All")
        self.btn_clear_all.setFixedWidth(80)
        self.btn_clear_all.clicked.connect(self.clear_all_segments)
        top_controls.addWidget(self.btn_clear_all)

        self.character_limit_input = QLineEdit()
        self.character_limit_input.setPlaceholderText("Max")
        self.character_limit_input.setFixedWidth(50)
        self.character_limit_input.setMaxLength(3)
        top_controls.addWidget(self.character_limit_input)

        self.apply_limit_button = QPushButton("Apply Limit")
        self.apply_limit_button.setFixedWidth(80)
        self.apply_limit_button.clicked.connect(self.apply_limit)
        top_controls.addWidget(self.apply_limit_button)

        self.save_button = QPushButton("Save")
        self.save_button.setFixedWidth(60)
        self.save_button.clicked.connect(self.save_files)
        top_controls.addWidget(self.save_button)
        right_panel.addLayout(top_controls)

        # Fixed header row
        header_widget = QWidget()
        header_layout = QHBoxLayout(header_widget)
        header_layout.setContentsMargins(2, 2, 2, 2)

        lbl_sel = QLabel("Select")
        lbl_sel.setFixedWidth(60)
        lbl_source = QLabel("Source")
        lbl_source.setAlignment(Qt.AlignCenter)

        lbl_max = QLabel("MaxLen")
        lbl_max.setFixedWidth(60)
        lbl_max.setAlignment(Qt.AlignCenter)

        lbl_id = QLabel("ID")
        lbl_id.setFixedWidth(150)
        lbl_id.setAlignment(Qt.AlignCenter)

        header_layout.addWidget(lbl_sel)
        header_layout.addWidget(lbl_source)
        header_layout.addWidget(lbl_max)
        header_layout.addWidget(lbl_id)
        right_panel.addWidget(header_widget)

        # Scroll area for segments
        self.segment_scroll = QScrollArea()
        self.segment_scroll.setWidgetResizable(True)
        right_panel.addWidget(self.segment_scroll)

        self.segment_container = QWidget()
        self.segment_layout = QGridLayout(self.segment_container)
        self.segment_layout.setColumnStretch(0, 0)
        self.segment_layout.setColumnStretch(1, 1)
        self.segment_layout.setColumnStretch(2, 0)
        self.segment_layout.setColumnStretch(3, 0)
        self.segment_scroll.setWidget(self.segment_container)

        self.loaded_files = []
        self.current_file_data = None

    ############################################################################
    # THEME METHODS (Visual appearance remains as in your original script)
    ############################################################################
    def apply_stylesheet(self, theme):
        if theme == "dark":
            dark_style = """
                QWidget { background-color: #2b2b2b; color: #ccc; font-family: 'Segoe UI Variable'; }
                QMainWindow { background-color: #2b2b2b; }
                QLineEdit, QTextBrowser, QProgressBar, QScrollArea, QListWidget {
                    background-color: #444; border: 1px solid #555; border-radius: 4px; color: #ccc;
                }
                QPushButton {
                    background-color: #3a3a3a; border: 1px solid #555; border-radius: 4px; padding: 4px 8px; color: #ccc;
                }
                QPushButton:hover { background-color: #505050; }
                QFrame { border: none; }
                QToolTip { background-color: #333333; color: #ffffff; border: none; }
                QScrollBar:vertical { background: transparent; width: 8px; }
                QScrollBar::handle:vertical { background: #666; border-radius: 4px; min-height: 20px; }
                QScrollBar::handle:vertical:hover { background: #888; }
                QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px; background: none; }
                QScrollBar:horizontal { background: transparent; height: 8px; }
                QScrollBar::handle:horizontal { background: #666; border-radius: 4px; min-width: 20px; }
                QScrollBar::handle:horizontal:hover { background: #888; }
                QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal { width: 0px; background: none; }
            """
            self.setStyleSheet(dark_style)
            pal = QPalette()
            pal.setColor(QPalette.Window, QColor("#2b2b2b"))
            pal.setColor(QPalette.WindowText, QColor("#ccc"))
            self.setPalette(pal)
        else:
            light_style = """
                QWidget { background-color: #f3f3f3; color: #333; font-family: 'Segoe UI Variable'; }
                QMainWindow { background-color: #f3f3f3; }
                QLineEdit, QTextBrowser, QProgressBar, QScrollArea, QListWidget {
                    background-color: #fff; border: 1px solid #ccc; border-radius: 4px; color: #333;
                }
                QPushButton { background-color: #e1e1e1; border: none; border-radius: 4px; padding: 4px 8px; color: #333; }
                QPushButton:hover { background-color: #d7d7d7; }
                QFrame { border: none; }
                QToolTip { background-color: #ffffff; color: #333333; border: 1px solid #cccccc; }
                QScrollBar:vertical { background: transparent; width: 8px; }
                QScrollBar::handle:vertical { background: #bbb; border-radius: 4px; min-height: 20px; }
                QScrollBar::handle:vertical:hover { background: #999; }
                QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px; background: none; }
                QScrollBar:horizontal { background: transparent; height: 8px; }
                QScrollBar::handle:horizontal { background: #bbb; border-radius: 4px; min-width: 20px; }
                QScrollBar::handle:horizontal:hover { background: #999; }
                QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal { width: 0px; background: none; }
            """
            self.setStyleSheet(light_style)
            pal = QPalette()
            pal.setColor(QPalette.Window, QColor("#f3f3f3"))
            pal.setColor(QPalette.WindowText, QColor("#333"))
            self.setPalette(pal)

    def check_system_theme(self):
        new_theme = detect_system_theme()
        if new_theme != self.current_theme:
            self.current_theme = new_theme
            self.apply_stylesheet(self.current_theme)

    ############################################################################
    # FILE PANEL METHODS
    ############################################################################
    def browse_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder", os.getcwd())
        if not folder:
            return
        self.file_list_widget.clear()
        self.loaded_files.clear()
        self.current_file_data = None
        self.clear_segment_display()

        loading_item = QListWidgetItem("Loading...")
        self.file_list_widget.addItem(loading_item)
        QApplication.processEvents()

        exts = (".xlf", ".xliff", ".tsxf", ".tsxlf", ".ts")
        try:
            for root, _, files in os.walk(folder):
                for fname in files:
                    _, ext = os.path.splitext(fname)
                    if ext.lower() in exts:
                        fpath = os.path.join(root, fname)
                        try:
                            tfd = self.parse_translation_file(fpath)
                            if tfd and tfd.segments:
                                self.loaded_files.append(tfd)
                        except Exception:
                            pass
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error reading folder:\n{str(e)}\n{traceback.format_exc()}")

        self.file_list_widget.clear()
        if not self.loaded_files:
            QMessageBox.information(self, "No files found", "No valid translation files found.")
            return
        for fd in self.loaded_files:
            item = QListWidgetItem(os.path.basename(fd.file_path))
            item.setToolTip(fd.file_path)
            self.file_list_widget.addItem(item)

    def handleDroppedFiles(self, files):
        for f in files:
            tfd = self.parse_translation_file(f)
            if tfd and tfd.segments:
                self.loaded_files.append(tfd)
                item = QListWidgetItem(os.path.basename(f))
                item.setToolTip(f)
                self.file_list_widget.addItem(item)

    def remove_selected_files(self):
        items = self.file_list_widget.selectedItems()
        if not items:
            return
        for it in items:
            path = it.toolTip()
            self.loaded_files = [fd for fd in self.loaded_files if fd.file_path != path]
            self.file_list_widget.takeItem(self.file_list_widget.row(it))
        if self.current_file_data and self.current_file_data.file_path not in [fd.file_path for fd in self.loaded_files]:
            self.current_file_data = None
            self.clear_segment_display()

    ############################################################################
    # PARSE & RAW EXTRACTION
    ############################################################################
    def parse_translation_file(self, file_path):
        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            raw_content = f.read()

        tree = ET.parse(file_path)
        root = tree.getroot()
        remove_all_namespaces(root)

        segments = []
        trans_units = root.findall(".//trans-unit")
        if not trans_units:
            msgs = root.findall(".//message")
            if not msgs:
                return None
            for msg in msgs:
                mid = msg.get("id", "")
                maxw = msg.get("maxwidth", "")
                snippet = self.get_parent_snippet(raw_content, msg, "message")
                raw_src = self.extract_raw_tag(snippet, "source") or ""
                seg = SegmentData(mid, raw_src, msg, current_maxlen=maxw)
                segments.append(seg)
            return TranslationFileData(file_path, segments, tree)

        for tu in trans_units:
            tid = tu.get("id", "")
            maxw = tu.get("maxwidth", "")
            snippet = self.get_parent_snippet(raw_content, tu, "trans-unit")
            raw_src = self.extract_raw_tag(snippet, "source")
            if not raw_src.strip():
                raw_src = self.extract_raw_tag(snippet, "seg-source") or ""
            seg = SegmentData(tid, raw_src, tu, current_maxlen=maxw)
            segments.append(seg)

        if not segments:
            return None
        return TranslationFileData(file_path, segments, tree)

    def get_parent_snippet(self, raw_text, elem, parent_tagname):
        pid = elem.get("id", "")
        if not pid:
            return ""
        pat_start = f"<{parent_tagname}[^>]*id=[\"']{re.escape(pid)}[\"']"
        match_start = re.search(pat_start, raw_text, flags=re.IGNORECASE|re.DOTALL)
        if not match_start:
            return ""
        start_idx = match_start.start()
        pat_end = f"</{parent_tagname}>"
        match_end = re.search(pat_end, raw_text[start_idx:], flags=re.IGNORECASE|re.DOTALL)
        if not match_end:
            return ""
        end_idx = start_idx + match_end.end()
        return raw_text[start_idx:end_idx]

    def extract_raw_tag(self, snippet, tagname):
        pat = f"<{tagname}[^>]*>(.*?)</{tagname}>"
        m = re.search(pat, snippet, flags=re.IGNORECASE|re.DOTALL)
        if not m:
            return ""
        return m.group(0).strip()

    ############################################################################
    # FILE SELECTION
    ############################################################################
    def on_file_selected(self, item):
        name = item.text()
        for fd in self.loaded_files:
            if os.path.basename(fd.file_path) == name:
                self.current_file_data = fd
                break
        self.show_segments()

    ############################################################################
    # SHOW SEGMENTS (STRIP ALL TAGS BEFORE DISPLAY)
    ############################################################################
    def show_segments(self):
        self.clear_segment_display()
        if not self.current_file_data:
            return

        for row_idx, seg in enumerate(self.current_file_data.segments):
            chk = QCheckBox()
            seg.check_box = chk

            raw = seg.raw_text
            # Strip all tags (including <bpt>, <ept>, <ph>, etc.)
            plain_text = strip_tags(raw)

            lbl_text = QLabel(plain_text)
            lbl_text.setWordWrap(True)
            lbl_text.setTextFormat(Qt.PlainText)
            lbl_text.setStyleSheet("font-size:14pt;")
            lbl_text.setTextInteractionFlags(Qt.TextSelectableByMouse)

            lbl_max = QLabel(seg.current_maxlen)
            lbl_max.setFixedWidth(60)
            lbl_max.setAlignment(Qt.AlignCenter)
            seg.maxlen_label = lbl_max

            lbl_id = QLabel(seg.id)
            lbl_id.setFixedWidth(150)
            lbl_id.setAlignment(Qt.AlignCenter)
            lbl_id.setStyleSheet("font-size:12pt;")
            lbl_id.setTextInteractionFlags(Qt.TextSelectableByMouse)

            self.segment_layout.addWidget(chk, row_idx, 0, Qt.AlignCenter)
            self.segment_layout.addWidget(lbl_text, row_idx, 1)
            self.segment_layout.addWidget(lbl_max, row_idx, 2, Qt.AlignCenter)
            self.segment_layout.addWidget(lbl_id, row_idx, 3, Qt.AlignCenter)

            self.apply_alternate_color(row_idx, lbl_text)

        spacer = QFrame()
        spacer.setFrameShape(QFrame.NoFrame)
        self.segment_layout.addWidget(spacer, len(self.current_file_data.segments), 0, 1, 4)

    def clear_segment_display(self):
        while self.segment_layout.count():
            it = self.segment_layout.takeAt(0)
            if it:
                w = it.widget()
                if w:
                    w.deleteLater()

    def apply_alternate_color(self, row_idx, widget):
        is_dark = (self.current_theme == "dark")
        even_bg = "#333333" if is_dark else "#eeeeee"
        odd_bg  = "#2b2b2b" if is_dark else "#ffffff"
        bg = even_bg if row_idx % 2 == 0 else odd_bg
        widget.setStyleSheet(f"background-color:{bg};font-size:14pt;")

    ############################################################################
    # SELECT ALL / CLEAR ALL BUTTONS
    ############################################################################
    def select_all_segments(self):
        if not self.current_file_data:
            return
        for seg in self.current_file_data.segments:
            if seg.check_box:
                seg.check_box.setChecked(True)

    def clear_all_segments(self):
        if not self.current_file_data:
            return
        for seg in self.current_file_data.segments:
            if seg.check_box:
                seg.check_box.setChecked(False)

    ############################################################################
    # APPLY LIMIT & MERGE MRK TAGS
    ############################################################################
    def apply_limit(self):
        if not self.current_file_data:
            QMessageBox.warning(self, "No File Selected", "Please select a file first.")
            return
        txt = self.character_limit_input.text().strip()
        if not txt.isdigit() or int(txt) <= 0:
            QMessageBox.warning(self, "Invalid Input", "Please enter a positive integer (1-999).")
            return
        limit_val = int(txt)
        selected_units = set()
        for seg in self.current_file_data.segments:
            if seg.check_box and seg.check_box.isChecked():
                selected_units.add(seg.xml_element)
        if not selected_units:
            QMessageBox.warning(self, "No Segments Selected", "Please select at least one segment.")
            return

        for tu_elem in selected_units:
            tu_elem.set("maxwidth", str(limit_val))
            tu_elem.set("size-unit", "char")
            seg_source = tu_elem.find("seg-source")
            if seg_source is not None:
                mrks = seg_source.findall(".//mrk")
                if len(mrks) > 1:
                    merged = []
                    for m in mrks:
                        # Use get_inner_xml to get content without outer <mrk> tags
                        inn = get_inner_xml(m).strip()
                        if inn:
                            merged.append(inn)
                    joined = " ".join(merged)
                    for m in mrks:
                        seg_source.remove(m)
                    new_str = f'<mrk mtype="seg" mid="0">{joined}</mrk>'
                    try:
                        new_m = ET.fromstring(new_str)
                        seg_source.append(new_m)
                    except Exception:
                        fb = ET.SubElement(seg_source, "mrk")
                        fb.set("mtype", "seg")
                        fb.set("mid", "0")
                        fb.text = joined

        for seg in self.current_file_data.segments:
            if seg.xml_element in selected_units:
                seg.current_maxlen = str(limit_val)
                if seg.maxlen_label:
                    seg.maxlen_label.setText(str(limit_val))
        QMessageBox.information(self, "Limit Applied",
            f"Applied character limit of {limit_val} to {len(selected_units)} trans-unit(s).")

    ############################################################################
    # SAVE FILES
    ############################################################################
    def save_files(self):
        if not self.current_file_data:
            QMessageBox.warning(self, "No File Selected", "Please select a file to save.")
            return
        try:
            self.current_file_data.xml_tree.write(
                self.current_file_data.file_path,
                encoding="utf-8",
                xml_declaration=True
            )
            QMessageBox.information(self, "Save Successful",
                f"Changes saved to {self.current_file_data.file_path}.")
        except Exception as e:
            QMessageBox.critical(self, "Save Error",
                f"Failed to save file:\n{str(e)}\n\n{traceback.format_exc()}")

    ############################################################################
    # MAIN
    ############################################################################
    def main(self):
        pass

##############################################################################
# HELPER FUNCTION: GET INNER XML
##############################################################################
def get_inner_xml(elem):
    parts = []
    if elem.text:
        parts.append(elem.text)
    for child in elem:
        parts.append(ET.tostring(child, encoding="unicode", method="xml"))
        if child.tail:
            parts.append(child.tail)
    return "".join(parts)

##############################################################################
# MAIN FUNCTION
##############################################################################
def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
