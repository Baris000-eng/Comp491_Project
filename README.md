# Comp491_Project
This is the repository of our Comp491 Computer Engineering Senior Design Project.

Group Members:

1-) Özkan Yamaner

2-) Batuhan Altınyollar

3-) Barış Kaplan

4-) Lütfü Mustafa Kemal Ato

5-) Vedat Can Akın


Su an projede kalanlar: 
- Admin ekrani ve signupi
- Admin icin bazi verilerin gorsellestirilmesi (fakulte isimleri, her fakultedeki derslik isimleri, dersliklerin ne icin kullanildiklari (classroom, computer lab, aktif ogrenme sinifi vb), her sinifin sinif kapasiteleri, reserve edilmis olan classlar, hangi sinifta hangi ogrenci/ogrenciler ne zaman ders calisiyo, hangi ogretmenler hangi sinifta ne zaman sinav/ps/ders yapacak, vb. bilgiler).
- classroom infodan girilip ordan bir ders reserve edilirken (yandaki minik reserve buttonina basip) userlari rollerine gore farkli signup ekranlarina yonlendirme ve buralardan signup olmasini saglama.
- Chat implementasyonu
- Code refactor etme sadelestirme ve daha moduler hale getirme
- Admin logini ve flask authentication
- Veri gorsellestirmede hangi fakultede kac sinif var onun histogrami da yapilabilir
- Bide ek olarak su yapilabilir: faculties diye bi ekran olcak on yuzde ayrica her fakulte icin de ayri ayri ekran olcak. Facultiesden fakulte adina basinca fakultenin kendi ekranina gidecek. Orda da 8 - 10 civari class olcak mesela. Her classin radio buttoni veya checkboxu veya buna benzer bir ui elementi olcak. Ona basinca classin anlik kapasitesi, içeride kimin olduğu, sınıfın anlık olarak rezerve olup olmadığı, hangi saatlerde kimin rezerve ettiği gözükebilir.
- Mesela öğrenci sosb07yi kendi çalışmak için rezerve edince sosb07'nin checkboxuna/radio buttonına basınca şu yazcak: 

Total capacity: 120
Current capacity: 119
Reservation status: Reserved
Reservation Time: 19:00 - 20:00
Reserved By: xyz
- Böyle böyle reservation geldikçe current capacityyi düşürürüz
- Bide password updateleme user rolüne göre her rol için olcak o var.
