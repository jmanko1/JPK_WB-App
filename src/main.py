import datetime
import os
import warnings
import xml.dom.minidom as md
import xml.etree.ElementTree as ET

import pandas as pd

from src.jpk_classes.operacja import Operacja
from src.jpk_classes.podmiot import Podmiot
from src.jpk_classes.rachunek import Rachunek
from src.validator.validator import validate_podmiot_values, validate_rachunek_values, validate_operacje_values, \
  validate_kod_urzedu, validate_dataframes

#Wczytanie plików zawierających zbiory danych
print("Wczytywanie pliku CSV zawierającego dane podmiotu.")
print("PelnaNazwa,NIP,REGON,KodKraju,Wojewodztwo,Powiat,Gmina,Ulica,NrDomu,NrLokalu,Miejscowosc,KodPocztowy,Poczta")
podmiot_file = input("Podaj ścieżkę do pliku CSV zawierającego dane podmiotu: ")
if not os.path.exists(podmiot_file):
  print("Podana ścieżka do pliku nie istnieje.")
  exit(1)

df_podmiot = pd.read_csv(podmiot_file)
warnings.filterwarnings("ignore")
df_podmiot.fillna("", inplace=True)
print()
print("Wczytano następujące dane podmiotu:")
print(df_podmiot, end="\n\n")

print("Wczytywanie pliku CSV zawierającego dane rachunku bankowego.")
print("NumerRachunku,KodWaluty")
rachunek_file = input("Podaj ścieżkę do pliku CSV zawierającego dane rachunku bankowego: ")
if not os.path.exists(rachunek_file):
  print("Podana ścieżka do pliku nie istnieje.")
  exit(1)

df_rachunek = pd.read_csv(rachunek_file)
df_rachunek.fillna("", inplace=True)
print()
print("Wczytano następujące dane rachunku bankowego:")
print(df_rachunek, end="\n\n")

print("Wczytywanie pliku CSV zawierającego dane operacji na rachunku bankowym.")
print("DataOperacji,NazwaPodmiotu,OpisOperacji,KwotaOperacji,SaldoOperacji")
operacje_file = input("Podaj ścieżkę do pliku CSV zawierającego dane operacji na rachunku bankowym: ")
if not os.path.exists(operacje_file):
  print("Podana ścieżka do pliku nie istnieje.")
  exit(1)

df_operacje = (pd.read_csv(operacje_file)).sort_values(by="DataOperacji")
df_operacje.fillna("", inplace=True)
print()
print("Wczytano następujące dane operacji na rachunku bankowym:")
print(df_operacje, end="\n\n")

warnings.filterwarnings("default")

#Walidacja struktur zbiorów danych
if validate_dataframes(df_podmiot, df_rachunek, df_operacje) == 1:
  exit(1)

#Rachunek - dane rachunku bankowego
#Podmiot - dane właściciela rachunku bankowego
#Operacje - operacje na rachunku bankowym

jpk_podmiot = Podmiot(df_podmiot.iloc[0,0], df_podmiot.iloc[0,1], df_podmiot.iloc[0,2], df_podmiot.iloc[0,3], df_podmiot.iloc[0,4], df_podmiot.iloc[0,5], df_podmiot.iloc[0,6], df_podmiot.iloc[0,7], df_podmiot.iloc[0,8], df_podmiot.iloc[0,9], df_podmiot.iloc[0,10], df_podmiot.iloc[0,11], df_podmiot.iloc[0,12])
jpk_rachunek = Rachunek(df_rachunek.iloc[0,0], df_rachunek.iloc[0,1])

jpk_operacje = list()
for indeks, wiersz in df_operacje.iterrows():
  jpk_operacja = Operacja(wiersz["DataOperacji"], wiersz["NazwaPodmiotu"], wiersz["OpisOperacji"], wiersz["KwotaOperacji"], wiersz["SaldoOperacji"])
  jpk_operacje.append(jpk_operacja)

