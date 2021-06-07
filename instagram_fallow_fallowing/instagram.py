from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys 
import os
import json
import pandas as pd


class User:
    
    
    def __init__(self,username,password):
                self.username=username
                self.password=password


class userrepository:
    
    
    def __init__(self):
                self.users=[]
                self.linkler=[]
                self.islogedin=False
                self.currentudrt={}
                
                self.loaduser()
                
        
    def loaduser(self):

                if os.path.exists('instagramusers.json'):

                        with open('instagramusers.json','r',encoding="utf-8") as file:
                                newUser=json.load(file)

                                for user in newUser:
                                        user=json.loads(user)
                                        newUser2=User(username=user['username'],password=user['password'])
                                        self.users.append(newUser2)
                                        

    def register(self,user:User):
                c=False
                for i in range(0,len(self.users)):
                    if self.users[i].username==user.username:
                        c=True
                if c:
                    time.sleep(0.5)
                    print("Varolan Bir Kullanıcı")
                else:
                    self.users.append(user)
                    self.savetofile()
                    time.sleep(0.5)
                    print("Kullanıcı Oluşturuldu")
                        

    def savetofile(self):
                liste=[]

                for user in self.users:
                        liste.append(json.dumps(user.__dict__))

                with open('instagramusers.json','w',encoding="utf-8") as file:
                        json.dump(liste,file,ensure_ascii=False)


    def logout(self):
                if self.islogedin:
                    self.islogedin=False
                    self.currentudrt={}
                    print("Çıkış Yapılmıştır")
                else:
                    print("Henüz Giriş Yapılmamıştır")    
    
    
    def sendusername(self):      
            uusername=self.currentudrt.username
            return  uusername        
 
 
    def sendPassword(self):
            ppassword=self.currentudrt.password
            return  ppassword
        
                
    def login(self):
            a=1
            for i in self.users:
                print(f"{a} ) {i.username}")
                a+=1
            secim=input("Hangi Kullanıcı İle Giriş Yapmak İstiyorsunuz:")
            if self.currentudrt==self.users[int(secim)-1]:
                print("Bu Kullanıcı İle Zaten Giriş Yapıldı")
            else:
                self.currentudrt=self.users[int(secim)-1]
                self.islogedin=True
                print ("Giriş Yapıldı")
            
        
    def deleteuser(self):
            if len(self.users)>0:
                q=1
                for i in self.users:
                    print(f"{q} ) {i.username}")
                    q+=1
                print("g )Geri")
                secim=input("Hangi Kullanıcıyı Silmek İstiyorsunuz :")
                
                if secim=="g":
                    pass    
                else:
                    del self.users[int(secim)-1] 
                    
                    liste=[]
                    for user in self.users:
                        liste.append(json.dumps(user.__dict__))

                    with open('instagramusers.json','w',encoding="utf-8") as file:
                            json.dump(liste,file,ensure_ascii=False)
                    print("Kullanıcı Silinmiştir")
            else:
                print("Silinecek Kullanıcı Bulunamadı")


    def cevir(self,TakipEtmeyenler):
        for i in TakipEtmeyenler:
            link="https://www.instagram.com/"+i+"/?hl=tr"
            self.linkler.append(link)
        return self.linkler
            

