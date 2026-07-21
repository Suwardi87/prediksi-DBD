"""
Script untuk Visualisasi Pohon Keputusan Random Forest
=======================================================
Script ini membuat visualisasi pohon keputusan individual
dari Random Forest untuk memahami bagaimana model membuat prediksi
"""

import os
import pickle
import matplotlib.pyplot as plt
from sklearn.tree import plot_tree, export_text
import numpy as np

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'app', 'models', 'random_forest_model.pkl')

def visualisasi_pohon_keputusan(tree_index=0, max_depth=3):
    """
    Visualisasi satu pohon keputusan dari Random Forest
    
    Args:
        tree_index: Index pohon yang mau divisualisasi (0 sampai n_estimators-1)
        max_depth: Kedalaman maksimum yang ditampilkan (agar tidak terlalu besar)
    """
    print("=" * 80)
    print(f"🌲 VISUALISASI POHON KEPUTUSAN #{tree_index}")
    print("=" * 80)
    
    # Load model
    if not os.path.exists(MODEL_PATH):
        print("\n❌ Model belum di-training!")
        print("💡 Silakan training model dulu dari web interface")
        return
    
    with open(MODEL_PATH, 'rb') as f:
        model_data = pickle.load(f)
    
    model = model_data['model']
    feature_columns = model_data['feature_columns']
    inverse_label_map = model_data['inverse_label_map']
    
    print(f"\n📊 Info Model:")
    print(f"   Jumlah pohon: {model.n_estimators}")
    print(f"   Fitur: {feature_columns}")
    print(f"   Target: {list(inverse_label_map.values())}")
    
    if tree_index >= model.n_estimators:
        print(f"\n❌ Tree index {tree_index} tidak valid!")
        print(f"💡 Gunakan index 0 sampai {model.n_estimators - 1}")
        return
    
    # Ambil satu pohon
    tree = model.estimators_[tree_index]
    
    # Plot pohon
    plt.figure(figsize=(20, 10))
    plot_tree(
        tree,
        feature_names=feature_columns,
        class_names=list(inverse_label_map.values()),
        filled=True,
        rounded=True,
        fontsize=10,
        max_depth=max_depth
    )
    
    output_path = os.path.join(os.path.dirname(__file__), f'decision_tree_{tree_index}.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"\n✅ Visualisasi disimpan ke: {output_path}")
    
    # Export text representation
    tree_text = export_text(tree, feature_names=feature_columns, max_depth=max_depth)
    print(f"\n📝 Struktur Pohon (Depth ≤ {max_depth}):")
    print(tree_text)
    
    # Feature importance untuk pohon ini
    print(f"\n📊 Feature Importance Pohon #{tree_index}:")
    importances = tree.feature_importances_
    for feature, importance in sorted(zip(feature_columns, importances), 
                                     key=lambda x: x[1], reverse=True):
        if importance > 0:
            print(f"   {feature}: {importance:.4f} ({importance*100:.2f}%)")

def visualisasi_feature_importance():
    """Visualisasi feature importance dari keseluruhan Random Forest"""
    print("\n" + "=" * 80)
    print("📊 FEATURE IMPORTANCE - KESELURUHAN MODEL")
    print("=" * 80)
    
    if not os.path.exists(MODEL_PATH):
        print("\n❌ Model belum di-training!")
        return
    
    with open(MODEL_PATH, 'rb') as f:
        model_data = pickle.load(f)
    
    model = model_data['model']
    feature_columns = model_data['feature_columns']
    
    # Get feature importance
    importances = model.feature_importances_
    indices = np.argsort(importances)[::-1]
    
    # Print ranking
    print("\n🏆 Ranking Feature (dari yang paling penting):")
    for i, idx in enumerate(indices, 1):
        feature = feature_columns[idx]
        importance = importances[idx]
        print(f"   {i}. {feature}: {importance:.4f} ({importance*100:.2f}%)")
    
    # Plot bar chart
    plt.figure(figsize=(10, 6))
    plt.bar(range(len(importances)), importances[indices], color='skyblue')
    plt.xticks(range(len(importances)), [feature_columns[i] for i in indices], rotation=45)
    plt.xlabel('Fitur')
    plt.ylabel('Importance')
    plt.title('Feature Importance - Random Forest Model')
    plt.tight_layout()
    
    output_path = os.path.join(os.path.dirname(__file__), 'feature_importance.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"\n✅ Chart disimpan ke: {output_path}")

def penjelasan_cara_baca_pohon():
    """Penjelasan cara membaca pohon keputusan"""
    print("\n" + "=" * 80)
    print("📖 CARA MEMBACA POHON KEPUTUSAN")
    print("=" * 80)
    
    print("""
🌳 STRUKTUR POHON:

    [Root Node]
       |
    [bulan <= 7.5]    ← Kondisi split
    /            \\
  True          False
   |              |
[jumlah_kasus <= 12.5]   [jumlah_kasus <= 16.5]
   /      \\                /       \\
Rendah  Sedang         Sedang    Tinggi


📝 CARA BACA:

1. ROOT NODE (Paling atas)
   - Node pertama yang menerima data
   - Fitur paling penting untuk split pertama
   - Contoh: "bulan <= 7.5"

2. INTERNAL NODE (Node tengah)
   - Keputusan berdasarkan kondisi
   - True → ke kiri
   - False → ke kanan
   - Contoh: "jumlah_kasus <= 12.5"

3. LEAF NODE (Paling bawah)
   - Prediksi akhir
   - Class: Rendah/Sedang/Tinggi
   - Value: [jumlah_rendah, jumlah_sedang, jumlah_tinggi]
   - Samples: berapa data yang sampai ke leaf ini

📊 INFO DI SETIAP NODE:

┌─────────────────────────┐
│ jumlah_kasus <= 12.5    │ ← Kondisi split
│ gini = 0.444            │ ← Impurity (0=pure, 0.5=mixed)
│ samples = 100           │ ← Jumlah data di node ini
│ value = [20, 50, 30]    │ ← [Rendah, Sedang, Tinggi]
│ class = Sedang          │ ← Prediksi mayoritas
└─────────────────────────┘

🎯 GINI IMPURITY:
- 0.0 = Pure (semua data satu kelas)
- 0.5 = Mixed (data tercampur rata)
- Semakin rendah semakin baik

📈 CONTOH INTERPRETASI:

Node: jumlah_kasus <= 12.5
├─ True (≤ 12.5)
│  └─ value = [40, 10, 0]  → Mayoritas Rendah
│     Artinya: Kalau kasus ≤ 12.5, biasanya risiko RENDAH
│
└─ False (> 12.5)
   └─ value = [5, 30, 65]  → Mayoritas Tinggi
      Artinya: Kalau kasus > 12.5, biasanya risiko TINGGI


🔍 PATH DECISION (Contoh):

Data: {bulan: 8, jumlah_kasus: 18, usia: 25, jenis_kelamin: 1, lama_rawat: 4}

Path:
1. bulan <= 7.5? → False (8 > 7.5) → Ke kanan
2. jumlah_kasus <= 16.5? → False (18 > 16.5) → Ke kanan
3. Sampai ke leaf: "Tinggi"

Prediksi: TINGGI ✅


💡 TIPS:

1. Pohon yang bagus:
   - Tidak terlalu dalam (max_depth 5-10)
   - Gini di leaf mendekati 0
   - Samples di leaf tidak terlalu sedikit

2. Overfitting jika:
   - Pohon terlalu dalam
   - Leaf punya samples sangat sedikit (1-2)
   - Perfect fit di training tapi jelek di testing

3. Random Forest = Gabungan banyak pohon
   - Setiap pohon vote
   - Mayoritas vote jadi prediksi final
   - Lebih robust dari single tree
""")

if __name__ == '__main__':
    print("\n")
    print("=" * 80)
    print("🌲 VISUALISASI RANDOM FOREST - SISTEM PREDIKSI DBD")
    print("=" * 80)
    
    # Penjelasan cara baca
    penjelasan_cara_baca_pohon()
    
    # Feature importance keseluruhan
    visualisasi_feature_importance()
    
    # Visualisasi 3 pohon pertama
    print("\n\n")
    for i in range(min(3, 10)):  # Visualisasi max 3 pohon
        try:
            visualisasi_pohon_keputusan(tree_index=i, max_depth=3)
            print("\n")
        except Exception as e:
            if i == 0:
                print(f"❌ Error: {e}")
            break
    
    print("\n" + "=" * 80)
    print("✅ VISUALISASI SELESAI!")
    print("=" * 80)
    print("\n📁 File yang dibuat:")
    print("   - decision_tree_0.png")
    print("   - decision_tree_1.png") 
    print("   - decision_tree_2.png")
    print("   - feature_importance.png")
    print("\n💡 Buka file .png untuk melihat visualisasi pohon")