#Walidacja danych
err1 = validate_podmiot_values(jpk_podmiot)
err2 = validate_rachunek_values(jpk_rachunek)
err3 = validate_operacje_values(jpk_operacje)

if err1 == 1 or err2 == 1 or err3 == 1:
  exit(1)

kod_urzedu = input("\nPodaj kod urzędu skarbowego: ")
err = validate_kod_urzedu(kod_urzedu)
if err == 1:
  print("Nieprawidłowy kod urzędu skarbowego.")
  exit(1)

suma_uznan = 0.0
suma_obciazen = 0.0
for operacja in jpk_operacje:
  if operacja.kwota_operacji < 0.0:
    suma_obciazen -= operacja.kwota_operacji
  else:
    suma_uznan += operacja.kwota_operacji

data_od = jpk_operacje[0].data_operacji
data_do = jpk_operacje[-1].data_operacji

data_wytworzenia = (datetime.datetime.now()).strftime("%Y-%m-%d %H:%M:%S")

#Generowanie pliku JPK_WB
root = ET.Element("tns:JPK")
root.set("xmlns:etd", "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2018/08/24/eD/DefinicjeTypy/")
root.set("xmlns:tns", "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2018/08/24/eD/DefinicjeTypy/")
root.set("xmlns:xsi", "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2018/08/24/eD/DefinicjeTypy/")
root.set("xsi:schemaLocation", "http://crd.gov.pl/wzor/2021/12/27/11148/schemat.xsd")

#Nagłówek pliku JPK_WB
naglowek = ET.SubElement(root, "tns:Naglowek")

kod_formularza = ET.SubElement(naglowek, "tns:KodFormularza")
kod_formularza.set("type", "tns:TKodFormularza")
kod_formularza.set("kodSystemowy", "JPK_WB (1)")
kod_formularza.set("wersjaSchemy", "1-0")
kod_formularza.text = "JPK_WB"

wariant_formularza = ET.SubElement(naglowek, "tns:WariantFormularza")
wariant_formularza.set("type", "xsd:byte")
wariant_formularza.text = "1"

cel_zlozenia = ET.SubElement(naglowek, "tns:CelZlozenia")
cel_zlozenia.set("type", "tns:TCelZlozenia")
cel_zlozenia.text = "1"

data_wytworzenia_jpk = ET.SubElement(naglowek, "tns:DataWytworzeniaJPK")
data_wytworzenia_jpk.set("type", "etd:TDataCzas")
data_wytworzenia_jpk.text = data_wytworzenia

data_od_jpk = ET.SubElement(naglowek, "tns:DataOd")
data_od_jpk.set("type", "etd:TData")
data_od_jpk.text = data_od

data_do_jpk = ET.SubElement(naglowek, "tns:DataDo")
data_do_jpk.set("type", "etd:TData")
data_do_jpk.text = data_do

domyslny_kod_waluty = ET.SubElement(naglowek, "tns:DomyslnyKodWaluty")
domyslny_kod_waluty.set("type", "kck:currCode_Type")
domyslny_kod_waluty.text = jpk_rachunek.kod_waluty.upper()

kod_urzedu_jpk = ET.SubElement(naglowek, "tns:KodUrzedu")
kod_urzedu_jpk.set("type", "etd:TKodUS")
kod_urzedu_jpk.text = kod_urzedu

#Dane podmiotu, którego dotyczy plik JPK_WB
podmiot1 = ET.SubElement(root, "tns:Podmiot1")

identyfikator_podmiotu = ET.SubElement(podmiot1, "tns:IdentyfikatorPodmiotu")
identyfikator_podmiotu.set("type", "etd:TIdentyfikatorOsobyNiefizycznej")

adres_podmiotu = ET.SubElement(podmiot1, "tns:AdresPodmiotu")
adres_podmiotu.set("type", "etd:TAdresPolski")