class islemler:
    
        
    def __init__(self,username,password):
        self.driver=webdriver.Chrome()
        self.driver.maximize_window()
        self.username=username
        self.password=password
        self.takipciler=[]
        self.takipedilenler=[]
        self.geritakipetmeyenler=[]
        self.geritakipetmediklerim=[]
        self.sayfayagit()
        self.girisyap()
        
        
    def sayfayagit(self):    
        self.driver.get("https://www.instagram.com/?hl=tr")
        time.sleep(3)
    
        
    def girisyap(self):  
        try:
            detail = self.driver.find_elements_by_class_name('_2hvTZ')
            detail[0].clear()
            detail[1].clear()
            detail[0].send_keys(self.username)
            detail[1].send_keys(self.password)
            self.driver.find_element_by_class_name('L3NKy').click()
            time.sleep(3)
        except:
            print("Yanlış Bilgiler Girdiniz")
                     
                
    def profilegit(self):
        
        self.driver.get(f"https://www.instagram.com/{self.username}")
        time.sleep(3)
        
   
    def takipcilerial(self):   
        self.profilegit()
        time.sleep(0.6)
        
        self.driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/header/section/ul/li[2]/a").click()
        time.sleep(0.6) 
            
        dialog=self.driver.find_element_by_css_selector("div[role=dialog]")
        
        
        takipcisayisi=len(dialog.find_elements_by_css_selector("li"))
        action=webdriver.ActionChains(self.driver)
        
        while True:
            dialog.click()            
            action.key_down(Keys.SPACE).key_up(Keys.SPACE).perform()#scroll rockda aşağı inecek
            time.sleep(0.6)
            action.key_down(Keys.SPACE).key_up(Keys.SPACE).perform()
            yenitakipcisayisi=len(dialog.find_elements_by_css_selector("li"))
            if yenitakipcisayisi!=takipcisayisi:
                takipcisayisi=yenitakipcisayisi 
                       
            else:
                break
            
        takipciler=dialog.find_elements_by_css_selector("li")    
        for i in takipciler:
            isim=i.find_element_by_tag_name("a").get_attribute("href")
            isim=isim.split("/")
            isim=isim[3]
            self.takipciler.append(isim)
    
    
    def takipedilenlerial(self):
            
        self.profilegit()
        time.sleep(0.6)
        self.driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/header/section/ul/li[3]/a").click()    
        time.sleep(0.6)
        dialog=self.driver.find_element_by_css_selector("div[role=dialog]")
        
        
        takipedilenlersayisi=len(dialog.find_elements_by_css_selector("li") )
        action=webdriver.ActionChains(self.driver)
        
        while True:
            dialog.click()            
            action.key_down(Keys.SPACE).key_up(Keys.SPACE).perform()#scroll rockda aşağı inecek
            time.sleep(0.6)
            action.key_down(Keys.SPACE).key_up(Keys.SPACE).perform()
            yenitakiedilenlersayisi=len(dialog.find_elements_by_css_selector("li"))
            if yenitakiedilenlersayisi!=takipedilenlersayisi:
                takipedilenlersayisi=yenitakiedilenlersayisi       
            else:
                break
        takipedilenler=dialog.find_elements_by_css_selector("li")    
        for i in takipedilenler:
            isim=i.find_element_by_tag_name("a").get_attribute("href")
            isim=isim.split("/")
            isim=isim[3]
            self.takipedilenler.append(isim)


    def gtler(self):
        self.takipcilerial()
        self.takipedilenlerial()
        for i in self.takipedilenler:
            degisken=False
            for j in self.takipciler:
                if i==j:
                    degisken=True
            if degisken==False:
                self.geritakipetmeyenler.append(i)
        
        for i in self.takipciler:
            degisken=False
            for j in self.takipedilenler:
                if i==j:
                    degisken=True
            if degisken==False:
                self.geritakipetmediklerim.append(i)


    def takipedilensil(self,TakipEtmeyenler):

        for i in TakipEtmeyenler:
            self.driver.get(i)
            time.sleep(0.5)
            self.driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/header/section/div[1]/div[1]/div/div[2]/div/span/span[1]/button").click()
            self.driver.find_element_by_css_selector("div[role=dialog] button").click()  
            time.sleep(0.5)     


    def chromekapat(self):
        self.driver.quit()


    def minimizewindow(self):
        self.driver.minimize_window()
  
    
    def maximize_window(self):
        self.driver.maximize_window()    


