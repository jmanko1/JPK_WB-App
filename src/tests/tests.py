import unittest

import numpy as np
import pandas as pd

from src.validator.validator import is_date_correct, check_podmiot_columns, check_rachunek_columns, check_operacje_columns, \
    is_one_row, is_not_empty_str, is_nip_correct, is_regon_correct, is_cc_correct, is_wojewodztwo_correct, \
    is_adres_element_correct, is_nrdomu_correct, is_nrlokalu_correct, is_kod_pocztowy_correct, is_nrrachunku_correct, \
    is_waluta_correct, is_not_empty, is_money_amount_correct, validate_kod_urzedu


class TestIsDateCorrect(unittest.TestCase):
    #Prawidłowa data w formacie rok-miesiąc-dzień - True
    def test_valid_date(self):
        self.assertTrue(is_date_correct("2024-05-11"))

    #Data w formacie rok-dzień-miesiąc - False
    def test_invalid_date(self):
        self.assertFalse(is_date_correct("2024-30-02"))

    #Dzień, miesiąc i rok nieoddzielone od siebie - False
    def test_custom_format(self):
        self.assertFalse(is_date_correct(11052024))

    #Data w formacie rok/miesiąc/dzień - False
    def test_invalid_format(self):
        self.assertFalse(is_date_correct("2024/05/11"))


class TestCheckPodmiotColumns(unittest.TestCase):
    #Pasujące kolumny - True
    def test_matching_columns(self):
        my_columns = ['PelnaNazwa', 'NIP', 'REGON', 'KodKraju', 'Wojewodztwo', 'Powiat', 'Gmina', 'Ulica',
                            'NrDomu', 'NrLokalu', 'Miejscowosc', 'KodPocztowy', 'Poczta']
        df = pd.DataFrame(columns=my_columns)
        self.assertTrue(check_podmiot_columns(df))

    #Brak jednej kolumny - False
    def test_non_matching_columns(self):
        my_columns = ['PelnaNazwa', 'NIP', 'REGON', 'KodKraju', 'Wojewodztwo', 'Powiat', 'Gmina', 'Ulica',
                            'NrDomu', 'NrLokalu', 'Miejscowosc', 'KodPocztowy']
        df = pd.DataFrame(columns=my_columns)
        self.assertFalse(check_podmiot_columns(df))

    #Dodatkowa kolumna - False
    def test_extra_columns(self):
        my_columns = ['PelnaNazwa', 'NIP', 'REGON', 'KodKraju', 'Wojewodztwo', 'Powiat', 'Gmina', 'Ulica',
                            'NrDomu', 'NrLokalu', 'Miejscowosc', 'KodPocztowy', 'Poczta', 'DodatkowaKolumna']
        df = pd.DataFrame(columns=my_columns)
        self.assertFalse(check_podmiot_columns(df))


class TestCheckRachunekColumns(unittest.TestCase):
    #Odpowiednie kolumny - True
    def test_matching_columns(self):
        my_columns = ['NumerRachunku', 'KodWaluty']
        df = pd.DataFrame(columns=my_columns)
        self.assertTrue(check_rachunek_columns(df))

    #Brak jednej kolumny - False
    def test_non_matching_columns(self):
        my_columns = ['NumerRachunku']
        df = pd.DataFrame(columns=my_columns)
        self.assertFalse(check_rachunek_columns(df))

    #Dodatkowa kolumna - False
    def test_extra_columns(self):
        my_columns = ['NumerRachunku', 'KodWaluty', 'DodatkowaKolumna']
        df = pd.DataFrame(columns=my_columns)
        self.assertFalse(check_rachunek_columns(df))


class TestIsOneRow(unittest.TestCase):
    #Jeden wiersz - True
    def test_single_row(self):
        df = pd.DataFrame({'A': [1], 'B': [2]})
        self.assertTrue(is_one_row(df))

    #Wiele wierszy - False
    def test_multiple_rows(self):
        df = pd.DataFrame({'A': [1, 2], 'B': [2, 3]})
        self.assertFalse(is_one_row(df))

    #Brak wierszy - False
    def test_empty_dataframe(self):
        df = pd.DataFrame(columns=['A', 'B'])
        self.assertFalse(is_one_row(df))