nip = ET.SubElement(identyfikator_podmiotu, "etd:NIP")
nip.set("type", "etd:TNrNIP")
nip.text = jpk_podmiot.nip

pelna_nazwa = ET.SubElement(identyfikator_podmiotu, "etd:PelnaNazwa")
pelna_nazwa.set("type", "xsd:token")
pelna_nazwa.text = jpk_podmiot.pelna_nazwa

regon = ET.SubElement(identyfikator_podmiotu, "etd:REGON")
regon.set("type", "etd:TNrREGON")
regon.text = jpk_podmiot.regon

kod_kraju = ET.SubElement(adres_podmiotu, "etd:KodKraju")
kod_kraju.set("type", "etd:TKodKraju")
kod_kraju.text = jpk_podmiot.kod_kraju.upper()

wojewodztwo = ET.SubElement(adres_podmiotu, "etd:Wojewodztwo")
wojewodztwo.set("type", "etd:TJednAdmin")
wojewodztwo.text = jpk_podmiot.wojewodztwo.lower()

powiat = ET.SubElement(adres_podmiotu, "etd:Powiat")
powiat.set("type", "etd:TJednAdmin")
zmienione_slowa = [slowo.capitalize() for slowo in jpk_podmiot.powiat.split()]
jpk_podmiot.powiat = ' '.join(zmienione_slowa)
powiat.text = jpk_podmiot.powiat

gmina = ET.SubElement(adres_podmiotu, "etd:Gmina")
gmina.set("type", "etd:TJednAdmin")
zmienione_slowa = [slowo.capitalize() for slowo in jpk_podmiot.gmina.split()]
jpk_podmiot.gmina = ' '.join(zmienione_slowa)
gmina.text = jpk_podmiot.gmina

ulica = ET.SubElement(adres_podmiotu, "etd:Ulica")
ulica.set("type", "etd:TUlica")
zmienione_slowa = [slowo.capitalize() for slowo in jpk_podmiot.ulica.split()]
jpk_podmiot.ulica = ' '.join(zmienione_slowa)
ulica.text = jpk_podmiot.ulica

nrdomu = ET.SubElement(adres_podmiotu, "etd:NrDomu")
nrdomu.set("type", "etd:TNrBudynku")
nrdomu.text = str(jpk_podmiot.nrdomu).upper()

nrlokalu = ET.SubElement(adres_podmiotu, "etd:NrLokalu")
nrlokalu.set("type", "etd:TNrLokalu")
nrlokalu.text = str(jpk_podmiot.nrlokalu)

miejscowosc = ET.SubElement(adres_podmiotu, "etd:Miejscowosc")
miejscowosc.set("type", "etd:TMiejscowosc")
zmienione_slowa = [slowo.capitalize() for slowo in jpk_podmiot.miejscowosc.split()]
jpk_podmiot.miejscowosc = ' '.join(zmienione_slowa)
miejscowosc.text = jpk_podmiot.miejscowosc

kod_pocztowy = ET.SubElement(adres_podmiotu, "etd:KodPocztowy")
kod_pocztowy.set("type", "etd:TKodPocztowy")
kod_pocztowy.text = jpk_podmiot.kod_pocztowy

poczta = ET.SubElement(adres_podmiotu, "etd:Poczta")
poczta.set("type", "etd:TMiejscowosc")
zmienione_slowa = [slowo.capitalize() for slowo in jpk_podmiot.poczta.split()]
jpk_podmiot.poczta = ' '.join(zmienione_slowa)
poczta.text = jpk_podmiot.poczta

#Numer rachunku bankowego
numer_rachunku = ET.SubElement(root, "tns:NumerRachunku")
numer_rachunku.set("type", "xsd:string")
numer_rachunku.text = jpk_rachunek.nrrachunku

