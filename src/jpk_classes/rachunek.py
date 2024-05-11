class Rachunek:
  def __init__(self, nrrachunku, kod_waluty):
    self.nrrachunku = nrrachunku
    self.kod_waluty = kod_waluty

  def __str__(self):
    text = "Numer: " + str(self.nrrachunku) + "\n"
    text += "Kod waluty: " + str(self.kod_waluty) + "\n"

    return text