class Podmiot:
  def __init__(self, pelna_nazwa, nip, regon, kod_kraju, wojewodztwo, powiat, gmina, ulica, nrdomu, nrlokalu, miejscowosc, kod_pocztowy, poczta):
    self.pelna_nazwa = pelna_nazwa
    self.nip = nip
    self.regon = regon
    self.kod_kraju = kod_kraju
    self.wojewodztwo = wojewodztwo
    self.powiat = powiat
    self.gmina = gmina
    self.ulica = ulica
    self.nrdomu = nrdomu
    self.nrlokalu = nrlokalu
    self.miejscowosc = miejscowosc
    self.kod_pocztowy = kod_pocztowy
    self.poczta = poczta

  def __str__(self):
    text = "Pełna nazwa: " + str(self.pelna_nazwa) + "\n"
    text += "NIP: " + str(self.nip) + "\n"
    text += "REGON: " + str(self.regon) + "\n"
    text += "Kod kraju: " + str(self.kod_kraju) + "\n"
    text += "Wojewodztwo: " + str(self.wojewodztwo) + "\n"
    text += "Gmina: " + str(self.gmina) + "\n"
    text += "Ulica: " + str(self.ulica) + "\n"
    text += "Nr domu: " + str(self.nrdomu) + "\n"
    text += "Nr lokalu: " + str(self.nrlokalu) + "\n"
    text += "Miejscowosc: " + str(self.miejscowosc) + "\n"
    text += "Kod pocztowy: " + str(self.kod_pocztowy) + "\n"
    text += "Poczta: " + str(self.poczta)

    return text