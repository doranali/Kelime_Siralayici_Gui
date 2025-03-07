# Kelime_Siralayici_Gui
Kelime Sıralayıcı, GTK tabanlı bir Python uygulamasıdır. Kullanıcıların bir metin dosyasına kelime ekleyip düzenlemesine, silmesine ve alfabetik olarak sıralamasına olanak tanır.

# Kelime Sıralayıcı

Bu proje, Gtk arayüzü ile kelimeleri bir dosyaya kaydeden, sıralayan ve düzenlemeye imkan tanıyan bir uygulamadır.

## Özellikler
- Kullanıcıdan kelime ekleme
- Dosyadan kelime yükleme
- Eklenen kelimeleri alfabetik olarak sıralama
- Kelime düzenleme ve silme
- Gtk arayüzü ile kullanıcı dostu tasarım
- İlk çalıştırmada depo dosyalarının otomatik oluşturulması

## Gereksinimler
Bu uygulamayı çalıştırmak için aşağıdaki bağımlılıkların yüklü olması gerekmektedir:

```sh
sudo apt update
sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-3.0
```

## Kurulum
1. Depoyu klonlayın:
   ```sh
   git clone https://github.com/kullanici_adiniz/kelime_siralayici.git
   cd kelime_siralayici
   ```
2. Gerekli bağımlılıkları yükleyin (yukarıdaki komutları takip edin).
3. Uygulamayı çalıştırın:
   ```sh
   python3 kelime_siralayici.py
   ```

## Kullanım
- **Kelime Ekle:** Giriş kutusuna kelime yazıp "Kelime Ekle" butonuna basın.
- **Dosyadan Kelime Yükle:** "Dosya Seç" butonu ile bir `.txt` dosyası seçin.
- **Sıralamayı Güncelle:** "Sıralamayı Güncelle" butonu ile mevcut kelimeleri alfabetik olarak düzenleyin.
- **Kelime Düzenleme:** Mevcut kelimeyi ve yeni kelimeyi girerek "Kelimeyi Düzenle" butonuna basın.
- **Kelime Silme:** Silmek istediğiniz kelimeyi girerek "Kelimeyi Sil" butonuna basın.

---

Proje hakkında geri bildirimlerinizi paylaşabilirsiniz! 😊

