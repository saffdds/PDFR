import sys
from pathlib import Path

from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QLabel,
    QMainWindow,
    QMessageBox,
    QToolBar,
)
from PySide6.QtPdf import QPdfDocument
from PySide6.QtPdfWidgets import QPdfView
from PySide6.QtGui import QIcon


class PdfViewer(QMainWindow):
    def __init__(self):
        super().__init__()

        cartella_script = Path(__file__).parent
        percorso_icona = cartella_script / "PDFR.ico"

        self.setWindowTitle("PDFR")
        self.setWindowIcon(QIcon(str(percorso_icona)))
        self.resize(1000, 700)

        self.documento = QPdfDocument(self)

        self.visualizzatore = QPdfView(self)
        self.visualizzatore.setDocument(self.documento)
        self.setCentralWidget(self.visualizzatore)

        barra = QToolBar("Strumenti PDF")
        self.addToolBar(barra)

        barra.addAction("Apri PDF", self.apri_pdf)
        barra.addSeparator()
        barra.addAction("Zoom −", lambda: self.cambia_zoom(0.8))
        barra.addAction("Zoom +", lambda: self.cambia_zoom(1.25))
        barra.addAction("Adatta larghezza", self.adatta_larghezza)

        self.stato = QLabel("Nessun PDF aperto")
        self.statusBar().addWidget(self.stato)

    def apri_pdf(self):
        percorso, _ = QFileDialog.getOpenFileName(
            self,
            "Apri PDF",
            str(Path.home()),
            "Documenti PDF (*.pdf)",
        )

        if not percorso:
            return

        errore = self.documento.load(percorso)
        if errore != QPdfDocument.Error.None_:
            QMessageBox.critical(
                self,
                "Errore",
                "Non è stato possibile aprire il PDF.",
            )
            return

        self.setWindowTitle(f"Visualizzatore PDF — {Path(percorso).name}")
        self.stato.setText(f"{self.documento.pageCount()} pagine")

    def cambia_zoom(self, fattore):
        nuovo_zoom = self.visualizzatore.zoomFactor() * fattore
        self.visualizzatore.setZoomFactor(nuovo_zoom)

    def adatta_larghezza(self):
        self.visualizzatore.setZoomMode(QPdfView.ZoomMode.FitToWidth)


app = QApplication(sys.argv)
finestra = PdfViewer()
finestra.show()
sys.exit(app.exec())
