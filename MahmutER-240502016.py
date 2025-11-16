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
    gelişigüzel bir şekilde belirtilen kategoriler arasından
    birini ve o seçilen kategoriden bir kelime çeker
    """
    kategori = random.choice(list(KELIME_VERITABANI.keys()))
    kelime = random.choice(KELIME_VERITABANI[kategori])
    return kategori, kelime


def skorlari_getir():
    """
    skor dosyası okuma
    """
    try:
        with open("scores.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def skoru_kaydet(oyuncu_adi, son_puan):
    """
    en son kullanan oyuncunun puanını liste içindekiler ile birlikte sıralar ve en iyi 5 puanı yazdırır
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


def rastgele_harf_ac(oyun_durumu):
    """
    Kelimedeki kapalı harflerden rastgele birini açar.
    """
    # Açılmayan harflerin indekslerini bul
    acilacak_harfler = []
    for i, harf in enumerate(oyun_durumu['kelime']):
        if oyun_durumu['maskeli_kelime'][i] == '_':
            acilacak_harfler.append((i, harf))

    if acilacak_harfler:
        # Rastgele bir tane seç
        index, harf = random.choice(acilacak_harfler)
        # Maskeli kelimeyi güncelle
        yeni_maske = list(oyun_durumu['maskeli_kelime'])
        yeni_maske[index] = harf
        oyun_durumu['maskeli_kelime'] = "".join(yeni_maske)
        # Tahmin edilen harfler listesine ekle (eğer yoksa)
        if harf not in oyun_durumu['tahminler']:
            oyun_durumu['tahminler'].append(harf)
        print(f"Bonus: '{harf}' harfi açıldı!")
    else:
        print("Tüm harfler zaten açık!")


def sayi_al(mesaj):
    """
    Kullanıcıdan geçerli bir sayı alır
    """
    while True:
        try:
            sayi = float(input(mesaj))
            return sayi
        except ValueError:
            print("Geçersiz giriş! Lütfen bir sayı girin.")


# --- 3. Oyun Modülleri ---

def durumu_goster(oyun_durumu):
    """
    Oyun arayüzü ekrana bastırılır
    """
    print("\n" + "=" * 40)
    print("=== Calc & Hang: İşlem Yap, Harfi Kurtar! ===")
    print("--- Yeni Tur ---")

    print(ADAM_DURUMLARI[oyun_durumu["can"]])

    print(f"\nKelime: {' '.join(oyun_durumu['maskeli_kelime'])}")
    # Kategori ipucu sadece kullanıldıysa göster
    if oyun_durumu['ipucu_kullanildi']:
        print(f"Kategori: {oyun_durumu['kategori']}")
    else:
        print(f"Kategori: ???")
    print(f"Tahmin Edilen Harfler: {', '.join(oyun_durumu['tahminler'])}")
    print(f"Puan: {oyun_durumu['puan']} | Bonus Puan: {oyun_durumu['bonus_puan']} | Kalan Can: {oyun_durumu['can']}")

    print("\nSeçenekler:")
    print("[H]arf tahmini  [İ]şlem çöz  [I]pucu al  [C]ıkış")


