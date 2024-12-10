import tkinter as tk
from tkinter import messagebox
import tensorflow as tf
from tensorflow.keras.models import load_model
import numpy as np
import csv
from datetime import datetime

# Memuat model yang sudah dilatih
model = load_model('my_model.h5')

# Pemetaan hasil prediksi ke label kelas sesuai urutan yang diinginkan
class_mapping = {0: 'Normal', 1: 'Bipolar Type-1', 2: 'Bipolar Type-2', 3: 'Depression'}

# Mapping untuk fitur sesuai dengan pengkodean yang telah Anda tentukan
rentang_mapping = {
    '1 From 10': 0,
    '2 From 10': 1,
    '3 From 10': 2,
    '4 From 10': 3,
    '5 From 10': 4,
    '6 From 10': 5,
    '7 From 10': 6,
    '8 From 10': 7,
    '9 From 10': 8
}

usually_mapping = {
    'Seldom': 0,
    'Sometimes': 1,
    'Usually': 2,
    'Most-Often': 3
}

yes_no_mapping = {
    'YES': 1,
    'NO': 0
}

# Fungsi untuk memproses input dan prediksi dari model dan menyimpan jawaban ke CSV
def predict():
    try:
        # Mengumpulkan jawaban dari setiap pertanyaan
        answers = []
        for idx, var in enumerate(answer_vars):
            answer = var.get()  # Mengambil jawaban untuk setiap pertanyaan
            if idx in rentang_idx:  # Rentang nilai 1-10
                answers.append(rentang_mapping.get(answer, -1))  # Menggunakan rentang_mapping
            elif idx in usually_idx:  # Jawaban untuk Seldom, Sometimes, Usually, Most-Often
                answers.append(usually_mapping.get(answer, -1))  # Menggunakan usually_mapping
            elif idx in yes_no_idx:  # Jawaban YES/NO
                answers.append(yes_no_mapping.get(answer, -1))  # Menggunakan yes_no_mapping
            else:
                answers.append(answer)  # Jika tidak sesuai kategori di atas, simpan seperti adanya
                
        # Menambahkan timestamp untuk mencatat waktu pengisian survey
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        answers.append(timestamp)

        # Mengonversi jawaban ke dalam bentuk array atau vektor yang sesuai dengan input model
        input_vector = np.array(answers[:-1]).reshape(1, -1)  # Menggunakan semua jawaban kecuali timestamp

        # Melakukan prediksi menggunakan model
        prediction = model.predict(input_vector)

        # Menentukan kelas dengan probabilitas tertinggi
        predicted_class_idx = np.argmax(prediction)  # Index kelas dengan probabilitas tertinggi
        predicted_class = class_mapping[predicted_class_idx]  # Mendapatkan nama kelas berdasarkan index
        
        # Menampilkan hasil prediksi
        messagebox.showinfo("Hasil Prediksi", f"Prediksi hasil survey: {predicted_class}")
        
        # Menyimpan jawaban dan hasil prediksi ke CSV
        save_to_csv(answers, predicted_class)
        
    except Exception as e:
        messagebox.showerror("Error", f"Terjadi kesalahan: {str(e)}")

