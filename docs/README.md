# Optimisasi Holt-Winter dengan Algoritma Genetika untuk Prediksi Jumlah Penumpang di Bandara Soekarno-Hatta

Proyek ini bertujuan untuk melakukan optimisasi pada model peramalan Holt-Winter dengan menggunakan algoritma genetika dalam rangka memprediksi jumlah penumpang pesawat di Bandara Soekarno-Hatta. Algoritma genetika digunakan untuk mengoptimalkan parameter model Holt-Winter, yang dapat meningkatkan akurasi prediksi.

## Fitur Utama

- Optimasi parameter model Holt-Winter menggunakan Algoritma Genetika
- Prediksi jumlah penumpang pesawat di Bandara Soekarno-Hatta
- Penggunaan dataset riil untuk peramalan

## Instalasi

1. **Clone repositori ini:**

   ```bash
   git clone https://github.com/username/optimisasi-holt-winter-genetic-algorithm.git
   cd optimisasi-holt-winter-genetic-algorithm
   ```

2. **Buat environment Python baru:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Untuk Linux/MacOS
   venv\Scripts\activate     # Untuk Windows
   ```
3. **Instal dependensi yang diperlukan:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Langkah-langkah Pengolahan Data**

## Structure Project

```📂 ml-project/
┣━━ 📂 data/ → Raw and processed datasets
┃     ┣━━ 📂 raw/ → Unprocessed datasets
┃     ┣━━ 📂 processed/ → Cleaned and preprocessed datasets
┃     ┗━━ 📂 external/ → Third-party datasets

┣━━ 📂 notebooks/ → Jupyter notebooks for experiments
┃     ┣━━ 📄 01-data-exploration.ipynb
┃     ┣━━ 📄 02-feature-engineering.ipynb
┃     ┣━━ 📄 03-model-training.ipynb
┃     ┗━━ 📄 04-model-evaluation.ipynb

┣━━ 📂 src/ → Modular Python scripts
┃     ┣━━ 📂 data/ → Data handling
┃     ┃     ┣━━ 📄 load_data.py
┃     ┃     ┣━━ 📄 clean_data.py
┃     ┃     ┗━━ 📄 split_data.py
┃     ┣━━ 📂 features/ → Feature engineering
┃     ┃     ┗━━ 📄 feature_selection.py
┃     ┣━━ 📂 models/ → Model training and prediction
┃     ┃     ┣━━ 📄 train_model.py
┃     ┃     ┣━━ 📄 predict.py
┃     ┃     ┗━━ 📄 evaluate.py
┃     ┣━━ 📂 visualizations/ → Data visualization
┃     ┃     ┗━━ 📄 plot_results.py

┣━━ 📂 tests/ → Unit tests for scripts
┃     ┣━━ 📄 test_data.py
┃     ┣━━ 📄 test_models.py
┃     ┗━━ 📄 test_visualizations.py

┣━━ 📂 reports/ → Final analysis & results
┃     ┣━━ 📂 figures/ → Plots & charts
┃     ┗━━ 📄 report.md

┣━━ 📂 docs/ → Documentation & guides
┃     ┗━━ 📄 README.md

┣━━ 📄 requirements.txt → Dependencies
┣━━ 📄 .gitignore
┗━━ 📄 LICENSE
```
