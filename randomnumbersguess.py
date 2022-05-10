
import random 
sayi = random.randint(0,10)
hak  = 10


while hak != 0 :
    girdi = int(input("Sayı giriniz... : "))
   

    if girdi == sayi :
      print("Tebrikler! Kazandınız.")
      break

    if girdi > sayi :
      print ("Maalesef ! Daha düşük bir sayı deneyiniz ")
      hak = hak - 1 
      print(f"Kalan hakkınız : {hak}")

    if girdi < sayi :
      print("Maalesef! Daha yüksek bir sayı deneyiniz ")
      hak = hak - 1
      print(f"Kalan hakkınız : {hak}")

(skor) = hak * 10
print("Toplam skorunuz : "  + str(skor) )      





