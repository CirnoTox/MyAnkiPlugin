import html
import json
from pathlib import Path

from aqt import gui_hooks, mw
from aqt.qt import QAction, QDialog, QVBoxLayout, QLineEdit, QPushButton, QListWidget, QTextEdit, QLabel
from aqt.utils import showWarning
from aqt.webview import AnkiWebView
from .storage import Repository

window = None


class Library(QDialog):
    def __init__(self):
        super().__init__(mw)
        self.repo = Repository(mw.pm.profileFolder())
        self.topic = None
        self.pending = None
        self.setWindowTitle('Incremental Reading')
        self.resize(900, 750)
        layout = QVBoxLayout(self)
        self.search = QLineEdit()
        self.search.setPlaceholderText('Search title or text')
        layout.addWidget(self.search)
        button = QPushButton('Import Text')
        layout.addWidget(button)
        self.items = QListWidget()
        layout.addWidget(self.items)
        self.reader = AnkiWebView(parent=self)
        self.reader.set_bridge_command(self.bridge, self)
        layout.addWidget(self.reader, 3)
        self.search.textChanged.connect(self.refresh)
        button.clicked.connect(self.import_text)
        self.items.itemClicked.connect(self.open_item)
        self.refresh()

    def refresh(self):
        self.rows = self.repo.search(self.search.text())
        self.items.clear()
        self.items.addItems([r['title'] for r in self.rows])

    def import_text(self):
        dialog = QDialog(self)
        dialog.setWindowTitle('Import plain text')
        layout = QVBoxLayout(dialog)
        fields = [QLineEdit(), QTextEdit(), QLineEdit()]
        for name, field in zip(['Title', 'Text', 'URL or citation (optional)'], fields):
            layout.addWidget(QLabel(name))
            layout.addWidget(field)
        save = QPushButton('Import')
        layout.addWidget(save)
        def commit():
            try:
                self.repo.add(fields[0].text(), fields[1].toPlainText(), fields[2].text())
                self.refresh()
                dialog.accept()
            except Exception as error:
                showWarning(str(error), parent=dialog)
        save.clicked.connect(commit)
        dialog.exec()

    def persist(self):
        if self.pending:
            self.repo.save(*self.pending)
            self.pending = None

    def open_item(self, item):
        try:
            self.persist()
            row = self.rows[self.items.row(item)]
            self.topic = row['id']
            self.repo.opened(self.topic)
            body = ''.join('<p>' + html.escape(p) + '</p>' for p in row['content'].split('\n'))
            script = (Path(__file__).parent / 'web' / 'reader.js').read_text()
            self.reader.setHtml('<meta charset="utf-8"><style>body{font:18px sans-serif;padding:24px}p{white-space:pre-wrap;min-height:1em}</style><h1>' + html.escape(row['title']) + '</h1><small>' + html.escape(row['citation']) + '</small><main>' + body + '</main><script>const topic=' + json.dumps(self.topic) + ';const saved=' + row['position'] + ';' + script + '</script>')
        except Exception as error:
            showWarning('Could not open/save reading: ' + str(error), parent=self)

    def bridge(self, message):
        try:
            data = json.loads(message)
            if set(data) != {'topic', 'position'} or data['topic'] != self.topic:
                return
            self.pending = (self.topic, data['position'])
            self.persist()
        except Exception as error:
            showWarning('Reading position could not be saved: ' + str(error), parent=self)

    def closeEvent(self, event):
        global window
        try:
            self.persist()
        except Exception as error:
            showWarning(str(error), parent=self)
            event.ignore()
            return
        self.reader.cleanup()
        self.repo.close()
        window = None
        event.accept()


def open_library():
    global window
    try:
        if window is None:
            window = Library()
        window.show()
        window.raise_()
    except Exception as error:
        showWarning(str(error))


def close_library():
    if window is not None:
        window.close()


menu = mw.form.menuTools.addMenu('Incremental Reading')
action = QAction('Reading Library', mw)
action.triggered.connect(open_library)
menu.addAction(action)
gui_hooks.profile_will_close.append(close_library)
