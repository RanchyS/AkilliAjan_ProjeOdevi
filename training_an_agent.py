import numpy as np

def durum_matrisi_olusturma(matris_boyutu): # Spesifik bir matris için kullanılabilir. Rastgelelik ile entegre edilecek. 
    matris_boyutu = 4 # [4,5,6,7,8]
    durum_matrisi = np.zeros((matris_boyutu,matris_boyutu),dtype="str")

    durum_matrisi[:][:]= "F" 

    durum_matrisi[3][0] = "S"
    durum_matrisi[2][2] = "G"
    durum_matrisi[0][0] = "H"
    durum_matrisi[0][1] = "H"
    durum_matrisi[1][1] = "H"

    return durum_matrisi

def q_table_olusturma(matris_boyutu):
    q_table = np.zeros((matris_boyutu*matris_boyutu,4)) # 4 sabit çünkü eylem uzayımız 4 elemanlı: [sol,sağ,alt,üst]
    return q_table

def qt_donusum(bulunulan_durum): # q_table'nin satir indisini döndürür!
    # q_table aslında 3 boyutta anlam ifade ediyor fakat optimizasyon için iki boyuta indirgedim, aşağıdaki bağıntı bunu sağlıyor!
    return bulunulan_durum[0] * 4 + bulunulan_durum[1]

def eylem_secme(bulunulan_durum): # bulunulan durum bir tuple (satır,sütun). epsilon-greedy stratejisine göre seçilir.
    secilen_eylem = ""
    if(np.random.rand() < epsilon):
        secilen_eylem = eylem_matrisi[np.random.randint(0,4)] # rastgele bir eylem seçer. epsilon policy, keşif!
    else:        
        secilen_eylem = eylem_matrisi[q_table[qt_donusum(bulunulan_durum)].argmax()] # q tablosundaki maksimum değeri alır. greedy policy, sömürü!
    
    return secilen_eylem

def eylem_gercekleme(bulunulan_durum,secilen_eylem):

    if secilen_eylem == "L":
        bulunulan_durum = (bulunulan_durum[0],bulunulan_durum[1]-1) if bulunulan_durum[1] != 0 else bulunulan_durum

    elif secilen_eylem == "R":
        bulunulan_durum = (bulunulan_durum[0],bulunulan_durum[1]+1) if bulunulan_durum[1] != matris_boyutu - 1 else bulunulan_durum

    elif secilen_eylem == "D":
        bulunulan_durum = (bulunulan_durum[0]+1,bulunulan_durum[1]) if bulunulan_durum[0] != matris_boyutu - 1 else bulunulan_durum

    else: # "U"
        bulunulan_durum = (bulunulan_durum[0]-1,bulunulan_durum[1]) if bulunulan_durum[0] != 0 else bulunulan_durum

    return bulunulan_durum


def odul_al(bulunulan_durum):
    durum = durum_matrisi[bulunulan_durum[0]][bulunulan_durum[1]]
    odul = 0
    if durum == "G":
        odul = 100
    elif durum == "H":
        odul = -100
    else: # Geriye yalnızca "F" kalıyor!
        odul = -1 # en kısa yolu bulmaya çalışması için.
    
    return odul

# bulunulan hücreden 4 yönde de alınabilecek en yüksek puanı buluyor, halbuki formülde kastedilen bu değil!
# formülde kastedilen, gidilecek yerdeki en yüksek puandır. 
"""
def sonraki_eniyi_durum(bulunulan_durum):
    sonraki_durumlar = np.zeros(4,dtype=tuple) # sırasıyla; sol,sağ,alt,üst.
    sonraki_durumlar[0] = eylem_gercekleme(bulunulan_durum, "L") # for ile eylem uzayından da yapılabilir
    sonraki_durumlar[1] = eylem_gercekleme(bulunulan_durum, "R") # okunurluk için böyle yazdım.
    sonraki_durumlar[2] = eylem_gercekleme(bulunulan_durum, "D")
    sonraki_durumlar[3] = eylem_gercekleme(bulunulan_durum, "U")

    eniyi_durum = sonraki_durumlar[0]
    
    for sonraki_durum in sonraki_durumlar:
        if q_table[qt_donusum(eniyi_durum)].max() < q_table[qt_donusum(sonraki_durum)].max(): # burada hata var gibi, kontrol edilmeli! q_table erişimde
            eniyi_durum = sonraki_durum

    return eniyi_durum
"""

