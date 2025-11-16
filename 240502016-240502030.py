import random
import json
import math

# --- 1. Proje Sabitleri ve Kurulum ---

KELIME_VERITABANI = {
    "meyveler": ["elma", "armut", "muz", "kiraz", "cilek", "portakal"],
    "hayvanlar": ["kedi", "kopek", "aslan", "kaplan", "zurafa", "fil"],
    "teknoloji": ["bilgisayar", "klavye", "yazilim", "python", "algoritma"]
}

ADAM_DURUMLARI = [
    # İndeks 0 (can = 0) -> KAYBETTİN
    """
       +---+
       |   |
       O   |
      /|\\  |
      / \\  |
           |
    =========
    """,
    # İndeks 1 (can = 1)
    """
       +---+
       |   |
       O   |
      /|\\  |
      /    |
           |
    =========
    """,
    # İndeks 2 (can = 2)
    """
       +---+
       |   |
       O   |
      /|\\  |
           |
           |
    =========
    """,
    # İndeks 3 (can = 3)
    """
       +---+
       |   |
       O   |
      /|   |
           |
           |
    =========
    """,
    # İndeks 4 (can = 4)
    """
       +---+
       |   |
       O   |
       |   |
           |
           |
    =========
    """,
    # İndeks 5 (can = 5)
    """
       +---+
       |   |
       O   |
           |
           |
           |
    =========
    """,
    # İndeks 6 (can = 6) -> BAŞLANGIÇ
    """
       +---+
       |   |
           |
           |
           |
           |
    =========
    """
]

# --- 2. Yardımcı Fonksiyonlar ---

def kategori_ve_kelime_sec():
    """
    Kategorilerden rastgele birini ve o kategoriden rastgele bir kelime seçer.
    Returns:
        tuple: (secilen_kategori, secilen_kelime)
    """
    kategori = random.choice(list(KELIME_VERITABANI.keys()))
    kelime = random.choice(KELIME_VERITABANI[kategori])
    return kategori, kelime

