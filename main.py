from PyQt5 import QtCore, QtGui, QtWidgets
from design import Ui_MainWindow  
import sys
import feedparser

class MyApp(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyApp, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Haber Radar")
        self.ui.treeWidget.itemClicked.connect(self.display_news)
        self.ui.textBrowser.setStyleSheet("""
            QTextBrowser {
                background-color: #f0f0f0;  /* Arka plan rengi */
                color: #333;                 /* Metin rengi */
                font-size: 12px;             /* Yazı boyutu */
                padding: 10px;               /* İç boşluk */
                border: 1px solid #aaa;      /* Kenar rengi */
                border-radius: 7px;          /* Kenar yuvarlama */
            }

            QTextBrowser a {
                color: #0066cc;              /* Bağlantı rengi */
                text-decoration: none;       /* Alt çizgi kaldır */
            }

            QTextBrowser a:hover {
                text-decoration: underline;   /* Alt çizgi ekle hover'da */
            }
        """)
        self.refresh_button = QtWidgets.QPushButton(self)
        self.refresh_button.setText("Yenile")
        self.refresh_button.setGeometry(QtCore.QRect(962, 8, 80, 30))  # Sağ üst köşeye yerleştirilir
        self.refresh_button.setStyleSheet("""
                QPushButton {
                    background-color: #4CAF50; /* Arka plan rengi */
                    color: white;              /* Metin rengi */
                    font-size: 14px;           /* Yazı boyutu */
                    padding: 10px 20px;        /* İç boşluk (yatay ve dikey) */
                    border: 2px solid #388E3C; /* Buton kenarlığı */
                    border-radius: 8px;        /* Kenar yuvarlama */
                }

                QPushButton:hover {
                    background-color: #45a049; /* Hover (üzerine gelince) rengi */
                }

                QPushButton:pressed {
                    background-color: #2e7d32; /* Tıklandığında rengi */
                }
            """)

        self.refresh_button.clicked.connect(self.refresh_news)  # Butona tıkla
        



        self.current_resource = None


    def refresh_news(self):
        if self.current_resource:  # Geçerli bir haber kaynağı varsa
            resource_info = self.fetch_news(self.current_resource)  # Güncel haberleri çek
            self.animate_text_browser(resource_info)  # Animasyonlu olarak güncelle


    def display_news(self, item):
        resource = item.text(0)  
        resource_info = self.fetch_news(resource)  #

        self.ui.textBrowser.clear()  #
        for news in resource_info:
            summary = news['summary']
            truncated_summary = summary[:100] + "..." if len(summary) > 100 else summary  # İlk 100 karakteri al
            

            self.ui.textBrowser.insertHtml(
                "<hr>"
                f"<h3 style='color: black;'>{news['title']}</h3>"  # Başlık boyutunu artır
                f"<a href='{news['link']}'>{news['link']}</a><br>"
                f"{truncated_summary}<br>"
                f"<b>Yayınlanma Tarihi: {news['published']}</b><br>"  # Koyu metin
                "<hr>" # Alt çizgi ekler
            )
        self.ui.textBrowser.verticalScrollBar().setValue(0)  
    def fetch_news(self, resource):
        urls = {
            "A HABER": "https://www.ahaber.com.tr/rss/galeri/anasayfa.xml",
            "CNN": "https://www.cnnturk.com/feed/rss/all/news",
            "YENİ AKİT": "https://www.yeniakit.com.tr/rss/haber/gundem",
            "NTV": "https://www.ntv.com.tr/gundem.rss",
            "ANA YURT": "https://anayurtgazetesi.com/rss.xml",
            "CUMHURİYET": "http://www.cumhuriyet.com.tr/rss/son_dakika.xml",
            "HÜRRİYET": "http://www.hurriyet.com.tr/rss/gundem",
            "MİLLİYET": "http://www.milliyet.com.tr/rss/rssNew/gundemRss.xml",
            "SABAH": "https://www.sabah.com.tr/rss/gundem.xml",
            "YENİ ŞAFAK": "https://www.yenisafak.com/Rss",
            "HABERTÜRK": "http://www.haberturk.com/rss",
            "TAKVİM": "https://www.takvim.com.tr/rss/anasayfa.xml",
            "TRT HABER": "http://www.trthaber.com/sondakika.rss",
            "MYNET": "https://www.mynet.com/haber/rss/sondakika",

            "A PARA":"https://www.ahaber.com.tr/rss/ekonomi.xml",
            "BBC TÜRKÇE": "https://feeds.bbci.co.uk/turkce/rss.xml",            
            "CNN EKONOMİ":"https://www.cnnturk.com/feed/rss/ekonomi/news",
            "HÜRRİYET EKONOMİ":"http://www.hurriyet.com.tr/rss/ekonomi",
            "MİLLİYET EKONOMİ":"http://www.milliyet.com.tr/rss/rssNew/ekonomiRss.xml",
            "SABAH EKONOMİ":" https://www.sabah.com.tr/rss/ekonomi.xml",
            "TAKVİM EKONOMİ":"https://www.takvim.com.tr/rss/ekonomi.xml",
            "YENİ AKİT EKONOMİ":"https://www.yeniakit.com.tr/rss/haber/ekonomi",
            "YENİ ŞAFAK EKONOMİ":"https://www.yenisafak.com/rss?xml=ekonomi",
            "NTV EKONOMİ":"https://www.ntv.com.tr/ekonomi.rss",

            "HÜRRİYET MAGAZİN":"http://www.hurriyet.com.tr/rss/magazin",
            "MİLLİYET MAGAZİN":"http://www.milliyet.com.tr/rss/rssNew/magazinRss.xml",
            "YENİ AKİT MAGAZİN":"https://www.yeniakit.com.tr/rss/haber/medya",
            "A MAGAZİN":"https://www.ahaber.com.tr/rss/magazin.xml",
            "CNN MAGAZİN":"https://www.cnnturk.com/feed/rss/magazin/news",
            "MYNET MAGAZİN":"https://www.mynet.com/magazin/rss",

            "DÜNYA":"https://www.dunya.com/rss?dunya",
            "HÜRRİYET DÜNYA":"http://www.hurriyet.com.tr/rss/dunya",
            "MİLLİYET DÜNYA":"http://www.milliyet.com.tr/rss/rssNew/dunyaRss.xml",
            "SABAH DÜNYA":"https://www.sabah.com.tr/rss/dunya.xml",
            "YENİ AKİT DÜNYA":"https://www.yeniakit.com.tr/rss/haber/dunya",
            "YENİ ŞAFAK DÜNYA":"https://www.yenisafak.com/rss-feeds?category=dunya",
            "A DÜNYA":"https://www.ahaber.com.tr/rss/dunya.xml",
            "CNN DÜNYA":"https://www.cnnturk.com/feed/rss/dunya/news",
            "MYNET DÜNYA":"http://www.mynet.com/haber/rss/kategori/dunya/",

            "YENİ AKİT SİYASET":"https://www.yeniakit.com.tr/rss/haber/siyaset",
            "MİLLİYET SİYASET":"https://www.milliyet.com.tr/rss/rssNew/siyasetRss.xml"	


        }
        if resource in urls:
            feed = feedparser.parse(urls[resource])  # RSS feed'i parse eder
            # Haber bilgilerini al
            return [{"title": entry.title, 
                     "link": entry.link,
                     "summary": entry.summary,
                     "published": entry.published} for entry in feed.entries]
        return []  # Eğer kaynak URL bulunamazsa boş liste döner

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
