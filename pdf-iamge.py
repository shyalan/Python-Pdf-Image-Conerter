import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QFileDialog, QLabel, QWidget
from PyQt5.QtGui import QPixmap
import fitz  # PyMuPDF
from PIL import Image
from io import BytesIO

class PDFConverterApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PDF to Image Converter")
        self.setGeometry(100, 100, 600, 400)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        self.label = QLabel("No PDF selected.")
        self.layout.addWidget(self.label)

        self.select_button = QPushButton("Select PDF File")
        self.select_button.clicked.connect(self.select_pdf_file)
        self.layout.addWidget(self.select_button)

        self.convert_button = QPushButton("Convert to Images")
        self.convert_button.clicked.connect(self.convert_to_images)
        self.layout.addWidget(self.convert_button)

        self.central_widget.setLayout(self.layout)

        self.pdf_path = ""

    def select_pdf_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        pdf_file, _ = QFileDialog.getOpenFileName(self, "Select PDF File", "", "PDF Files (*.pdf);;All Files (*)", options=options)

        if pdf_file:
            self.pdf_path = pdf_file
            self.label.setText(f"Selected PDF: {self.pdf_path}")

    def convert_to_images(self):
        if not self.pdf_path:
            self.label.setText("Please select a PDF file first.")
            return

        pdf_document = fitz.open(self.pdf_path)

        for page_number in range(pdf_document.page_count):
            page = pdf_document[page_number]
            image_bytes = page.get_pixmap().get_buffer()
            image = Image.open(BytesIO(image_bytes))
            
            # Save the image (you can customize the file name and format)
            image.save(f"page_{page_number + 1}.png")

        pdf_document.close()
        self.label.setText("Conversion completed. Images saved.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PDFConverterApp()
    window.show()
    sys.exit(app.exec_())
