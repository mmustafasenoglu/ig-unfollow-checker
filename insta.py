"""
Instagram'da seni geri takip etmeyenleri bulan ARAYÜZLÜ (GUI) script.
Takipten çıkma özellikli yeni versiyon.

KURULUM (bir kere yapman yeterli):
    pip install instaloader requests

ÇALIŞTIRMA:
    python insta.py
"""

import threading
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog, scrolledtext
import instaloader
import urllib.parse
import http.cookies
import requests
import time
import re
import math

class TakipUygulamasi:
    def __init__(self, kok):
        self.kok = kok
        kok.title("Instagram - Geri Takip Etmeyenler")
        kok.geometry("540x680")
        kok.resizable(False, False)

        self.sonuc_listesi = []
        self.takip_ettigim = 0
        self.takipcim = 0
        self.mevcut_sayfa = 1
        self.sayfa_boyutu = 30
        
        self.headers = {}
        self.cookie_degeri = ""

        cerceve = ttk.Frame(kok, padding=15)
        cerceve.pack(fill="x")

        ttk.Label(cerceve, text="Kullanıcı adı:").grid(row=0, column=0, sticky="w", pady=4)
        self.kullanici_adi_girisi = ttk.Entry(cerceve, width=38)
        self.kullanici_adi_girisi.grid(row=0, column=1, pady=4, sticky="w")

        # Cookie alanı (Zorunlu yöntem)
        ttk.Label(cerceve, text="Tüm Cookie:").grid(row=1, column=0, sticky="w", pady=4)
        self.cookie_girisi = ttk.Entry(cerceve, width=38, show="*")
        self.cookie_girisi.grid(row=1, column=1, pady=4, sticky="w")

        session_aciklama = ttk.Label(
            cerceve,
            text="↑ Safari Ağ sekmesinde 'graphql' isteğine SAĞ TIKLA -> 'cURL Olarak Kopyala'\ndeyip buraya VEYA sadece Cookie değerini yapıştır.",
            foreground="#555",
            font=("Helvetica", 10),
        )
        session_aciklama.grid(row=2, column=0, columnspan=2, sticky="w", pady=(0, 6))

        ayrac = ttk.Separator(cerceve, orient="horizontal")
        ayrac.grid(row=3, column=0, columnspan=2, sticky="ew", pady=6)

        ttk.Label(cerceve, text="— VEYA şifre ile giriş —", foreground="#888").grid(
            row=4, column=0, columnspan=2, pady=(0, 4)
        )

        ttk.Label(cerceve, text="Şifre:").grid(row=5, column=0, sticky="w", pady=4)
        self.sifre_girisi = ttk.Entry(cerceve, width=38, show="*")
        self.sifre_girisi.grid(row=5, column=1, pady=4, sticky="w")

        self.baslat_butonu = ttk.Button(
            cerceve, text="Geri Takip Etmeyenleri Bul", command=self.basla
        )
        self.baslat_butonu.grid(row=6, column=0, columnspan=2, pady=12)

        self.durum_etiketi = ttk.Label(cerceve, text="Hazır.", foreground="gray")
        self.durum_etiketi.grid(row=7, column=0, columnspan=2, sticky="w")

        self.sonuc_cercevesi = ttk.Frame(kok, padding=(15, 0, 15, 15))
        self.sonuc_cercevesi.pack(fill="both", expand=True)

        self.liste_baslik = ttk.Label(self.sonuc_cercevesi, text="Sonuçlar:")
        self.liste_baslik.pack(anchor="w")
        
        # Liste için Canvas ve Scrollbar (Takipten Çık butonları için)
        liste_kapsayici = ttk.Frame(self.sonuc_cercevesi)
        liste_kapsayici.pack(fill="both", expand=True, pady=5)
        
        self.canvas = tk.Canvas(liste_kapsayici, borderwidth=0, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(liste_kapsayici, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Sayfalama kontrolleri
        sayfalama_cercevesi = ttk.Frame(self.sonuc_cercevesi)
        sayfalama_cercevesi.pack(fill="x", pady=5)
        
        self.onceki_butonu = ttk.Button(sayfalama_cercevesi, text="<< Önceki", command=self.onceki_sayfa, state="disabled", width=10)
        self.onceki_butonu.pack(side="left")
        
        self.sayfa_etiketi = ttk.Label(sayfalama_cercevesi, text="Sayfa: 0 / 0", width=15, anchor="center")
        self.sayfa_etiketi.pack(side="left", expand=True)
        
        self.sonraki_butonu = ttk.Button(sayfalama_cercevesi, text="Sonraki >>", command=self.sonraki_sayfa, state="disabled", width=10)
        self.sonraki_butonu.pack(side="right")

        self.kaydet_butonu = ttk.Button(
            self.sonuc_cercevesi, text="Tüm Sonucu .txt olarak kaydet", command=self.kaydet, state="disabled"
        )
        self.kaydet_butonu.pack(anchor="e", pady=(10, 0))

    def durum_yaz(self, metin):
        self.durum_etiketi.config(text=metin)

    def iki_faktor_kodu_iste(self):
        return simpledialog.askstring(
            "2FA Kodu", "Telefonuna/mailine gelen doğrulama kodunu gir:"
        )

    def basla(self):
        kullanici_adi = self.kullanici_adi_girisi.get().strip()
        self.cookie_degeri = self.cookie_girisi.get().strip()
        sifre         = self.sifre_girisi.get()

        if not kullanici_adi:
            messagebox.showwarning("Eksik bilgi", "Kullanıcı adı boş olamaz.")
            return

        if not self.cookie_degeri and not sifre:
            messagebox.showwarning("Eksik bilgi", "Tüm Cookie değeri veya şifre girilmeli.")
            return

        self.baslat_butonu.config(state="disabled")
        self.kaydet_butonu.config(state="disabled")
        
        # Ekranı temizle
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
            
        self.durum_yaz("Giriş yapılıyor...")

        is_parcacigi = threading.Thread(
            target=self._calistir, args=(kullanici_adi, self.cookie_degeri, sifre), daemon=True
        )
        is_parcacigi.start()

    def _calistir(self, kullanici_adi, cookie_degeri, sifre):
        try:
            L = instaloader.Instaloader()
            
            L.context._session.headers.update({
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Safari/605.1.15",
                "X-IG-App-ID": "936619743392459",
            })
            
            giris_yapildi = False

            if cookie_degeri:
                try:
                    # Eğer kullanıcı tüm cURL komutunu yapıştırdıysa içinden Cookie'yi ayıkla
                    curl_match = re.search(r"-H\s+['\"]Cookie:\s*(.*?)['\"]", cookie_degeri, re.IGNORECASE)
                    if curl_match:
                        cookie_degeri = curl_match.group(1)
                        self.cookie_degeri = cookie_degeri # güncelle
                        
                    if cookie_degeri.lower().startswith("cookie:"):
                        cookie_degeri = cookie_degeri[7:].strip()
                        self.cookie_degeri = cookie_degeri
                        
                    cookie_obj = http.cookies.SimpleCookie()
                    cookie_obj.load(cookie_degeri)
                    
                    for key, morsel in cookie_obj.items():
                        L.context._session.cookies.set(key, morsel.value, domain=".instagram.com")
                    
                    if "csrftoken" in cookie_obj:
                        L.context._session.headers.update({"X-CSRFToken": cookie_obj["csrftoken"].value})
                    
                    L.context.username = kullanici_adi
                    
                    try:
                        self.kok.after(0, lambda: self.durum_yaz("Cookie test ediliyor..."))
                        test_profil = instaloader.Profile.from_username(L.context, kullanici_adi)
                        giris_yapildi = True
                        self.kok.after(0, lambda: self.durum_yaz("Cookie ile giriş başarılı!"))
                        try:
                            L.save_session_to_file(kullanici_adi)
                        except Exception:
                            pass
                    except Exception as e:
                        hata_detay = str(e)
                        self.kok.after(0, lambda m=hata_detay: self.durum_yaz(f"Cookie geçersiz ({m}), şifre deneniyor..."))
                except Exception as ex:
                    err = str(ex)
                    self.kok.after(0, lambda m=err: self.durum_yaz(f"Cookie hatası: {m}, şifre deneniyor..."))

            if not giris_yapildi:
                try:
                    L2 = instaloader.Instaloader()
                    L2.load_session_from_file(kullanici_adi)
                    L = L2
                    giris_yapildi = True
                    self.kok.after(0, lambda: self.durum_yaz("Kayıtlı oturum bulundu, kullanılıyor..."))
                except Exception:
                    pass

            if not giris_yapildi and sifre:
                try:
                    L.login(kullanici_adi, sifre)
                    giris_yapildi = True
                except instaloader.exceptions.TwoFactorAuthRequiredException:
                    kod_kutusu = {}

                    def kod_sor():
                        kod_kutusu["kod"] = self.iki_faktor_kodu_iste()

                    self.kok.after(0, kod_sor)
                    while "kod" not in kod_kutusu:
                        threading.Event().wait(0.1)

                    if not kod_kutusu["kod"]:
                        self.kok.after(0, lambda: self._hata("2FA kodu girilmedi, işlem durduruldu."))
                        return

                    L.two_factor_login(kod_kutusu["kod"])
                    giris_yapildi = True

                if giris_yapildi:
                    try:
                        L.save_session_to_file(kullanici_adi)
                        self.kok.after(0, lambda: self.durum_yaz("Oturum kaydedildi."))
                    except Exception:
                        pass

            if not giris_yapildi:
                self.kok.after(0, lambda: self._hata(
                    "Giriş yapılamadı.\n\n"
                    "Lütfen 'Tüm Cookie' değerini Safari'den kopyalayıp deneyin."
                ))
                return

            self.kok.after(0, lambda: self.durum_yaz("Kullanıcı ID'si bulunuyor..."))
            profil = instaloader.Profile.from_username(L.context, kullanici_adi)
            user_id = profil.userid

            # Fetch_users için headers oluştur (takipten çıkarken de lazım olacak)
            self.headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Safari/605.1.15",
                "X-IG-App-ID": "936619743392459",
                "Cookie": self.cookie_degeri,
            }
            csrf_match = re.search(r"csrftoken=([^;]+)", self.cookie_degeri)
            if csrf_match:
                self.headers["X-CSRFToken"] = csrf_match.group(1)
            
            def fetch_users(endpoint_type):
                # { "username": pk } şeklinde sözlük döneceğiz
                users_dict = {}
                max_id = ""
                
                while True:
                    url = f"https://www.instagram.com/api/v1/friendships/{user_id}/{endpoint_type}/?count=100"
                    if max_id:
                        url += f"&max_id={max_id}"
                        
                    res = requests.get(url, headers=self.headers)
                    if res.status_code != 200:
                        raise Exception(f"{endpoint_type} çekilirken hata: {res.status_code} - {res.text[:100]}")
                        
                    data = res.json()
                    for user in data.get("users", []):
                        users_dict[user["username"]] = user["pk"]
                        
                    max_id = data.get("next_max_id")
                    if not max_id:
                        break
                    time.sleep(1.5) # rate limit yememek için bekle
                    
                return users_dict

            self.kok.after(0, lambda: self.durum_yaz("Takipçi listesi alınıyor (Yeni API ile)..."))
            takipcilerim_dict = fetch_users("followers")

            self.kok.after(0, lambda: self.durum_yaz("Takip edilenler listesi alınıyor (Yeni API ile)..."))
            takip_ettiklerim_dict = fetch_users("following")

            takipcilerim_set = set(takipcilerim_dict.keys())
            takip_ettiklerim_set = set(takip_ettiklerim_dict.keys())

            geri_takip_etmeyenler_usernames = sorted(takip_ettiklerim_set - takipcilerim_set)
            
            self.sonuc_listesi = [{"username": u, "pk": takip_ettiklerim_dict[u]} for u in geri_takip_etmeyenler_usernames]
            
            self.takip_ettigim = len(takip_ettiklerim_set)
            self.takipcim = len(takipcilerim_set)
            
            self.kok.after(0, self._tamamlandi)

        except instaloader.exceptions.BadCredentialsException:
            self.kok.after(0, lambda: self._hata("Kullanıcı adı veya şifre hatalı."))
        except instaloader.exceptions.ConnectionException as e:
            hata_mesaji = f"Bağlantı hatası (Instagram engelleyebilir): {e}"
            self.kok.after(0, lambda m=hata_mesaji: self._hata(m))
        except Exception as e:
            hata_mesaji = f"Beklenmeyen hata: {e}"
            self.kok.after(0, lambda m=hata_mesaji: self._hata(m))

    def _tamamlandi(self):
        self.mevcut_sayfa = 1
        self.sayfayi_guncelle()
        self.durum_yaz("Tamamlandı.")
        self.baslat_butonu.config(state="normal")
        self.kaydet_butonu.config(state="normal" if self.sonuc_listesi else "disabled")

    def sayfayi_guncelle(self):
        toplam_kisi = len(self.sonuc_listesi)
        if toplam_kisi == 0:
            for widget in self.scrollable_frame.winfo_children():
                widget.destroy()
            ttk.Label(self.scrollable_frame, text="Seni geri takip etmeyen kimse yok! Harika.").pack(pady=10)
            self.sayfa_etiketi.config(text="Sayfa: 0 / 0")
            return

        toplam_sayfa = math.ceil(toplam_kisi / self.sayfa_boyutu)
        baslangic = (self.mevcut_sayfa - 1) * self.sayfa_boyutu
        bitis = min(baslangic + self.sayfa_boyutu, toplam_kisi)
        
        sayfa_icerigi = self.sonuc_listesi[baslangic:bitis]
        
        self.liste_baslik.config(text=(
            f"Takip ettiğin: {self.takip_ettigim} | Takipçin: {self.takipcim}\n"
            f"Seni geri takip etmeyenler: {toplam_kisi} kişi\n"
            f"Gösterilen: {baslangic + 1} - {bitis}"
        ))
        
        # Ekranı temizle
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
            
        # Kişileri listele ve butonları ekle
        for i, kisi in enumerate(sayfa_icerigi):
            satir = ttk.Frame(self.scrollable_frame)
            satir.pack(fill="x", pady=2, padx=5)
            
            lbl = ttk.Label(satir, text=f"{baslangic + i + 1}. {kisi['username']}", width=35)
            lbl.pack(side="left")
            
            btn = ttk.Button(satir, text="Takipten Çık", width=15)
            # lambda içine default argüman koyarak her butonun kendi değerini hatırlamasını sağlıyoruz
            btn.config(command=lambda k=kisi, b=btn: self.takipten_cik(k, b))
            btn.pack(side="right")
        
        # Scroll'u en başa al
        self.canvas.yview_moveto(0)
        
        self.sayfa_etiketi.config(text=f"Sayfa: {self.mevcut_sayfa} / {toplam_sayfa}")
        self.onceki_butonu.config(state="normal" if self.mevcut_sayfa > 1 else "disabled")
        self.sonraki_butonu.config(state="normal" if self.mevcut_sayfa < toplam_sayfa else "disabled")

    def takipten_cik(self, kisi, btn):
        btn.config(state="disabled", text="Bekleniyor...")
        
        def islem():
            try:
                pk = kisi["pk"]
                url = f"https://www.instagram.com/api/v1/friendships/destroy/{pk}/"
                res = requests.post(url, headers=self.headers)
                
                if res.status_code == 200:
                    data = res.json()
                    if data.get("status") == "ok":
                        self.kok.after(0, lambda: btn.config(text="Çıkıldı") if btn.winfo_exists() else None)
                        return
                
                # Eğer hata verdiyse butonu geri aç
                self.kok.after(0, lambda: btn.config(state="normal", text="Hata! Tekrar dene") if btn.winfo_exists() else None)
            except Exception as e:
                self.kok.after(0, lambda: btn.config(state="normal", text="Hata!") if btn.winfo_exists() else None)
                
        threading.Thread(target=islem, daemon=True).start()

    def onceki_sayfa(self):
        if self.mevcut_sayfa > 1:
            self.mevcut_sayfa -= 1
            self.sayfayi_guncelle()

    def sonraki_sayfa(self):
        toplam_sayfa = math.ceil(len(self.sonuc_listesi) / self.sayfa_boyutu)
        if self.mevcut_sayfa < toplam_sayfa:
            self.mevcut_sayfa += 1
            self.sayfayi_guncelle()

    def kaydet(self):
        if not self.sonuc_listesi:
            return
        dosya_yolu = filedialog.asksaveasfilename(
            defaultextension=".txt",
            initialfile="geri_takip_etmeyenler.txt",
            filetypes=[("Metin dosyası", "*.txt")],
        )
        if dosya_yolu:
            with open(dosya_yolu, "w", encoding="utf-8") as f:
                f.write("\n".join(k["username"] for k in self.sonuc_listesi))
            messagebox.showinfo("Kaydedildi", f"Liste kaydedildi:\n{dosya_yolu}")


if __name__ == "__main__":
    kok = tk.Tk()
    uygulama = TakipUygulamasi(kok)
    kok.mainloop()