#!/usr/bin/env python
# coding: utf-8

# In[2]:


import random
#Python'ın random modülünü programımıza dahil ediyoruz. Bu modül, rastgele sayılar ve seçimler oluşturmak için kullanılır.

# Şehirlerin koordinatlarını temsil eden bir liste
cities = [(0, 0), (1, 3), (5, 8), (9, 4), (6, 1)]
#cities adında bir liste oluşturuyoruz.
#Bu liste, şehirlerin koordinatlarını (x, y) çiftleri olarak içerir. Örneğin, (0, 0) koordinatları ilk şehri temsil eder.

# Karınca kolonisi parametreleri
num_ants = 5  #num_ants değişkenine 5 değerini atıyoruz. Bu, kullanacağımız karınca sayısını belirler.
num_iterations = 50 #num_iterations değişkenine 50 değerini atıyoruz. Bu, algoritmanın kaç iterasyon boyunca çalışacağını belirler.
alpha = 1   # Feromon etkileme katsayısı
beta = 2    # Uzaklık etkileme katsayısı
evaporation_rate = 0.5 #evaporation_rate değişkenine 0.5 değerini atıyoruz.
#Bu, feromonların her iterasyonda ne kadar buharlaşacağını belirler. Daha yavaş buharlaşma, feromonların daha uzun süre etkili olmasını sağlar.



# Feromon matrisi: Şehirler arası feromon seviyelerini tutar
pheromone = [[1.0 for _ in range(len(cities))] for _ in range(len(cities))]
#Bu matris, şehirler arası feromon seviyelerini saklayacak. İlk başta, tüm feromon seviyelerini 1.0 olarak başlatıyoruz.
#Bu, tüm yolların başlangıçta eşit derecede etkili olduğu anlamına gelir.



# Uzaklık matrisi: Şehirler arası uzaklıkları tutar
distance = [[0.0 for _ in range(len(cities))] for _ in range(len(cities))]
for i in range(len(cities)):
    for j in range(len(cities)):
        distance[i][j] = ((cities[i][0] - cities[j][0]) ** 2 + (cities[i][1] - cities[j][1]) ** 2) ** 0.5
#Bu matris, şehirler arası uzaklıkları saklayacak. İki şehir arasındaki uzaklığı hesaplamak için Euclidean mesafe formülünü kullanıyoruz. 
#Bu matris, algoritmanın herhangi iki şehir arasındaki uzaklığı bulmasına yardımcı olacak.


# Başlangıç şehri
start_city = 0 # Bu, karıncaların başlangıçta hangi şehirden hareket edeceklerini belirler.




# Her bir iterasyonda en iyi yol ve toplam mesafe
best_path = None
best_distance = float('inf')
#best_path değişkenine None (boş) değerini ve best_distance değişkenine sonsuz (∞) değerini atıyoruz. 
#Bu değişkenler, her iterasyonda en iyi yolun ve en kısa mesafenin saklanacağı değişkenlerdir.
#Başlangıçta en iyi yol veya mesafe bilinmediği için bu değerleri başlangıç değerleri olarak ayarlıyoruz.


# Karınca yürüyüşü fonksiyonu
def ant_walk(ant_path):
    current_city = start_city
    while len(ant_path) < len(cities):
        # Şehirleri ziyaret edip feromon ve uzaklık bilgilerine dayanarak bir sonraki şehri seç
        next_city = select_next_city(current_city, ant_path)
        ant_path.append(next_city)
        current_city = next_city
#ant_walk fonksiyonu, bir karıncanın belirli bir yol boyunca hareket etmesini simüle eder. 
#ant_path parametresi, karıncanın mevcut yolunu temsil eden bir liste olarak geçilir.
#Fonksiyon, ant_path listesinin uzunluğu şehir sayısına eşit olana kadar (yani tüm şehirler ziyaret edilene kadar) çalışır. 
#Her adımda, select_next_city fonksiyonu çağrılarak bir sonraki şehir seçilir ve bu şehir ant_path listesine eklenir.



# Bir sonraki şehri seçme fonksiyonu
def select_next_city(current_city, ant_path):
    # Bir sonraki şehir seçimi için olasılık hesaplama
    probabilities = []
    for city in range(len(cities)):
        if city not in ant_path:
            pheromone_factor = pheromone[current_city][city] ** alpha
            distance_factor = (1.0 / distance[current_city][city]) ** beta
            probabilities.append(pheromone_factor * distance_factor)
        else:
            probabilities.append(0.0)
    
    total_prob = sum(probabilities)
    probabilities = [prob / total_prob for prob in probabilities]