class Menü:
    userresp=userrepository()
    while True:
        print("\n")
        print("MENÜ".center(150,"*"))
        sayı=input("\n1 )Kullanıcı Olustur\n2 )Giris Yap\n3 )Hesaptan Cıkıs Yap\n4 )Bilgiler ve İslemler\n5 )Kullanıcı Sil\nc )Cıkıs\nSeçiminz:")
        if sayı =="c":
            exit()
        else:
            
            
            if sayı=="1":
                try:
                    username=input("Kullanıcı Adınız:")
                    password=input("Sifre:")        
                    kullanıcı=User(username,password)
                    userresp.register(kullanıcı)
                except:
                    print("Yanlış Bilgi Girdiniz")                        
            
            
            elif sayı=="2":
                try:
                    userresp.login()
                                
                except:
                    print("\nVarolmayan Bir Sıra Seçtiniz")    
            
            
            elif sayı=="3":
                try:
                    userresp.logout()
                except:
                    pass
                                    
            
            elif sayı=="4":
                
                
                try:
                    username=userresp.sendusername()
                    password=userresp.sendPassword()
                    print("\n")
                    print(f'Giriş Yapılan Hesap : {username}')
                    print("\n")
                    print("İŞLEM MENÜSÜ".center(150,"*"))
                    secim=input("\n1.)TakipEtmeyenler\n2.)TakipEtmediklerin\n3.)İkiside\ng.)Geri\nc.)Çıkış\nSeçiminiz:")
                    
                    
                    if secim=="1":
                        time.sleep(0.5)
                        islem=islemler(username,password) 
                        islem.gtler()
                        geritakipetmeyenler=islem.geritakipetmeyenler
                        geritakipetmediklerim=islem.geritakipetmediklerim 
                        islem.minimizewindow()
                        
                    
                    if secim=="2":   
                        time.sleep(0.5)
                        islem=islemler(username,password) 
                        islem.gtler()
                        geritakipetmeyenler=islem.geritakipetmeyenler
                        geritakipetmediklerim=islem.geritakipetmediklerim 
                        islem.minimizewindow()
                        
                    if secim=="3":   
                        time.sleep(0.5)
                        islem=islemler(username,password) 
                        islem.gtler()
                        geritakipetmeyenler=islem.geritakipetmeyenler
                        geritakipetmediklerim=islem.geritakipetmediklerim 
                        islem.minimizewindow()
                        
                    while True:
             
                        if secim=="1":
                            
                            try:
                                
                                print(f'\nGeri Takip Etmeyenler: {len(geritakipetmeyenler)}')
                                time.sleep(0.5)
                                print("\n\n")
                                a=1
                                for i in geritakipetmeyenler:
                                    print(f'{a}.){i}')
                                    a=a+1
                                    
                                silme=input("Takipten Çıkamk İstediklerinizi Sırayla ,Araya ',' Koyarak Seçiniz İstemiyorsanız g Tuşuna Basınız\nSecim:")
                                
                                
                                try:
                                
                                    if silme=="g":
                                        pass
                                    else:
                                        islem.maximize_window()    
                                        silme1=silme.split(",")
                                        silme2=[]
                                        degisken1=[]
                                        for i in silme1:
                                            degisken=int(i)-1
                                            degisken1.append(degisken)
                                            silme2.append(geritakipetmeyenler[degisken])
                                        a=0
                                        for i in degisken1:                                            
                                            geritakipetmeyenler.pop(i-a)
                                            a+=1
                            
                                        silme3=userresp.cevir(silme2)
                                        time.sleep(0.5)
                                        islem.takipedilensil(silme3)
                                        time.sleep(0.5)
                                        islem.minimizewindow()
                                        
                                except:
                                    print("Yanlış Tuşlama Yaptınız")

                            except:
                                print("\nKullanıcı Bilgileri yanlış")
                                            
                                        
                        elif secim=="2":
                            try:
                                print(f'\nGeri Takip Etmediklerin: {len(geritakipetmediklerim)}')                            
                                time.sleep(0.5)
                                print("\n\n")
                                for i in geritakipetmediklerim:
                                    print(i)
                            except:
                                print("\nKullanıcı Bilgileri yanlış")  


                        elif secim=="3":
                            try:
                                print(f'\nGeri Takip Etmediklerin: {len(geritakipetmediklerim)}\nGeri Takip Etmeyenler: {len(geritakipetmeyenler)}')
                                df1=pd.Series(geritakipetmediklerim,name="Geri Takip Etmediklerim")
                                df2=pd.Series(geritakipetmeyenler,name="Geri Takip Etmeyenler")
                                df=pd.concat([df1,df2],axis=1)
                                df=df.fillna(" ")
                                print("\n\n")
                                print(df)
                            except:
                                print("\nKullanıcı Bilgileri yanlış") 


                        elif secim=="c":
                            islem.chromekapat()
                            break


                        elif secim=="g":
                            islem.chromekapat()
                            break


                        else:
                            print("Yanlış Tuşlama Yaptınız")
                        time.sleep(0.5)
                        print("\n")
                        print("İŞLEM MENÜSÜ".center(150,"*"))
                        secim=input("\n1.)TakipEtmeyenler\n2.)TakipEtmediklerin\n3.)İkiside\ng.)Geri\nc.)Çıkış\nSeçiminiz:")                    
                                        
                except:
                    print("\nHenüz Giriş Yapılmamıştır")
                                       
                    
            elif (sayı=="5"):
                try:
                    userresp.deleteuser()
                                    
                except:
                    print("\nYanlış Seçim Yaptınız")
                                
            else:
                print("yanlış seçim")
            try:
                if secim=="c":
                    break       
            except:
                pass

