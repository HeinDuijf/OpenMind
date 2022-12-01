## Opmerkingen

- In de code werd de functie accuracy_information altijd aangeroepen met dezelfde
  waarde voor content_evaluation_right en content_evaluation_wrong. Dan kun je beter
  1 variabele weggooien uit de functie --> dat is minder complex.
- Bij functie figure_heatmap_source had je variabelen `save` en `filename`. Echter, die waren erg gelinkt. (Save=True, filename='') of (Save=False, filename='henkie.jpg') zouden rare inputs zijn. Het is nu vervangen naar 1 param: filename. Als die is gespecificeerd, dan slaan we op.
- In dezelfde functie stond het volgende pattern:

```python
    for x in range(len(index)):  # x ~ 0, 1, 2, 3, ..
        c = index[x]   # c ~ index[0], index[1], index[2], ..
        data[x] = f(c)
```

Dat is niet echt 'pythonic'. Het is leesbaarder om te gebruiken:

```python
    for x, c in enumerate(index):  # x ~ 0,1,2,3, c~index[0],index[1],index[2]
        data[x] = f(c)
```

- In dezelfde functie is het gebruik van namen `x, c, y, p, index, columns` niet echt inzichtelijk.
- In figuur added_accuracy_content staat complexe logica.
  Vond dat geen logische plek voor die logica.
- heatmap_style werd grotendeels herhaald in verschillende plot functies
- In `figure_heatmap_content_only` gebruik je `"variabele = " + str(var)`.
  Sinds een recente python update kun je dit schrijven als f-string:
  `f"variabele = {var}"`
- De functie `find_tipping_evaluation_content` heb ik ook in de ProbabilityCalculator
  gestopt. Ik twijfel zelf over deze implementatie. Het vervelende eraan vind ik dat
  er zogenaamde `side-effects` zijn. De functie geeft een output, maar de uitvoer van deze
  functie verandert ook de waarde van `self.probability_companion_right`. Zulke functies
  zijn gevaarlijk, omdat je soms niet in de gaten hebt dat deze side effects gebeuren.
  De functie meenemen in de klasse leverde wel een simplificatie op, omdat alle nodige
  parameters al in de klasse zaten. <br>
  Deze verplaatsing is bovendien niet goed gegaan: waarschijnlijk vanwege deze
  side effects.
- In `figure_individual_calculated_accuracy` geef je source_evaluative_capacity de
  standaardwaarde `None`, maar gooi je later een fout als deze niet is ingevuld. Beter
  zet je dan geen default.
- In dezelfde functie check je een input, en _print_ je `error: ....`. Als je niet wilt
  dat een bepaalde waarde wordt gebruikt, dan kun je beter een _error raisen_.
