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

# Fungsi untuk memproses input dan prediksi dari model dan menyimpan jawaban ke CSV
def predict():
    try:
        # Mengumpulkan jawaban dari setiap pertanyaan
        answers = []
        for var in answer_vars:
            answers.append(var.get())  # Mengambil jawaban untuk setiap pertanyaan

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

# Menambahkan Canvas untuk scrolling
canvas = tk.Canvas(window)
scrollbar = tk.Scrollbar(window, orient="vertical", command=canvas.yview)
frame = tk.Frame(canvas)

# Menyambungkan scrollbar dengan canvas
canvas.configure(yscrollcommand=scrollbar.set)

# Menempatkan frame di dalam canvas
canvas.create_window((0, 0), window=frame, anchor="nw")
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

# Membuat form untuk menampilkan pertanyaan dan pilihan
for idx, question in enumerate(questions):
    frame_question = tk.Frame(frame)
    frame_question.pack(fill='x', padx=10, pady=5)
    
    # Label untuk pertanyaan
    label = tk.Label(frame_question, text=question)
    label.pack(anchor="w")
    
    # Variabel untuk pilihan
    var = tk.IntVar()
    answer_vars.append(var)
    
    # Pilihan untuk pertanyaan 1-4 (4 opsi)
    if idx < 4:
        for i, option in enumerate(options_1_4, 1):
            radio_button = tk.Radiobutton(frame_question, text=option, variable=var, value=i)
            radio_button.pack(anchor="w")
    
    # Pilihan untuk pertanyaan 5-13 (2 opsi)
    elif 4 <= idx < 14:
        for i, option in enumerate(options_5_14, 1):
            radio_button = tk.Radiobutton(frame_question, text=option, variable=var, value=i)
            radio_button.pack(anchor="w")
    
    # Pilihan untuk pertanyaan 15-16 (9 opsi)
    else:
        for i, option in enumerate(options_15_16, 1):
            radio_button = tk.Radiobutton(frame_question, text=option, variable=var, value=i)
            radio_button.pack(anchor="w")

# Fungsi untuk memperbarui scroll region setiap kali pertanyaan baru ditambahkan
def update_scroll_region():
    frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

# Tombol untuk melakukan prediksi
button_predict = tk.Button(frame, text="Prediksi", command=predict)
button_predict.pack(pady=20)

# Memperbarui scroll region untuk memastikan scrolling berfungsi
window.after(100, update_scroll_region)

# Menjalankan aplikasi Tkinter
window.mainloop()
