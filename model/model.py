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
        self.__sequenza_ottima.sort(key=lambda x: x[1])
        self.__costo_ottimo = self.__sequenza_ottima[0][1]
        self.__sequenza_ottima = self.__sequenza_ottima[0][0]
        # Traduci gli ID in nomi
        id_to_nome = {impianto.id: impianto.nome for impianto in self._impianti}
        sequenza_nomi = [f"Giorno {giorno}: {id_to_nome[i]}" for giorno, i in enumerate(self.__sequenza_ottima, start=1)]
        return sequenza_nomi, self.__costo_ottimo

    def __ricorsione(self, sequenza_parziale, giorno, ultimo_impianto, costo_corrente, consumi_settimana):
        """ Implementa la ricorsione """
        # TODO
        if len(sequenza_parziale) == 7:
            self.__sequenza_ottima.append((sequenza_parziale,costo_corrente))
            return None
        else:
            seq_p_a = list(sequenza_parziale)
            seq_p_b = list(sequenza_parziale)
            seq_p_a.append(1)
            seq_p_b.append(2)
            costo_corrente_a = costo_corrente + consumi_settimana[1][giorno - 1] if ultimo_impianto == seq_p_a[-1] or ultimo_impianto is None else costo_corrente + 5 + consumi_settimana[1][giorno - 1]
            costo_corrente_b = costo_corrente + consumi_settimana[2][giorno - 1] if ultimo_impianto == seq_p_b[-1] or ultimo_impianto is None else costo_corrente + 5 + consumi_settimana[2][giorno - 1]
            giorno += 1
            self.__ricorsione(seq_p_a,giorno,seq_p_a[-1],costo_corrente_a,consumi_settimana)
            self.__ricorsione(seq_p_b,giorno,seq_p_b[-1],costo_corrente_b,consumi_settimana)

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
                for g in range(1,8):
                    if c.data.month == mese and c.data.day == g:
                        lista.append(c.kwh)
                consumi_settimana[i.id]=lista
        return consumi_settimana
