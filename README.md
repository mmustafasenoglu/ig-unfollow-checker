# 🔍 IG Unfollow Checker

**Instagram'da seni geri takip etmeyenleri bul ve tek tıkla takipten çık!**

> 🛡️ %100 güvenli — tüm işlemler bilgisayarında çalışır, verilerin paylaşılır mı?

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-macOS%20%7C%20Windows%20%7C%20Linux-lightgrey)]()

---

## ✨ Özellikler

| Özellik | Açıklama |
|---------|----------|
| 🔐 **Cookie veya Şifre** | Tarayıcıdan cookie kopyala veya şifre ile giriş yap |
| 🛡️ **2FA Desteği** | İki faktörlü doğrulama kodunu gir |
| 📊 **Gelişmiş Liste** | Takip ettiğin ama seni geri takip etmeyenleri göster |
| 🚀 **Tek Tıkla Unfollow** | Her kişinin yanında "Takipten Çık" butonu |
| 📄 **TXT Dışa Aktar** | Listeyi dosyaya kaydet |
| 📱 **Sayfalama** | Uzun listelerde kolayca gezin |
| 🖥️ **Desktop GUI** | Tkinter ile güzel arayüz |

## 🚀 Hızlı Başlangıç

### Kurulum

```bash
git clone https://github.com/mmustafasenoglu/ig-unfollow-checker.git
cd ig-unfollow-checker
pip install -r requirements.txt
```

### Çalıştırma

```bash
python insta.py
```

## 📖 Kullanım

### Yöntem 1 — Cookie ile Giriş (Önerilen)

1. [instagram.com](https://www.instagram.com)'a giriş yap
2. Tarayıcıda DevTools'u aç (`Cmd+Option+I` / `Ctrl+Shift+I`)
3. **Network** sekmesine git
4. Herhangi bir Instagram isteğine sağ tıkla → **Copy as cURL**
5. Uygulamadaki "Tüm Cookie" alanına yapıştır

### Yöntem 2 — Şifre ile Giriş

Cookie alanını boş bırak, sadece şifreni gir. 2FA aktifse kodu gir.

## 📸 Ekran Görüntüsü

```
┌─────────────────────────────────────────┐
│  Instagram - Geri Takip Etmeyenler      │
│                                         │
│  Kullanıcı adı: [________________]      │
│  Tüm Cookie:    [________________]      │
│  Şifre:         [________________]      │
│                                         │
│  [🔍 Geri Takip Etmeyenleri Bul]       │
│                                         │
│  Takip ettiğin: 412 | Takipçin: 387    │
│  Seni geri takip etmeyenler: 58 kişi    │
│                                         │
│  1. @kullanici1          [Takipten Çık] │
│  2. @kullanici2          [Takipten Çık] │
│  3. @kullanici3          [Takipten Çık] │
│                                         │
│  << Önceki    Sayfa: 1/2    Sonraki >>  │
│                          [💾 Kaydet]    │
└─────────────────────────────────────────┘
```

## 🔒 Gizlilik ve Güvenlik

- ✅ Tüm istekler **sadece senin bilgisayarından** Instagram sunucularına gider
- ✅ Hiçbir veri üçüncü taraf sunucuya gönderilmez
- ✅ Cookie/sifren asla paylaşılmaz
- ⚠️ Cookie, şifren kadar hassastır — kimseyle paylaşma

## ⚠️ Sorumluluk Reddi

- Bu proje **Instagram/Meta ile bağlantılı değildir**
- Instagram'ın Hizmet Şartları'nı otomatik erişim **yasaklar**
- Hesabında geçici engelleme veya askıya alma yaşanabilir
- Günde 1'den fazla çalıştırma
- Çok fazla kişiyi hızlıca takipten çıkma → `Action Blocked` (24-48 saat)
- **Kendi hesabında, kendi sorumluluğunda kullan**

## 🛠️ Teknolojiler

- **Python 3.9+**
- **Tkinter** — Desktop GUI
- **Instaloader** — Instagram GraphQL API
- **Requests** — Instagram Private API

## 📁 Proje Yapısı

```
ig-unfollow-checker/
├── insta.py           # Ana uygulama (GUI + Instagram mantığı)
├── requirements.txt   # Python bağımlılıkları
├── README.md          # Bu dosya
└── .gitignore
```

## �katkıda Bulun

1. Fork'la
2. Branch oluştur (`git checkout -b feature/yen ozellik`)
3. Değişikliklerini ekle (`git commit -m 'Yeni özellik ekle'`)
4. Push et (`git push origin feature/yen ozellik`)
5. PR aç

## 📄 License

MIT — kullan, fork et, değiştir. Garanti yoktur.

---

**Popüler Instagram araçları:**
`#instagram` `#unfollow` `#python` `#tkinter` `#desktop-app` `#social-media` `#instagram-tools` `#follower-tracking` `#non-followers` `#privacy` `#open-source` `#cli` `#automation`
