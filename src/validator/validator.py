import re
from datetime import datetime

import numpy as np


def is_date_correct(data, format="%Y-%m-%d"):
    try:
        datetime.strptime(data, format)
        return True
    except (ValueError, TypeError):
        return False


def check_podmiot_columns(df_podmiot):
    columns = ['PelnaNazwa', 'NIP', 'REGON', 'KodKraju', 'Wojewodztwo', 'Powiat', 'Gmina', 'Ulica', 'NrDomu',
               'NrLokalu', 'Miejscowosc', 'KodPocztowy', 'Poczta']
    df_columns = list(df_podmiot.columns)
    return df_columns == columns


def check_rachunek_columns(df_rachunek):
    columns = ['NumerRachunku', 'KodWaluty']
    df_columns = list(df_rachunek.columns)
    return columns == df_columns


def check_operacje_columns(df_operacje):
    columns = ['DataOperacji', 'NazwaPodmiotu', 'OpisOperacji', 'KwotaOperacji', 'SaldoOperacji']
    df_columns = list(df_operacje.columns)
    return df_columns == columns


def is_one_row(df):
    return df.shape[0] == 1


def validate_dataframes(df_podmiot, df_rachunek, df_operacje):
    if not check_podmiot_columns(df_podmiot):
        print("Plik CSV z danymi podmiotu nie zawiera poprawnych kolumn.")
        return 1

    if not check_rachunek_columns(df_rachunek):
        print("Plik CSV z danymi rachunku bankowego nie zawiera poprawnych kolumn.")
        return 1

    if not check_operacje_columns(df_operacje):
        print("Plik CSV z danymi operacji bankowych nie zawiera poprawnych kolumn.")
        return 1

    if not is_one_row(df_podmiot):
        print("Plik CSV z danymi podmiotu zawiera dane więcej niż jednego podmiotu.")
        return 1

    if not is_one_row(df_rachunek):
        print("Plik CSV z danymi rachunku bankowego zawiera dane więcej niż jednego rachunku bankowego.")
        return 1
    
    return 0


def is_not_empty_str(mystr):
    return isinstance(mystr, str) and mystr != ""


def is_nip_correct(nip):
    return isinstance(nip, str) and re.fullmatch(r'\d{3}-\d{3}-\d{2}-\d{2}', nip)


def is_regon_correct(regon):
    return isinstance(regon, str) and (re.fullmatch(r"^\d{2} \d{6} \d$", regon) or re.fullmatch(r"^\d{2} \d{6} \d{1} \d{4} \d{1}$", regon) or regon == "")


def is_cc_correct(kod_kraju):
    return kod_kraju.upper() == "PL"


def is_wojewodztwo_correct(wojewodztwo):
    wojewodztwa = [
        'dolnośląskie',
        'kujawsko-pomorskie',
        'lubelskie',
        'lubuskie',
        'łódzkie',
        'małopolskie',
        'mazowieckie',
        'opolskie',
        'podkarpackie',
        'podlaskie',
        'pomorskie',
        'śląskie',
        'świętokrzyskie',
        'warmińsko-mazurskie',
        'wielkopolskie',
        'zachodniopomorskie'
    ]
    return wojewodztwo.lower() in wojewodztwa


def is_adres_element_correct(element):
    return isinstance(element, str) and re.fullmatch(r"[a-zA-ZąćęłńóśźżĄĆĘŁŃÓŚŻŹ\s]+", element)


def is_nrdomu_correct(nrdomu):
    return isinstance(nrdomu, np.int64) or isinstance(nrdomu, str) and re.fullmatch(r"^\d+[a-zA-Z]?$", nrdomu)


def is_nrlokalu_correct(nrlokalu):
    return isinstance(nrlokalu, np.int64) or nrlokalu == ""


def is_kod_pocztowy_correct(kod_pocztowy):
    return isinstance(kod_pocztowy, str) and re.fullmatch(r"^\d{2}-\d{3}$", kod_pocztowy)


