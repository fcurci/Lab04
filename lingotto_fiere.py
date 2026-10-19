class Stand:
    def __init__(self, codice, superficie, padiglione, prezzo):
        self.codice_stand=codice
        self.superficie_stand=superficie
        self.padiglione_stand=padiglione
        self.prezzo_stand=float(prezzo)

        self.espositore_associato=None

    def __str__(self):
        if self.espositore_associato==None:
            return f"{self.codice_stand}: {self.superficie_stand} mq - Padiglione {self.padiglione_stand} - Prezzo {self.prezzo_stand:.2f}€ - Disponibile"
        else:
            return f"{self.codice_stand}: {self.superficie_stand} mq - Padiglione {self.padiglione_stand} - Prezzo {self.prezzo_stand:.2f}€ - Assegnato a {self.espositore_associato.codice_espositore}"

    def __lt__(self,other):
        return self.prezzo_stand<other.prezzo_stand

    def associazione(self,associato):
        self.espositore_associato=associato

class Prese(Stand):
    def __init__(self, codice, superficie, padiglione, prezzo, prese):
        super().__init__(codice, superficie, padiglione, prezzo)
        self.prese_stand=int(prese)

    def incremento_prezzo(self):
        self.prezzo_stand=self.prezzo_stand*(1+0.07*self.prese_stand)

    def __str__(self):
        if self.espositore_associato==None:
            return f"{self.codice_stand}: Prese extra | {self.superficie_stand} mq - Padiglione {self.padiglione_stand} - Prezzo {self.prezzo_stand:.2f}€ - Prese aggiuntive: {self.prese_stand} - Disponibile"
        else:
            return f"{self.codice_stand}: Prese extra | {self.superficie_stand} mq - Padiglione {self.padiglione_stand} - Prezzo {self.prezzo_stand:.2f}€ - Prese aggiuntive: {self.prese_stand} - Assegnato a {self.espositore_associato.codice_espositore}"

class Premium(Stand):
    def __init__(self, codice, superficie, padiglione, prezzo, tipo):
        super().__init__(codice, superficie, padiglione, prezzo)
        self.tipo_stand=tipo

    def incremento_prezzo(self):
        self.prezzo_stand=self.prezzo_stand*1.30

    def __str__(self):
        if self.espositore_associato==None:
            return f"{self.codice_stand}: Premium | {self.superficie_stand} mq - Padiglione {self.padiglione_stand} - Prezzo {self.prezzo_stand:.2f}€ - Posizione: {self.tipo_stand} - Disponibile"
        else:
            return f"{self.codice_stand}: Premium | {self.superficie_stand} mq - Padiglione {self.padiglione_stand} - Prezzo {self.prezzo_stand:.2f}€ - Posizione: {self.tipo_stand} - Assegnato a {self.espositore_associato.codice_espositore}"

class Espositore:
    def __init__(self, codice, nome, cognome):
        self.codice_espositore=codice
        self.nome_espositore=nome
        self.cognome_espositore=cognome

        self.stand_associato=None

    def __str__(self):
        if self.stand_associato==None:
            return f"{self.codice_espositore}: {self.nome_espositore} {self.cognome_espositore}"
        else:
            return f"{self.codice_espositore}: {self.nome_espositore} {self.cognome_espositore} - Associato a {self.stand_associato.codice_stand}"

    def __eq__(self,other):
        return isinstance(other, Espositore) and self.codice_espositore==other.codice_espositore
    def __lt__(self,other):
        return int(self.codice_espositore[2:])<int(other.codice_espositore[2:])

    def associazione(self,associato):
        self.stand_associato=associato


class LingottoFiere:
    def __init__(self, nome):
        self.nome_centro=nome
        self.lista_stand=[]
        self.lista_espositori=[]

    def carica_file_dati(self, file_path):

        f=open(file_path,"r",encoding="utf-8")
        line=f.readline()
        while line!="":
            el=line.strip().split(",")

            if el[0][:2]=="ST":
                if len(el)==4:
                    nuovo=Stand(el[0], el[1], el[2], el[3])
                else:
                    if el[4].isdigit():
                        nuovo=Prese(el[0], el[1], el[2], el[3], el[4])
                    else:
                        nuovo=Premium(el[0], el[1], el[2], el[3], el[4])

                    nuovo.incremento_prezzo()
                self.lista_stand.append(nuovo)

            if el[0][:2]=="ES":
                nuovo=Espositore(el[0], el[1], el[2])
                self.lista_espositori.append(nuovo)

            line=f.readline()

        f.close()

    def assegna_stand_a_espositore(self, codice_stand, codice_espositore):

        codice_stand=codice_stand[:2].strip().upper()+codice_stand[2:].strip()
        codice_espositore=codice_espositore[:2].strip().upper()+codice_espositore[2:].strip()

        stand_da_associare=None
        espositore_da_associare=None

        for stand in self.lista_stand:
            if stand.codice_stand==codice_stand:
                stand_da_associare=stand

        for espositore in self.lista_espositori:
            if espositore.codice_espositore==codice_espositore:
                espositore_da_associare=espositore

        if stand_da_associare!=None and espositore_da_associare!=None and stand_da_associare.espositore_associato==None and espositore_da_associare.stand_associato==None:
            stand_da_associare.associazione(espositore_da_associare)
            espositore_da_associare.associazione(stand_da_associare)

        else:
            raise Exception("Impossibile completare l'assegnazione")



    def elenca_espositori(self):
        return sorted(self.lista_espositori)


    def stand_ordinati_per_prezzo(self):
        return sorted(self.lista_stand)
