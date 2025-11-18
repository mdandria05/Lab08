import copy
from database.impianto_DAO import ImpiantoDAO

'''
    MODELLO:
    - Rappresenta la struttura dati
    - Si occupa di gestire lo stato dell'applicazione
    - Interagisce con il database
'''

class Model:
    def __init__(self):
        self._impianti = None
        self.load_impianti()

        self.__sequenza_ottima = []
        self.__costo_ottimo = -1

    def load_impianti(self):
        """ Carica tutti gli impianti e li setta nella variabile self._impianti """
        self._impianti = ImpiantoDAO.get_impianti()

    def get_consumo_medio(self, mese:int):
        """
        Calcola, per ogni impianto, il consumo medio giornaliero per il mese selezionato.
        :param mese: Mese selezionato (un intero da 1 a 12)
        :return: lista di tuple --> (nome dell'impianto, media), es. (Impianto A, 123)
        """
        # TODO
        lista_consumi_medi = []
        for impianto in self._impianti:
            impianto.get_consumi()
            lista_consumi = []
            for i in impianto.lista_consumi:
                if i.data.month == mese:
                    lista_consumi.append(i.kwh)
            media = sum(lista_consumi) / len(lista_consumi)
            lista_consumi_medi.append((impianto.nome, media))
        return lista_consumi_medi

    def get_sequenza_ottima(self, mese:int):
        """
        Calcola la sequenza ottimale di interventi nei primi 7 giorni
        :return: sequenza di nomi impianto ottimale
        :return: costo ottimale (cioè quello minimizzato dalla sequenza scelta)
        """
        self.__sequenza_ottima = []
        self.__costo_ottimo = -1
        consumi_settimana = self.__get_consumi_prima_settimana_mese(mese)
        self.__ricorsione([], 1, None, 0, consumi_settimana)
        # Traduci gli ID in nomi
        id_to_nome = {impianto.id: impianto.nome for impianto in self._impianti}
        sequenza_nomi = [f"Giorno {giorno}: {id_to_nome[i]}" for giorno, i in enumerate(self.__sequenza_ottima, start=1)]
        return sequenza_nomi, self.__costo_ottimo

    def __ricorsione(self, sequenza_parziale, giorno, ultimo_impianto, costo_corrente, consumi_settimana):
        """ Implementa la ricorsione """
        # TODO
        if len(sequenza_parziale) == 7:
            self.__sequenza_ottima = copy.deepcopy(sequenza_parziale)
            self.__costo_ottimo = costo_corrente
        else:
            for i in consumi_settimana.keys():
                sequenza_parziale.append(i)
                consumi_giorno = consumi_settimana[i]
                costo = costo_corrente + consumi_giorno[giorno - 1] if ultimo_impianto == sequenza_parziale[-1] or ultimo_impianto is None else costo_corrente + 5 + consumi_giorno[giorno - 1]
                if costo < self.__costo_ottimo or self.__costo_ottimo == -1:
                    self.__ricorsione(sequenza_parziale,giorno+1,sequenza_parziale[-1], costo, consumi_settimana)
                sequenza_parziale.pop()
    def __get_consumi_prima_settimana_mese(self, mese: int):
        """
        Restituisce i consumi dei primi 7 giorni del mese selezionato per ciascun impianto.
        :return: un dizionario: {id_impianto: [kwh_giorno1, ..., kwh_giorno7]}
        """
        # TODO
        consumi_settimana = {}
        for i in self._impianti:
            i.get_consumi()
            lista = []
            for c in i.lista_consumi:
                for g in range(1, 8):
                    if c.data.month == mese and c.data.day == g:
                        lista.append(c.kwh)
                consumi_settimana[i.id] = lista
        return consumi_settimana