def q_table_guncelleme(bulunulan_durum, secilen_eylem): # bellman eşitliğine göre
    sutun = 0
    sonraki_durum = eylem_gercekleme(bulunulan_durum, secilen_eylem)
    if secilen_eylem == "L":
        sutun = 0
    elif secilen_eylem == "R":
        sutun = 1
    elif secilen_eylem == "D":
        sutun = 2
    else:
        sutun = 3
        
    q_table[qt_donusum(bulunulan_durum)][sutun] = q_table[qt_donusum(bulunulan_durum)][sutun] + alpha * (odul_al(sonraki_durum) + gamma * q_table[qt_donusum(sonraki_durum)].max() - q_table[qt_donusum(bulunulan_durum)][sutun])

def train(epoch):
    global epsilon # python :')

    epoch = 1000
    while(0 < epoch): # epoch sayısı
        bulunulan_durum = baslangic_durumu # başlangıç durumu için: sol-alt kısımdan oyun başlatılacağından ilgili değeri jenerik olarak oluşturmalıyız.
        adim_sayaci = 0

        while(True):
            secilen_eylem = eylem_secme(bulunulan_durum)
            q_table_guncelleme(bulunulan_durum, secilen_eylem)
            bulunulan_durum = eylem_gercekleme(bulunulan_durum, secilen_eylem)
            
            if durum_matrisi[bulunulan_durum[0]][bulunulan_durum[1]] == "G" or durum_matrisi[bulunulan_durum[0]][bulunulan_durum[1]] == "H": # baslangic durumu zaten bunlardan biri olamaz. Onu atlamış olmamızın bir sakıncası yok yani.
                break
            elif adim_sayaci >= 1000:
                break
            else:
                adim_sayaci += 1

        if (epsilon * epsilon_azaltma_orani < min_epsilon):
            epsilon = min_epsilon
        else:
            epsilon = epsilon * epsilon_azaltma_orani

        epoch -= 1

def optimal_yolu_dondur(matris_boyutu):
    bulunan_yollar = np.zeros(matris_boyutu * matris_boyutu,dtype=str)
    
    i = 0
    while i < len(bulunan_yollar):
        yon = q_table[i].argmax()
        if yon == 0:
            yon = "L"
        elif yon == 1:
            yon = "R"
        elif yon == 2:
            yon = "D"
        else:
            yon = "U"

        bulunan_yollar[i] = yon
        i += 1
    
    return bulunan_yollar


""" epsilon değerinin min değerine ulaşmasının kaçıncı iterasyonda olduğunu öğrenmek için yazılan bir kod parçası.
i = 0
while i<1000:
    
    if(epsilon * epsilon_azaltma_orani < min_epsilon):
        epsilon = min_epsilon
        print(epsilon)
        print(i) # 918
        break
    else:
        epsilon = epsilon * epsilon_azaltma_orani
        print(epsilon)
    i = i+1
"""

#hiperparametreler
alpha = 0.1 # öğrenme katsayısı
gamma = 0.9 # sonraki adımlarda kazanılabilecek ödülleri dikkate alma oranı.

epsilon = 1
epsilon_azaltma_orani = 0.995
min_epsilon = 0.01 # i = 918 için bu değere ulaşıyor!

# ilgili durumda(matris konumunda) gerçekleştirilecek olan eylemi seçmek: epsilon-greedy stratejisi
# epsilon = 1 -> eylem uzayından bir eylem "rastgele" olarak seçilir.
# epsilon = 0 -> eylem uzayından bir eylem "q_tablosundaki en yüksek değere göre" seçilir.

eylem_matrisi = np.array(['L',"R","D","U"])


matris_boyutu = 4
durum_matrisi = durum_matrisi_olusturma(matris_boyutu)
baslangic_durumu = (matris_boyutu - 1, 0)

q_table = q_table_olusturma(matris_boyutu)

"""" klasörü yanlız çalıştırmak istiyorsanız bu yorumu kaldırın
train(1000)
bulunan_yollar = optimal_yolu_dondur(matris_boyutu)
print(bulunan_yollar)
"""
def matris_guncelle(guncel_matris):
    global durum_matrisi
    durum_matrisi = guncel_matris