# Fungsi untuk menyimpan jawaban dan hasil prediksi ke file CSV
def save_to_csv(data, prediction):
    file_name = 'survey_answers.csv'
    
    # Menentukan header jika file CSV kosong atau tidak ada
    header = ['Sadness', 'Euphoric', 'Exhausted', 'Sleep dissorder', 'Mood Swing', 'Suicidal thoughts', 
              'Anorexia', 'Authority Respect', 'Try-Explanation', 'Aggressive Response', 'Ignore & Move-On', 'Nervous Break-down', 
              'Admit Mistakes', 'Overthinking', 'Concentration', 'Optimism', 'Timestamp', 'Result']
    
    # Menambahkan hasil prediksi ke data sebelum disimpan
    data.append(prediction)
    
    # Jika file CSV belum ada, buat file dengan header
    try:
        with open(file_name, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            
            # Jika file kosong, tulis header
            if file.tell() == 0:
                writer.writerow(header)
            
            # Tulis data jawaban dan hasil prediksi ke file CSV
            writer.writerow(data)
    except Exception as e:
        messagebox.showerror("Error", f"Terjadi kesalahan saat menyimpan data ke CSV: {str(e)}")

# Membuat jendela utama aplikasi menggunakan Tkinter
window = tk.Tk()
window.title("Program Survey Pilihan Ganda")

# Membuat canvas untuk mendukung scroll
canvas = tk.Canvas(window)
scrollbar = tk.Scrollbar(window, orient="vertical", command=canvas.yview)
frame = tk.Frame(canvas)

# Menghubungkan canvas dengan scrollbar
canvas.configure(yscrollcommand=scrollbar.set)

# Menempatkan frame dalam canvas
canvas.create_window((0, 0), window=frame, anchor="nw")

# Menempatkan scrollbar di sisi kanan
scrollbar.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)

# List pertanyaan
questions = [
    "Sadness?",
    "Euphoric?",
    "Exhausted?",
    "Sleep dissorder?",
    "Mood Swing?",
    "Suicidal thoughts?",
    "Anorexia?",
    "Authority Respect?",
    "Try-Explanation?",
    "Aggressive Response?",
    "Ignore & Move-On?",
    "Nervous Break-down?",
    "Admit Mistakes?",
    "Overthinking?",
    "Concentration?",
    "Optimism?"
]

# Pilihan untuk pertanyaan pilihan ganda
options_1_4 = ['Seldom', 'Sometimes', 'Usually', 'Most-Often']
options_5_14 = ['YES', 'NO']
options_15_16 = ['1 From 10', '2 From 10', '3 From 10', '4 From 10', '5 From 10', '6 From 10', '7 From 10', '8 From 10', '9 From 10']

# Variabel untuk menyimpan pilihan jawaban
answer_vars = []

# Indeks untuk pertanyaan rentang nilai (1-10), usually (Seldom, Sometimes, etc), yes/no
rentang_idx = [14, 15]  # Indeks 'Concentration' dan 'Optimism'
usually_idx = [0, 1, 2, 3]  # Indeks 'Sadness', 'Euphoric', 'Exhausted', 'Sleep dissorder'
yes_no_idx = [4, 5, 6, 7, 8, 9, 10, 11, 12, 13]  # Indeks 'Mood Swing', 'Suicidal thoughts', 'Anorexia', ...

# Membuat form untuk menampilkan pertanyaan dan pilihan
for idx, question in enumerate(questions):
    frame_question = tk.Frame(frame)
    frame_question.pack(fill='x', padx=10, pady=5)
    
    # Label untuk pertanyaan
    label = tk.Label(frame_question, text=question)
    label.pack(anchor="w")
    
    # Variabel untuk pilihan
    var = tk.StringVar()
    answer_vars.append(var)
    
    # Pilihan untuk pertanyaan 1-4 (4 opsi)
    if idx in usually_idx:
        for option in options_1_4:
            radio_button = tk.Radiobutton(frame_question, text=option, variable=var, value=option)
            radio_button.pack(anchor="w")
    
    # Pilihan untuk pertanyaan 5-13 (2 opsi)
    elif idx in yes_no_idx:
        for option in options_5_14:
            radio_button = tk.Radiobutton(frame_question, text=option, variable=var, value=option)
            radio_button.pack(anchor="w")
    
    # Pilihan untuk pertanyaan 14-16 (9 opsi)
    elif idx in rentang_idx:
        for option in options_15_16:
            radio_button = tk.Radiobutton(frame_question, text=option, variable=var, value=option)
            radio_button.pack(anchor="w")

# Tombol untuk melakukan prediksi
button_predict = tk.Button(frame, text="Prediksi", command=predict)
button_predict.pack(pady=20)

# Meng-update scrollregion canvas setelah menambahkan elemen
frame.update_idletasks()
canvas.config(scrollregion=canvas.bbox("all"))

# Menjalankan aplikasi Tkinter
window.mainloop()
