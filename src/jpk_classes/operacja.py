class Operacja:
  def __init__(self, data_operacji, nazwa_podmiotu, opis_operacji, kwota_operacji, saldo_operacji):
    self.data_operacji = data_operacji
    self.nazwa_podmiotu = nazwa_podmiotu
    self.opis_operacji = opis_operacji
    self.kwota_operacji = kwota_operacji
    self.saldo_operacji = saldo_operacji

  def __str__(self):
    text = "Data operacji: " + str(self.data_operacji) + "\n"
    text += "Nazwa podmiotu: " + str(self.nazwa_podmiotu) + "\n"
    text += "Opis operacji: " + str(self.opis_operacji) + "\n"
    text += "Kwota operacji: " + str(self.kwota_operacji) + "\n"
    text += "Saldo operacji: " + str(self.saldo_operacji) + "\n"

    return text