def harf_tahmini_yap(oyun_durumu):
    """
    Harf tahmini alır ve yeni durumu ekrana yazar
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


def islem_cozme_yap(oyun_durumu):
    """
    Kullanıcıya hangi işlemi seçtiği sorulur. ve ona göre rastgele bir işlem verir
    Puanlama: Doğru +15 puan, +1 bonus, +1 rastgele harf. Yanlış -10 puan, -1 can.
    """
    print("\n--- İşlem Çözme ---")

    # Kullanılabilecek işlemleri belirle (daha önce kullanılmamış olanlar)
    kullanilabilir_islemler = []
    if 'T' not in oyun_durumu['kullanilan_islemler']:
        kullanilabilir_islemler.append('T')
    if 'C' not in oyun_durumu['kullanilan_islemler']:
        kullanilabilir_islemler.append('C')
    if 'P' not in oyun_durumu['kullanilan_islemler']:
        kullanilabilir_islemler.append('P')
    if 'B' not in oyun_durumu['kullanilan_islemler']:
        kullanilabilir_islemler.append('B')

    if not kullanilabilir_islemler:
        print("Tüm işlem türlerini kullandınız. Başka işlem kalmadı.")
        return

    print("Hangi tür işlem yapmak istersiniz?")
    # Kullanılabilir işlemleri göster
    secenekler = []
    if 'T' in kullanilabilir_islemler:
        secenekler.append("[T]oplama")
    if 'C' in kullanilabilir_islemler:
        secenekler.append("[C]ıkarma")
    if 'P' in kullanilabilir_islemler:
        secenekler.append("[P]Çarpma")
    if 'B' in kullanilabilir_islemler:
        secenekler.append("[B]ölme")
    print(", ".join(secenekler))

    islem_secimi = input("Seçiminiz: ").upper()

    if islem_secimi not in kullanilabilir_islemler:
        print("Geçersiz seçim veya bu işlem türünü zaten kullandınız. İşlem iptal edildi.")
        return

    # İşlem seçimini kullanılan işlemlere ekle (sıfıra bölme durumunda da kullanılmış sayılacak)
    oyun_durumu['kullanilan_islemler'].append(islem_secimi)

    # Kullanıcıdan sayıları al
    print("\nLütfen iki sayı girin:")
    sayi1 = sayi_al("1. sayı: ")
    sayi2 = sayi_al("2. sayı: ")

    islem_str = ""
    dogru_sonuc = 0

    # Sıfıra bölme kontrolü
    if islem_secimi == 'B' and sayi2 == 0:
        print("Hata: Bölen 0 olamaz! Hata sayısı artırıldı.")
        oyun_durumu['puan'] -= 10
        oyun_durumu['can'] -= 1
        # İşlem zaten kullanılanlara eklendi, return ile çıkıyoruz
        return

    if islem_secimi == 'T':
        dogru_sonuc = sayi1 + sayi2
        islem_str = f"{sayi1} + {sayi2}"

    elif islem_secimi == 'C':
        dogru_sonuc = sayi1 - sayi2
        islem_str = f"{sayi1} - {sayi2}"

    elif islem_secimi == 'P':
        dogru_sonuc = sayi1 * sayi2
        islem_str = f"{sayi1} * {sayi2}"

    elif islem_secimi == 'B':
        dogru_sonuc = sayi1 / sayi2
        islem_str = f"{sayi1} / {sayi2}"

    try:
        cevap_str = input(f"İşlem: {islem_str} = ? (Çıkmak için 'iptal' yazın): ")

        if cevap_str.lower() == 'iptal':
            print("İşlem iptal edildi.")
            # İptal durumunda işlemi kullanılanlardan çıkar
            oyun_durumu['kullanilan_islemler'].remove(islem_secimi)
            return

        cevap = float(cevap_str)

        # Belirtilen toleransla karşılaştırma (abs_tol=1e-6)
        if math.isclose(cevap, dogru_sonuc, abs_tol=1e-6):
            print("Doğru cevap!")
            oyun_durumu['puan'] += 15
            oyun_durumu['bonus_puan'] += 1
            # Rastgele bir harf aç
            rastgele_harf_ac(oyun_durumu)

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
    bonus puanı yeterliyse kategori ipucunu açar
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
    menüler arası değişimi sağlayan fonksiyon
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
        "kullanilan_islemler": [],  # Her işlem türünün bir kere kullanılması için
        "oyun_bitti": False
    }

    while not oyun_durumu['oyun_bitti']:
        durumu_goster(oyun_durumu)

        secim = input("Seçiminiz (H, İ, I, C): ").upper()

        if secim == 'H':
            harf_tahmini_yap(oyun_durumu)
        elif secim == 'İ':
            islem_cozme_yap(oyun_durumu)
        elif secim == 'I':
            ipucu_al(oyun_durumu)
        elif secim == 'C':
            print("Oyundan çıkılıyor...")
            oyun_durumu['oyun_bitti'] = True
        else:
            print("Geçersiz seçim. Lütfen menüden bir harf girin.")

        # --- Kazanma / Kaybetme Kontrolü ---

        # if oyun_durumu['maskeli_kelime'] == oyun_durumu['kelime']: (Alternatif)
        if "_" not in oyun_durumu['maskeli_kelime']:
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