class TestCheckOperacjeColumns(unittest.TestCase):
    #Odpowiednie kolumny - True
    def test_matching_columns(self):
        my_columns = ['DataOperacji', 'NazwaPodmiotu', 'OpisOperacji', 'KwotaOperacji', 'SaldoOperacji']
        df = pd.DataFrame(columns=my_columns)
        self.assertTrue(check_operacje_columns(df))

    #Brak jednej kolumny - False
    def test_non_matching_columns(self):
        my_columns = ['DataOperacji', 'NazwaPodmiotu', 'OpisOperacji', 'KwotaOperacji']
        df = pd.DataFrame(columns=my_columns)
        self.assertFalse(check_operacje_columns(df))

    #Dodatkowa kolumna - False
    def test_extra_columns(self):
        my_columns = ['DataOperacji', 'NazwaPodmiotu', 'OpisOperacji', 'KwotaOperacji', 'SaldoOperacji', 'DodatkowaKolumna']
        df = pd.DataFrame(columns=my_columns)
        self.assertFalse(check_operacje_columns(df))


class TestIsNotEmptyStr(unittest.TestCase):
    #Niepusty string - True
    def test_non_empty_string(self):
        self.assertTrue(is_not_empty_str("Hello"))

    #Pusty string - False
    def test_empty_string(self):
        self.assertFalse(is_not_empty_str(""))

    #Zmienna, która nie jest stringiem - False
    def test_non_string_input(self):
        self.assertFalse(is_not_empty_str(123))


class TestIsNIPCorrect(unittest.TestCase):
    #Prawidłowy NIP - True
    def test_valid_nip(self):
        self.assertTrue(is_nip_correct("123-456-32-18"))

    #Nieprawidłowy NIP (za dużo cyfr) - False
    def test_invalid_nip(self):
        self.assertFalse(is_nip_correct("123-456-32-189"))

    #Zmienna, która nie jest stringiem - False
    def test_non_string_input(self):
        self.assertFalse(is_nip_correct(123))

    #NIP prawidłowy ale bez myślników - False
    def test_non_dash_format(self):
        self.assertFalse(is_nip_correct("1234563218"))

    #NIP z odpowiednią liczbą cyfr, ale są one źle oddzielone myślnikami - False
    def test_incorrect_length(self):
        self.assertFalse(is_nip_correct("12-3456-321-8"))


class TestIsREGONCorrect(unittest.TestCase):
    #Prawidłowy REGON - True
    def test_valid_regon1(self):
        self.assertTrue(is_regon_correct("12 345678 9"))

    #Prawidłowy REGON - True
    def test_valid_regon2(self):
        self.assertTrue(is_regon_correct("12 345678 9 1234 5"))

    #Prawidłowy REGON ale bez spacji - False
    def test_valid_regon_without_spaces(self):
        self.assertFalse(is_regon_correct("123456789"))

    #Nieprawidłowy REGON (nieodpowiednia liczba cyfr) - False
    def test_invalid_regon(self):
        self.assertFalse(is_regon_correct("1234567890"))

    #Zmienna, która nie jest stringiem - False
    def test_non_string_input(self):
        self.assertFalse(is_regon_correct(123))

    #Brak REGON - True
    def test_empty_string(self):
        self.assertTrue(is_regon_correct(""))


class TestIsCCCorrect(unittest.TestCase):
    #Prawidłowy kod kraju - True
    def test_valid_cc(self):
        self.assertTrue(is_cc_correct("PL"))

    #Kod kraju inny niż polski - False
    def test_invalid_cc(self):
        self.assertFalse(is_cc_correct("US"))

    #Prawidłowy kod kraju zapisany małymi literami - True
    def test_lower_case_cc(self):
        self.assertTrue(is_cc_correct("pl"))

    #Prawidłowy kod kraju zapisany małymi i wielkimi literami - True
    def test_mixed_case_cc(self):
        self.assertTrue(is_cc_correct("Pl"))