#select_next_city fonksiyonu, bir karıncanın bir sonraki şehiri seçerken kullanacağı olasılıkları hesaplar.
#Her şehir için, eğer o şehir daha önce ziyaret edilmediyse feromon ve uzaklık faktörlerine dayalı bir olasılık hesaplanır.
#Ve probabilities listesine eklenir. Eğer şehir zaten ziyaret edildiyse, olasılık olarak 0 eklenir.
#Sonrasında, hesaplanan olasılıklar normalize edilir (toplam 1 olacak şekilde ayarlanır).V
#Ve bu olasılıklar probabilities listesine kaydedilir. 
#Bu, bir sonraki şehir seçimini rastgele yaparken olasılıklara dayanılmasını sağlar.
    
    
# Olasılıklara dayanarak bir sonraki şehiri seç
    next_city = random.choices(range(len(cities)), probabilities)[0]
    return next_city
#next_city değişkenine, random.choices fonksiyonunu kullanarak, probabilities listesine dayalı olarak bir sonraki şehir seçimi atanır.
#random.choices fonksiyonu, verilen bir listeden rastgele öğeler seçmeye yardımcı olur. 
#Seçilen şehir, return ifadesiyle fonksiyondan döndürülür.



# Feromon güncelleme fonksiyonu
def update_pheromone(ant_paths):
    for i in range(len(pheromone)):
        for j in range(len(pheromone[i])):
            pheromone[i][j] *= (1.0 - evaporation_rate)
            for ant_path in ant_paths:
                if j in ant_path:
                    pheromone[i][j] += 1.0 / len(ant_path)

#update_pheromone fonksiyonu, feromon seviyelerinin güncellenmesini sağlar.
#Bu fonksiyon, her iterasyonda çağrılır ve feromon seviyelerini güncellemek için kullanılır.
#İç içe iki döngü kullanarak, pheromone matrisinin her elemanını güncelleriz.
#İlk döngü i indeksi ile satırları, ikinci döngü j indeksi ile sütunları temsil eder.
#Feromon buharlaşmasını hesaplamak için, her feromon seviyesini (1.0 - evaporation_rate) ile çarparız. 
#Bu, feromonun belirli bir oranda buharlaşmasını temsil eder.
#Sonra, her karınca yolunda gezinirken, feromon seviyelerini artırmak için bir iç döngü kullanırız.
#Eğer j şehri bir karınca yolunda bulunuyorsa (yani j ant_path içinde), ilgili feromon seviyesini 1.0 / len(ant_path) ile artırırız.
#Bu, karıncanın izlediği yolun feromonla güçlendirilmesini sağlar.
            
# Ana döngü
for iteration in range(num_iterations):
    ant_paths = []
    for _ in range(num_ants):
        ant_path = [start_city]
        ant_walk(ant_path)
        ant_paths.append(ant_path)
        
        # En iyi yol güncellemesi
        if sum([distance[ant_path[i - 1]][ant_path[i]] for i in range(1, len(ant_path))]) < best_distance:
            best_path = ant_path[:]
            best_distance = sum([distance[best_path[i - 1]][best_path[i]] for i in range(1, len(best_path))])
    
    update_pheromone(ant_paths)

#Bu döngü, belirtilen sayıda num_iterations iterasyon boyunca çalışır. 
#Her bir iterasyonda, her bir karınca num_ants kadar yürüyüş yapar ve sonuçlar ant_paths listesine eklenir.
#Her bir karınca için ant_walk fonksiyonu çağrılır ve karınca belirli bir yol boyunca hareket eder.
#Sonrasında, en iyi yol güncellemesi yapılır.
#Eğer karıncanın yolu, daha önce bulunan en iyi yoldan daha kısaysa (sum([distance[ant_path[i - 1]][ant_path[i]] for i in range(1, len(ant_path))]) < best_distance), en iyi yol ve en iyi mesafe güncellenir.
#Bu, algoritmanın en iyi yol ve mesafeyi kaydederek ilerlediği yerdir.
#Her bir iterasyonun sonunda, update_pheromone fonksiyonu çağrılarak feromon seviyeleri güncellenir.
#Bu, algoritmanın feromonların buharlaşmasını hesaplar ve karıncaların izlediği yolları güçlendirir.



# Sonuçları yazdır
print("En iyi yol:", best_path)
print("En iyi mesafe:", best_distance)

#Tüm iterasyonlar tamamlandığında, en iyi yol ve en iyi mesafe sonuçları ekrana yazdırılır. 
#Bu, algoritmanın en iyi çözümü bulduğunda hangi yolun ve mesafenin olduğunu gösterir.


# In[ ]:




