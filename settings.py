#### MUZE APP Interactif Video ve ses medyalarını oynama uygulaması
#### Senaryo seçimi ile farklı uygulama alanalarında kullanır.
#### Bu dosyayıdaki değişkenleri düzenledikten sonra cihazı açıp kapatılması gerekmektedir.


#### Ayarlanabilir Değişkenler

_debug      = True  # True veya False yazılır 
senaryo     = 1      # Seçtiğiniz Senaryo, detaylar için aşağıdaki şartları inceleyin
limit       = 180    # Santim cinsinden, bu değer ve altı durumlarda algılar
delay       = 200    # Ms cinsinden yaklaşık bir sonraki ölçüm için bekleme.
scan        = 5      # Kaç ölçüm ortalaması limit değerin altındaysa sistem aktif olur 
lostInTime  = 5      # Saniye cinsinden algılama kaybedildikten sonra aktif kalma süresi
startDelay  = 0      # Saniye cinsinden algılama oluşunca aktifleşmeden önceki bekleme
m_width     = "1920"
m_height    = "1080"
#### SENARYOLAR

#Senaryo 1
#Hareket Sensörlü Ekranlar
#   Sensör algıladığında video başlar
#   {lostInTime} sn eğer kimseyi göremezse video kesilir.
#   Video başa döner

#Senaryo 2 
#Butonlu Ekranlar
#   Düğmeye basıldığında kapanana kadar video oynayacak
#   {startDelay}  sn sonrasında video başlayacak

#Senaryo 3 
#Kulaklı Ekranlar (Videolu)
#   Video sürekli oynayacak.
#   Ses Kulaklıktan aktarılacak

#Senaryo 4 
#Kulaklı Ekranlar (Audio)
#   Düğmeye basıldığında kapana kadar ses kulaklıktan verilecek
#   {startDelay} sn sonrasında ses başlayacak

#Senaryo 5
#Dev Kulaklık
#   Sensör algıladığında ses başlar
#   {lostInTime} sn eğer kimseyi göremezse ses kesilir.
#   Video başa döner

#Senaryo 6 
#Diafon
#   Düğmeye basıldığında kapana kadar ses kulaklıktan verilecek
#   {startDelay}  sn sonrasında ses başlayacak

#Senaryo 7
#Laterna
#   Sensör algıladığında ses başlar
#   {lostInTime} sn eğer kimseyi göremezse ses kesilir.
#   Video başa döner

#Senaryo 8 
#Bavul Ekranlar
#   Sensör algıladığında video başlar
#   {lostInTime} sn eğer kimseyi göremezse video kesilir.
#   Video başa döner