def validate_podmiot_values(jpk_podmiot):
    if not is_not_empty_str(jpk_podmiot.pelna_nazwa):
        print("Niepoprawna pełna nazwa podmiotu.")
        return 1

    if not is_nip_correct(jpk_podmiot.nip):
        print("Niepoprawny NIP podmiotu.")
        return 1

    if not is_regon_correct(jpk_podmiot.regon):
        print("Niepoprawny REGON podmiotu.")
        return 1

    if not is_cc_correct(jpk_podmiot.kod_kraju):
        print("Aplikacja nie obsługuje podmiotów z innych krajów niż Polska (PL).")
        return 1

    if not is_wojewodztwo_correct(jpk_podmiot.wojewodztwo):
        print("Niepoprawne województwo podmiotu.")
        return 1

    if not is_adres_element_correct(jpk_podmiot.powiat):
        print("Nieprawidłowa nazwa powiatu podmiotu.")
        return 1

    if not is_adres_element_correct(jpk_podmiot.gmina):
        print("Nieprawidłowa nazwa gminy podmiotu.")
        return 1

    if not is_not_empty_str(jpk_podmiot.ulica):
        print("Nieprawidłowa nazwa ulicy podmiotu.")
        return 1

    if not is_nrdomu_correct(jpk_podmiot.nrdomu):
        print("Nieprawidłowy numer domu podmiotu.")
        return 1

    if not is_nrlokalu_correct(jpk_podmiot.nrlokalu):
        print("Nieprawidłowy numer lokalu podmiotu.")
        return 1

    if not is_adres_element_correct(jpk_podmiot.miejscowosc):
        print("Nieprawidłowa nazwa miejscowości podmiotu.")
        return 1

    if not is_kod_pocztowy_correct(jpk_podmiot.kod_pocztowy):
        print("Nieprawidłowy kod pocztowy podmiotu.")
        return 1

    if not is_adres_element_correct(jpk_podmiot.poczta):
        print("Nieprawidłowa nazwa poczty podmiotu.")
        return 1

    return 0


def is_nrrachunku_correct(nrrachunku):
    return isinstance(nrrachunku, str) and re.fullmatch(r"^\d{2} \d{4} \d{4} \d{4} \d{4} \d{4} \d{4}$", nrrachunku)


def is_waluta_correct(kod_waluty):
    waluty = ["PLN", "EUR", "CHF", "USD"]
    return kod_waluty.upper() in waluty


def validate_rachunek_values(jpk_rachunek):
    if not is_nrrachunku_correct(jpk_rachunek.nrrachunku):
        print("Nieprawidłowy numer rachunku.")
        return 1

    if not is_waluta_correct(jpk_rachunek.kod_waluty):
        print("Nieobsługiwana waluta. Program obsługuje PLN, EUR, USD i CHF.")
        return 1

    return 0


def is_not_empty(a):
    return isinstance(a, np.int64) or isinstance(a, str) and a != ""


def is_money_amount_correct(amount):
    try:
        amount = float(amount)
    except ValueError:
        return False

    return round(amount, 2) == amount


def validate_operacje_values(jpk_operacje):
    for jpk_operacja in jpk_operacje:
        if not is_date_correct(jpk_operacja.data_operacji):
            print("Niepoprawna data operacji w następującej operacji:")
            print(jpk_operacja)
            return 1

        if not is_not_empty(jpk_operacja.nazwa_podmiotu):
            print("Brak nazwy podmiotu w następującej operacji:")
            print(jpk_operacja)
            return 1

        if not is_not_empty(jpk_operacja.opis_operacji):
            print("Brak opisu operacji w następującej operacji:")
            print(jpk_operacja)
            return 1

        if not is_money_amount_correct(jpk_operacja.kwota_operacji):
            print("Niepoprawna kwota operacji w następującej operacji:")
            print(jpk_operacja)
            return 1

        if not is_money_amount_correct(jpk_operacja.saldo_operacji):
            print("Niepoprawna kwota operacji w następującej operacji:")
            print(jpk_operacja)
            return 1

    return 0


def validate_kod_urzedu(kod_urzedu):
    try:
        kod_urzedu = int(kod_urzedu)
    except ValueError:
        return 1

    if not re.fullmatch(r"^\d{4}$", str(kod_urzedu)):
        return 1

    return 0