class TestIsWojewodztwoCorrect(unittest.TestCase):
    #Prawidłowe województwo - True
    def test_valid_wojewodztwo(self):
        self.assertTrue(is_wojewodztwo_correct("małopolskie"))

    #Nieprawidłowe województwo - False
    def test_invalid_wojewodztwo(self):
        self.assertFalse(is_wojewodztwo_correct("lubusk"))

    #Prawidłowe województwo zapisane wielkimi literami - True
    def test_upper_case_wojewodztwo(self):
        self.assertTrue(is_wojewodztwo_correct("MAŁOPOLSKIE"))

    #Prawidłowe województwo zapisane wielkimi i małymi literami - True
    def test_mixed_case_wojewodztwo(self):
        self.assertTrue(is_wojewodztwo_correct("MaŁoPoLsKiE"))


class TestIsAdresElementCorrect(unittest.TestCase):
    #Poprawny element adresu - True
    def test_valid_element(self):
        self.assertTrue(is_adres_element_correct("Kazimierz Dolny"))

    #Nieprawidłowy element adresu - False
    def test_invalid_element(self):
        self.assertFalse(is_adres_element_correct("Kazimierz123"))

    #Zmienna, która nie jest stringiem - False
    def test_non_string_input(self):
        self.assertFalse(is_adres_element_correct(123))

    #Pusty string - False
    def test_empty_string(self):
        self.assertFalse(is_adres_element_correct(""))

    #Poprawny lement adresu z polskimi literami - True
    def test_special_characters(self):
        self.assertTrue(is_adres_element_correct("Pruszków"))


class TestIsNrdomuCorrect(unittest.TestCase):
    #Liczba całkowita - True
    def test_valid_nrdomu_int(self):
        self.assertTrue(is_nrdomu_correct(np.int64(10)))

    #Numer domu w postaci xy, gdzie x to liczba, a y to wielka litera - True
    def test_valid_nrdomu_str(self):
        self.assertTrue(is_nrdomu_correct("10A"))

    #Numer domu w postaci xy, gdzie x to liczba, a y to mała litera - True
    def test_valid_nrdomu_str2(self):
        self.assertTrue(is_nrdomu_correct("10a"))

    #Nieprawidłowy numer domu - False
    def test_invalid_nrdomu(self):
        self.assertFalse(is_nrdomu_correct("10Aa"))

    #Liczba zmiennoprzecinkowa - False
    def test_non_string_or_int_input(self):
        self.assertFalse(is_nrdomu_correct(10.5))

    #Pusty string - False
    def test_empty_string(self):
        self.assertFalse(is_nrdomu_correct(""))


class TestIsNrLokaluCorrect(unittest.TestCase):
    #Liczba całkowita - True
    def test_valid_nrlokalu_int(self):
        self.assertTrue(is_nrlokalu_correct(np.int64(10)))

    #Pusty numer lokalu - True
    def test_empty_nrlokalu(self):
        self.assertTrue(is_nrlokalu_correct(""))

    #String - False
    def test_invalid_nrlokalu(self):
        self.assertFalse(is_nrlokalu_correct("A"))

    #Liczba zmiennoprzecinkowa - False
    def test_non_string_or_int_input(self):
        self.assertFalse(is_nrlokalu_correct(10.5))


class TestIsKodPocztowyCorrect(unittest.TestCase):
    #Prawidłowy kod pocztowy - True
    def test_valid_kod_pocztowy(self):
        self.assertTrue(is_kod_pocztowy_correct("12-345"))

    #Nieprawidłowy kod pocztowy - False
    def test_invalid_kod_pocztowy(self):
        self.assertFalse(is_kod_pocztowy_correct("123-456"))

    #Zmienna, która nie jest stringiem - False
    def test_non_string_input(self):
        self.assertFalse(is_kod_pocztowy_correct(123))

    #Pusty string - False
    def test_empty_string(self):
        self.assertFalse(is_kod_pocztowy_correct(""))

    #Kod pocztowy bez myślnika - False
    def test_invalid_format(self):
        self.assertFalse(is_kod_pocztowy_correct("12345"))