def skorlari_getir():
    """
    scores.json dosyasını okur, yoksa boş bir liste döndürür.
    """
    try:
        with open("scores.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def skoru_kaydet(oyuncu_adi, son_puan):
    """
    Yeni skoru alır, mevcut skorlarla birleştirir, sıralar ve en iyi 5'i scores.json'a yazar.
    """
    skorlar = skorlari_getir()
    skorlar.append({"isim": oyuncu_adi, "puan": son_puan})
    sirali_skorlar = sorted(skorlar, key=lambda x: x["puan"], reverse=True)
    en_iyi_skorlar = sirali_skorlar[:5]
    
    with open("scores.json", "w") as f:
        json.dump(en_iyi_skorlar, f, indent=4)
    print("\n--- Yüksek Skorlar ---")
    for i, skor in enumerate(en_iyi_skorlar, 1):
        print(f"{i}. {skor['isim']}: {skor['puan']}")

# --- 3. Oyun Modülleri ---

def durumu_goster(oyun_durumu):
    """
    Mevcut oyun arayüzünü (ASCII, kelime, puanlar, menü) ekrana basar.
    """
    print("\n" + "="*40)
    print("=== Calc & Hang: İşlem Yap, Harfi Kurtar! ===")
    print("--- Yeni Tur ---")
    
    print(ADAM_DURUMLARI[oyun_durumu["can"]])
    
    print(f"\nKelime: {' '.join(oyun_durumu['maskeli_kelime'])}")
    print(f"Kategori İpucu: {'???' if not oyun_durumu['ipucu_kullanildi'] else oyun_durumu['kategori']}")
    print(f"Tahmin Edilen Harfler: {', '.join(oyun_durumu['tahminler'])}")
    print(f"Puan: {oyun_durumu['puan']} | Bonus Puan: {oyun_durumu['bonus_puan']} | Kalan Can: {oyun_durumu['can']}")
    
    print("\nSeçenekler:")
    print("[H]arf tahmini  [M]atematik işlemi  [I]pucu al  [C]ıkış")

def harf_tahmini_yap(oyun_durumu):
    """
    Kullanıcıdan harf tahmini alır ve oyun durumunu günceller.
    Puanlama: Doğru +10, Yanlış -5 puan ve -1 can.
    """
    tahmin = input("Tahmininiz (tek harf): ").lower()

    if len(tahmin) != 1 or not tahmin.isalpha():
        print("Geçersiz giriş! Lütfen sadece bir harf girin.")
        return 
    
    if tahmin in oyun_durumu['tahminler']:
        print(f"'{tahmin}' harfini zaten tahmin ettiniz.")
        return

    oyun_durumu['tahminler'].append(tahmin)

    if tahmin in oyun_durumu['kelime']:
        print(f"Doğru tahmin! '{tahmin}' harfi kelimede var.")
        oyun_durumu['puan'] += 10
        yeni_maske = list(oyun_durumu['maskeli_kelime'])
        for i, harf in enumerate(oyun_durumu['kelime']):
            if harf == tahmin:
                yeni_maske[i] = tahmin
        oyun_durumu['maskeli_kelime'] = "".join(yeni_maske)
    else:
        print(f"Yanlış tahmin! '{tahmin}' harfi kelimede yok.")
        oyun_durumu['puan'] -= 5
        oyun_durumu['can'] -= 1

# GÜNCELLENDİ: Bu fonksiyon artık işlem seçme menüsü içeriyor.
def islem_cozme_yap(oyun_durumu):
    """
    Kullanıcıya işlem türünü sorar, rastgele bir matematik işlemi oluşturur, 
    kullanıcıdan cevap alır.
    Puanlama: Doğru +15 puan, +1 bonus, +1 rastgele harf. Yanlış -10 puan, -1 can.
    """
    print("\n--- İşlem Çözme ---")
    
    # 1. Adım: Kullanıcıdan işlem türünü seçmesini iste
    print("Hangi tür işlem yapmak istersiniz?")
    islem_secimi = input("[T]oplama, [C]ıkarma, [P]Çarpma, [B]ölme: ").upper()

    sayi1 = random.randint(1, 10)
    sayi2 = random.randint(1, 10)
    islem_str = ""
    dogru_sonuc = 0

    # 2. Adım: Seçime göre işlemi ve sonucu belirle
    if islem_secimi == 'T':
        dogru_sonuc = sayi1 + sayi2
        islem_str = f"{sayi1} + {sayi2}"
        
    elif islem_secimi == 'C':
        if sayi1 < sayi2:
            sayi1, sayi2 = sayi2, sayi1 # Sayıları yer değiştir (swap)
        dogru_sonuc = sayi1 - sayi2
        islem_str = f"{sayi1} - {sayi2}"
        
    elif islem_secimi == 'P':
        sayi1 = random.randint(1, 9)
        sayi2 = random.randint(1, 9)
        dogru_sonuc = sayi1 * sayi2
        islem_str = f"{sayi1} * {sayi2}"
        
    elif islem_secimi == 'B':
        # Kullanıcı dostu bölme: Sonuç tam sayı olacak şekilde ayarla
        sayi2 = random.randint(2, 5) 
        kat = random.randint(1, 5)   
        sayi1 = sayi2 * kat          
        dogru_sonuc = kat 
        islem_str = f"{sayi1} / {sayi2}"
    
    else:
        print("Geçersiz seçim. İşlem iptal edildi.")
        return # Fonksiyondan çık

    # 3. Adım: Soruyu sor ve cevabı kontrol et
    try:
        cevap_str = input(f"İşlem: {islem_str} = ? (Çıkmak için 'iptal' yazın): ")
        
        if cevap_str.lower() == 'iptal':
            print("İşlem iptal edildi.")
            return

        cevap = float(cevap_str) 

        if math.isclose(cevap, dogru_sonuc):
            print("Doğru cevap!")
            oyun_durumu['puan'] += 15
            oyun_durumu['bonus_puan'] += 1
            
            # TODO: Rastgele bir harf açma mantığını buraya ekle
            print("Bir bonus puan ve rastgele bir harf kazandınız!")
            # ... (harf açma kodu) ...
            
        else:
            print(f"Yanlış cevap! Doğru sonuç {dogru_sonuc} olacaktı.")
            oyun_durumu['puan'] -= 10
            oyun_durumu['can'] -= 1

    except ValueError:
        print("Geçersiz giriş. Lütfen bir sayı girin.")
        oyun_durumu['puan'] -= 10
        oyun_durumu['can'] -= 1

def ipucu_al(oyun_durumu):
    """
    Bonus puanı yeterliyse (en az 1) kategori ipucunu açar.
    Puanlama: -1 Bonus Puanı.
    """
    if oyun_durumu['bonus_puan'] >= 1:
        if not oyun_durumu['ipucu_kullanildi']:
            print(f"1 Bonus Puan harcandı. Kelimenin kategorisi: {oyun_durumu['kategori']}")
            oyun_durumu['bonus_puan'] -= 1
            oyun_durumu['ipucu_kullanildi'] = True
        else:
            print(f"İpucunu zaten kullandınız. Kategori: {oyun_durumu['kategori']}")
    else:
        print("İpucu almak için yeterli bonus puanınız yok (En az 1 gerekli).")

# --- 4. Ana Oyun Döngüsü ---

def ana_oyun():
    """
    Oyunun ana döngüsünü yöneten fonksiyon.
    """
    
    secilen_kategori, secilen_kelime = kategori_ve_kelime_sec()
    
    oyun_durumu = {
        "kelime": secilen_kelime,
        "kategori": secilen_kategori,
        "maskeli_kelime": "_" * len(secilen_kelime),
        "can": 6,
        "puan": 0,
        "bonus_puan": 0,
        "tahminler": [],
        "ipucu_kullanildi": False,
        "oyun_bitti": False
    }

    while not oyun_durumu['oyun_bitti']:
        durumu_goster(oyun_durumu)
        
        secim = input("Seçiminiz (H, M, I, C): ").upper()

        if secim == 'H':
            harf_tahmini_yap(oyun_durumu)
        elif secim == 'M':
            islem_cozme_yap(oyun_durumu)
        elif secim == 'I':
            ipucu_al(oyun_durumu)
        elif secim == 'C':
            print("Oyundan çıkılıyor...")
            oyun_durumu['oyun_bitti'] = True
        else:
            print("Geçersiz seçim. Lütfen menüden bir harf girin.")

        # --- Kazanma / Kaybetme Kontrolü ---
        
        if oyun_durumu['maskeli_kelime'] == oyun_durumu['kelime']:
            print(f"\n--- TEBRİKLER! KAZANDINIZ! ---")
            print(f"Doğru kelime: {oyun_durumu['kelime']}")
            oyun_durumu['puan'] += 50 
            oyun_durumu['oyun_bitti'] = True

        if oyun_durumu['can'] <= 0:
            if not oyun_durumu['oyun_bitti']: 
                print(ADAM_DURUMLARI[0]) 
                print(f"\n--- KAYBETTİNİZ! ---")
                print(f"Doğru kelime: {oyun_durumu['kelime']} olacaktı.")
                oyun_durumu['puan'] -= 20 
                oyun_durumu['oyun_bitti'] = True
    
    # --- Oyun Sonu ve Skor Kaydı ---
    print(f"\nOyun Bitti! Final Puanınız: {oyun_durumu['puan']}")
    
    oyuncu_adi = input("Skor tablosu için adınızı girin: ")
    if oyuncu_adi: 
        skoru_kaydet(oyuncu_adi, oyun_durumu['puan'])


# --- Oyunu Başlat ---
if __name__ == "__main__":
    ana_oyun()