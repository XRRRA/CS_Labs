import sys
import string
from collections import Counter
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QTextEdit, QPushButton, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt
import matplotlib.pyplot as plt

# English letter frequencies
english_frequencies = {
    'a': 8.167, 'b': 1.492, 'c': 2.782, 'd': 4.253, 'e': 12.702,
    'f': 2.228, 'g': 2.015, 'h': 6.094, 'i': 6.966, 'j': 0.153,
    'k': 0.772, 'l': 4.025, 'm': 2.406, 'n': 6.749, 'o': 7.507,
    'p': 1.929, 'q': 0.095, 'r': 5.987, 's': 6.327, 't': 9.056,
    'u': 2.758, 'v': 0.978, 'w': 2.360, 'x': 0.150, 'y': 1.974,
    'z': 0.074
}


class MonoalphabeticCipherApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Monoalphabetic Cipher Decryption Tool")
        self.setGeometry(100, 100, 900, 700)

        # Set up layout
        self.central_widget = QWidget()
        self.layout = QVBoxLayout(self.central_widget)
        self.setCentralWidget(self.central_widget)

        # Encrypted Text Input
        self.input_label = QLabel("Input Encrypted Message:")
        self.layout.addWidget(self.input_label)

        self.input_text = QTextEdit()
        self.layout.addWidget(self.input_text)

        # Frequency Analysis Chart Button
        self.chart_label = QLabel("Frequency Analysis:")
        self.layout.addWidget(self.chart_label)

        self.show_chart_btn = QPushButton("Show Frequency Analysis")
        self.show_chart_btn.clicked.connect(self.show_frequency_analysis)
        self.layout.addWidget(self.show_chart_btn)

        # Frequency Analysis Table
        self.freq_table = QTableWidget(26, 4)
        self.freq_table.setHorizontalHeaderLabels(['Letter (Message)', 'Message Frequency (%)',
                                                   'Letter (English)', 'English Frequency (%)'])
        self.layout.addWidget(self.freq_table)

        # Letter Mappings Table
        self.mapping_label = QLabel("Substitution Letter Mappings:")
        self.layout.addWidget(self.mapping_label)

        self.mapping_table = QTableWidget(26, 2)
        self.mapping_table.setHorizontalHeaderLabels(['Encrypted Letter', 'Decrypted Letter'])
        for row, letter in enumerate(string.ascii_lowercase):
            self.mapping_table.setItem(row, 0, QTableWidgetItem(letter))
            self.mapping_table.setItem(row, 1, QTableWidgetItem(""))
        self.mapping_table.itemChanged.connect(self.update_decryption)
        self.layout.addWidget(self.mapping_table)

        # Result Display
        self.result_label = QLabel("Decrypted Message Preview:")
        self.layout.addWidget(self.result_label)

        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        self.layout.addWidget(self.result_text)

    def show_frequency_analysis(self):
        # Get encrypted message
        encrypted_message = self.input_text.toPlainText().lower()

        # Frequency analysis on encrypted message
        letter_counts = Counter(char for char in encrypted_message if char in string.ascii_lowercase)
        total_letters = sum(letter_counts.values())
        encrypted_frequencies = {letter: (count / total_letters) * 100 for letter, count in letter_counts.items()}

        # Sort encrypted message frequencies from most to least frequent
        sorted_encrypted_freq = sorted(encrypted_frequencies.items(), key=lambda item: item[1], reverse=True)

        # Sort English frequencies from most to least frequent
        sorted_english_freq = sorted(english_frequencies.items(), key=lambda item: item[1], reverse=True)

        # Clear the frequency table before populating
        self.freq_table.clearContents()

        # Fill frequency table with sorted values
        for row in range(26):
            # Populate sorted message frequencies
            if row < len(sorted_encrypted_freq):
                enc_letter, enc_freq = sorted_encrypted_freq[row]
                self.freq_table.setItem(row, 0, QTableWidgetItem(enc_letter))
                self.freq_table.setItem(row, 1, QTableWidgetItem(f"{enc_freq:.3f}"))
            else:
                self.freq_table.setItem(row, 0, QTableWidgetItem(""))
                self.freq_table.setItem(row, 1, QTableWidgetItem(""))

            # Populate sorted English frequencies
            eng_letter, eng_freq = sorted_english_freq[row]
            self.freq_table.setItem(row, 2, QTableWidgetItem(eng_letter))
            self.freq_table.setItem(row, 3, QTableWidgetItem(f"{eng_freq:.3f}"))

        # Plotting frequencies (not affected by the sorting, just for visualization)
        fig, ax = plt.subplots()
        letters = list(string.ascii_lowercase)
        encrypted_values = [encrypted_frequencies.get(letter, 0) for letter in letters]
        english_values = [english_frequencies.get(letter, 0) for letter in letters]

        ax.bar(letters, encrypted_values, alpha=0.6, label="Encrypted Message Frequency")
        ax.bar(letters, english_values, alpha=0.6, label="English Frequency", color='orange')

        ax.set_ylabel('Frequency (%)')
        ax.set_title('Frequency Analysis')
        ax.legend()

        plt.show()

    def update_decryption(self):
        encrypted_message = self.input_text.toPlainText().lower()
        decrypted_message = list(encrypted_message)

        # Apply user-provided letter mappings
        for row in range(26):
            encrypted_letter_item = self.mapping_table.item(row, 0)
            decrypted_letter_item = self.mapping_table.item(row, 1)

            if decrypted_letter_item and decrypted_letter_item.text():
                enc_letter = encrypted_letter_item.text()
                dec_letter = decrypted_letter_item.text().lower()

                # Replace encrypted letter with decrypted letter (in uppercase for visibility)
                for i, char in enumerate(decrypted_message):
                    if char == enc_letter:
                        decrypted_message[i] = dec_letter.upper()

        self.result_text.setText("".join(decrypted_message))


# Run the application
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MonoalphabeticCipherApp()
    window.show()
    sys.exit(app.exec_())
