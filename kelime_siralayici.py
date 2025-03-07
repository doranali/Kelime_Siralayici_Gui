import gi
import os

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

DEPO_FILE = "depo.txt"
SORTED_FILE = "sıralanmış.txt"

def ensure_files_exist():
    """Depo ve sıralanmış dosyalarının mevcut olup olmadığını kontrol eder, yoksa oluşturur."""
    if not os.path.exists(DEPO_FILE):
        with open(DEPO_FILE, "w", encoding="utf-8") as f:
            pass  # Boş dosya oluştur
    if not os.path.exists(SORTED_FILE):
        with open(SORTED_FILE, "w", encoding="utf-8") as f:
            pass  # Boş dosya oluştur

class WordSorterApp(Gtk.Window):
    def __init__(self):
        super().__init__(title="Kelime Sıralayıcı")
        self.set_border_width(10)
        self.set_default_size(400, 500)
        
        ensure_files_exist()  # Dosyaların varlığını kontrol et ve oluştur
        
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(vbox)

        # Dosya Seç Butonu
        self.file_button = Gtk.Button(label="Dosya Seç")
        self.file_button.connect("clicked", self.on_file_select)
        vbox.pack_start(self.file_button, False, False, 0)
        
        # Kelime Ekleme Alanı
        self.entry = Gtk.Entry()
        vbox.pack_start(self.entry, False, False, 0)
        
        self.add_button = Gtk.Button(label="Kelime Ekle")
        self.add_button.connect("clicked", self.on_add_word)
        vbox.pack_start(self.add_button, False, False, 0)
        
        # Senkronizasyon Butonu
        self.sync_button = Gtk.Button(label="Sıralamayı Güncelle")
        self.sync_button.connect("clicked", self.sync_sorted_file)
        vbox.pack_start(self.sync_button, False, False, 0)
        
        # Kaydırılabilir Liste Görüntüleme
        self.scrolled_window = Gtk.ScrolledWindow()
        self.scrolled_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        vbox.pack_start(self.scrolled_window, True, True, 0)

        self.word_list = Gtk.TextView()
        self.word_list.set_editable(False)
        self.word_list.set_wrap_mode(Gtk.WrapMode.WORD)
        self.scrolled_window.add(self.word_list)
        
        # Kelime Düzenleme Alanı
        self.old_word_entry = Gtk.Entry()
        self.old_word_entry.set_placeholder_text("Düzenlenecek kelime")
        vbox.pack_start(self.old_word_entry, False, False, 0)
        
        self.new_word_entry = Gtk.Entry()
        self.new_word_entry.set_placeholder_text("Yeni kelime")
        vbox.pack_start(self.new_word_entry, False, False, 0)
        
        self.edit_button = Gtk.Button(label="Kelimeyi Düzenle")
        self.edit_button.connect("clicked", self.on_edit_word)
        vbox.pack_start(self.edit_button, False, False, 0)
        
        self.delete_button = Gtk.Button(label="Kelimeyi Sil")
        self.delete_button.connect("clicked", self.on_delete_word)
        vbox.pack_start(self.delete_button, False, False, 0)

        self.load_sorted_words()

    def on_file_select(self, widget):
        dialog = Gtk.FileChooserDialog(
            title="Kelime Dosyasını Seç", parent=self,
            action=Gtk.FileChooserAction.OPEN,
            buttons=(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK)
        )
        
        filter_text = Gtk.FileFilter()
        filter_text.set_name("Text files")
        filter_text.add_pattern("*.txt")
        dialog.add_filter(filter_text)
        
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.add_words_from_file(dialog.get_filename())
        
        dialog.destroy()

    def add_words_from_file(self, filename):
        with open(filename, "r", encoding="utf-8") as f:
            new_words = set(word.strip() for word in f.readlines() if word.strip())
        
        existing_words = self.get_existing_words()
        unique_words = new_words - existing_words
        
        if unique_words:
            with open(DEPO_FILE, "a", encoding="utf-8") as f:
                for word in unique_words:
                    f.write(word + "\n")
        
        self.sync_sorted_file()

    def on_add_word(self, widget):
        new_word = self.entry.get_text().strip()
        if new_word and new_word.lower() not in self.get_existing_words():
            with open(DEPO_FILE, "a", encoding="utf-8") as f:
                f.write(new_word + "\n")
            self.entry.set_text("")
            self.sync_sorted_file()

    def on_edit_word(self, widget):
        old_word = self.old_word_entry.get_text().strip()
        new_word = self.new_word_entry.get_text().strip()
        existing_words = self.get_existing_words()
        
        if old_word.lower() in existing_words and new_word:
            existing_words.remove(old_word.lower())
            existing_words.add(new_word.lower())
            
            with open(DEPO_FILE, "w", encoding="utf-8") as f:
                for word in sorted(existing_words, key=str.lower):
                    f.write(word + "\n")
            self.sync_sorted_file()
            self.old_word_entry.set_text("")
            self.new_word_entry.set_text("")

    def on_delete_word(self, widget):
        word_to_delete = self.old_word_entry.get_text().strip()
        existing_words = self.get_existing_words()
        
        if word_to_delete.lower() in existing_words:
            existing_words.remove(word_to_delete.lower())
            
            with open(DEPO_FILE, "w", encoding="utf-8") as f:
                for word in sorted(existing_words, key=str.lower):
                    f.write(word + "\n")
            self.sync_sorted_file()
            self.old_word_entry.set_text("")

    def sync_sorted_file(self, widget=None):
        existing_words = self.get_existing_words()
        sorted_words = sorted(existing_words, key=str.lower)
        
        with open(SORTED_FILE, "w", encoding="utf-8") as f:
            for word in sorted_words:
                f.write(word + "\n")
        
        self.load_sorted_words()

    def load_sorted_words(self):
        if os.path.exists(SORTED_FILE):
            with open(SORTED_FILE, "r", encoding="utf-8") as f:
                content = f.read()
        else:
            content = ""
        
        buffer = self.word_list.get_buffer()
        buffer.set_text(content)

    def get_existing_words(self):
        if os.path.exists(DEPO_FILE):
            with open(DEPO_FILE, "r", encoding="utf-8") as f:
                return set(word.strip().lower() for word in f.readlines() if word.strip())
        return set()

if __name__ == "__main__":
    app = WordSorterApp()
    app.connect("destroy", Gtk.main_quit)
    app.show_all()
    Gtk.main()