#Saldo początkowe i końcowe wyciągu
saldo1 = jpk_operacje[0].saldo_operacji - jpk_operacje[0].kwota_operacji
saldo1 = "{:.2f}".format(saldo1)
saldo2 = "{:.2f}".format(jpk_operacje[-1].saldo_operacji)

salda = ET.SubElement(root, "tns:Salda")

saldo_pocz = ET.SubElement(salda, "tns:SaldoPoczatkowe")
saldo_pocz.set("type", "tns:TKwotowy")
saldo_pocz.text = saldo1

saldo_kocz = ET.SubElement(salda, "tns:SaldoKoncowe")
saldo_kocz.set("type", "tns:TKwotowy")
saldo_kocz.text = saldo2

#Operacje na rachunku bankowym
n_wierszy = 0

for jpk_operacja in jpk_operacje:
  wyciag_wiersz = ET.SubElement(root, "tns:WyciagWiersz")

  numer_wiersza = ET.SubElement(wyciag_wiersz, "tns:NumerWiersza")
  numer_wiersza.set("type", "tns:TNaturalnyJPK")
  numer_wiersza.text = str(n_wierszy + 1)

  data_operacji = ET.SubElement(wyciag_wiersz, "tns:DataOperacji")
  data_operacji.set("type", "etd:TData")
  data_operacji.text = jpk_operacja.data_operacji

  nazwa_podmiotu = ET.SubElement(wyciag_wiersz, "tns:NazwaPodmiotu")
  nazwa_podmiotu.set("type", "tns:TZnakowyJPK")
  nazwa_podmiotu.text = jpk_operacja.nazwa_podmiotu

  opis_operacji = ET.SubElement(wyciag_wiersz, "tns:OpisOperacji")
  opis_operacji.set("type", "tns:TZnakowyJPK")
  opis_operacji.text = jpk_operacja.opis_operacji

  kwota_operacji = ET.SubElement(wyciag_wiersz, "tns:KwotaOperacji")
  kwota_operacji.set("type", "tns:TKwotowy")
  kwota_operacji.text = "{:.2f}".format(jpk_operacja.kwota_operacji)

  saldo_operacji = ET.SubElement(wyciag_wiersz, "tns:SaldoOperacji")
  saldo_operacji.set("type", "tns:TKwotowy")
  saldo_operacji.text = "{:.2f}".format(jpk_operacja.saldo_operacji)

  n_wierszy += 1

#Dane kontrolne pliku JPK_WB
wyciag_ctrl = ET.SubElement(root, "tns:WyciagCtrl")

liczba_wierszy = ET.SubElement(wyciag_ctrl, "tns:LiczbaWierszy")
liczba_wierszy.set("type", "tns:TNaturalnyJPK")
liczba_wierszy.text = str(n_wierszy)

sumaObciazen = ET.SubElement(wyciag_ctrl, "tns:SumaObciazen")
sumaObciazen.set("type", "tns:TKwotowy")
sumaObciazen.text = "{:.2f}".format(suma_obciazen)

sumaUznan = ET.SubElement(wyciag_ctrl, "tns:SumaUznan")
sumaUznan.set("type", "tns:TKwotowy")
sumaUznan.text = "{:.2f}".format(suma_uznan)

#Zapis pliku JPK_WB
file_name = input("\nPodaj nazwę pliku XML, do którego zostanie zapisany wyciąg bankowy: ")
xmlstr = md.parseString(ET.tostring(root)).toprettyxml(indent="\t")
xmlstr_lines = xmlstr.splitlines(True)
xmlstr_lines = xmlstr_lines[1:]

if xmlstr_lines and xmlstr_lines[-1].endswith('\n'):
    xmlstr_lines[-1] = xmlstr_lines[-1].rstrip('\n')

# Zapisanie do pliku
with open(file_name + ".xml", "w", newline='', encoding='utf-8') as f:
  f.writelines(xmlstr_lines)

print("\nPlik JPK został pomyślnie utworzony")