class TestIsNrRachunkuCorrect(unittest.TestCase):
    #Prawidłowy numer rachunku - True
    def test_valid_nr_rachunku(self):
        self.assertTrue(is_nrrachunku_correct("12 3456 7890 1234 5678 9012 3456"))

    #Nieprawidłowy numer - False
    def test_invalid_nr_rachunku(self):
        self.assertFalse(is_nrrachunku_correct("123 456 7890 1234 5678 9012 3456"))

    #Zmienna, która nie jest stringiem - False
    def test_non_string_input(self):
        self.assertFalse(is_nrrachunku_correct(123))

    #Pusty string - False
    def test_empty_string(self):
        self.assertFalse(is_nrrachunku_correct(""))


class TestIsWalutaCorrect(unittest.TestCase):
    #Prawidłowa waluta - True
    def test_valid_waluta(self):
        self.assertTrue(is_waluta_correct("PLN"))

    #Nieprawidłowa waluta - False
    def test_invalid_waluta(self):
        self.assertFalse(is_waluta_correct("GBP"))

    #Prawidłowa waluta zapisana małymi literami - True
    def test_lower_case_waluta(self):
        self.assertTrue(is_waluta_correct("eur"))

    #Prawidłowa waluta zapisana małymi i wielkimi literami - True
    def test_mixed_case_waluta(self):
        self.assertTrue(is_waluta_correct("ChF"))


class TestIsNotEmpty(unittest.TestCase):
    #Niepusty string - True
    def test_not_empty_string(self):
        self.assertTrue(is_not_empty("Hello"))

    #Pusty string - False
    def test_empty_string(self):
        self.assertFalse(is_not_empty(""))

    #Liczba całkowita - True
    def test_non_string_input(self):
        self.assertTrue(is_not_empty(np.int64(123)))

    #Tablica - False
    def test_non_empty_list(self):
        self.assertFalse(is_not_empty([1, 2, 3]))

    #Pusta tablica - False
    def test_empty_list(self):
        self.assertFalse(is_not_empty([]))


class TestIsMoneyAmountCorrect(unittest.TestCase):
    #Prawidłowa kwota pieniężna - True
    def test_valid_amount(self):
        self.assertTrue(is_money_amount_correct("10.50"))

    #Nieprawidłowa kwota pieniężna - False
    def test_invalid_amount(self):
        self.assertFalse(is_money_amount_correct(10.555))

    #Nienumeryczny string - False
    def test_non_numeric_input(self):
        self.assertFalse(is_money_amount_correct("abc"))

    #Liczba całkowita - True
    def test_integer_amount(self):
        self.assertTrue(is_money_amount_correct(10))

    #Prawidłowa ujemna kwota - True
    def test_negative_amount(self):
        self.assertTrue(is_money_amount_correct(-10.50))

    #Zero w stringu - True
    def test_zero_amount(self):
        self.assertTrue(is_money_amount_correct("0"))


class TestValidateKodUrzedu(unittest.TestCase):
    #Prawidłowy kod urzędu - 0
    def test_valid_kod_urzedu(self):
        self.assertEqual(validate_kod_urzedu("1234"), 0)

    #Nieprawidłowy kod urzędu - 1
    def test_invalid_format_kod_urzedu(self):
        self.assertEqual(validate_kod_urzedu(12345), 1)

    #Nienumeryczna wartość - 1
    def test_non_numeric_input(self):
        self.assertEqual(validate_kod_urzedu("abc"), 1)

    #Pusty string - 1
    def test_empty_input(self):
        self.assertEqual(validate_kod_urzedu(""), 1)


if __name__ == '__main__':
    unittest.main()