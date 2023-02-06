import streamlit as st
import pandas as pd
import xml.etree.ElementTree as et 
import plotly as px
from datetime import datetime


class aplicacao():
    def __init__(self):

        with st.sidebar:
            st.title("Curva ETTJ")

        st.title("Exercício curva ETTJ")

        path = r"C:\Users\felip\OneDrive\Área de Trabalho\Kinea\Curva ETTJ\PR230203\B3.xml"
        df = self.read_xml(path)
        
        tab1, tab2 = st.tabs(['Curva ETTJ', 'Tabela'])
    
        ettj1 = px.plot(df, x = "data_vencimento", y = "valor_ajuste_taxa",kind= 'line', title='Curva ETTJ')
        ettj2 = px.plot(df, x = "Ticker", y = "valor_ajuste_taxa", kind= 'line', title='Curva ETTJ por Ticker')
        
        with tab1:
            st.write(ettj1)
            st.write(ettj2)
        
        with tab2:
            st.dataframe(df)

    @st.cache
    def read_xml(self, path):
        xtree = et.parse(path)

        lista1 = []
        for elem in xtree.iter():
            if elem.tag == '{urn:bvmf.217.01.xsd}PricRpt':
                lista1.append(elem)
            
        lista = []
        for j, i in enumerate(lista1):
            j = i.find('{urn:bvmf.217.01.xsd}SctyId')
            for ticker in j:
                if ticker.text.find('DI1') == 0:
                    lista.append(i)

        contratos_em_aberto, n_negocios, contratos_negociados, volume_reais, valor_fechamento, valor_ajuste_taxa,valor_ajuste, preco_abertura, preco_minimo, preco_maximo, preco_medio = [],[],[],[],[],[],[],[],[],[],[]
        ticker, data = [], []
        for i in lista:
            fin= i.find('{urn:bvmf.217.01.xsd}FinInstrmAttrbts')
            try:
                contratos_em_aberto.append(fin.find('{urn:bvmf.217.01.xsd}RglrTxsQty').text)
                n_negocios.append(fin.find('{urn:bvmf.217.01.xsd}OpnIntrst').text)
                contratos_negociados.append(fin.find('{urn:bvmf.217.01.xsd}FinInstrmQty').text )
                volume_reais.append(fin.find('{urn:bvmf.217.01.xsd}NtlFinVol').text )
                valor_fechamento.append(fin.find('{urn:bvmf.217.01.xsd}LastPric').text )
                valor_ajuste_taxa.append(fin.find('{urn:bvmf.217.01.xsd}AdjstdQtTax').text )
                valor_ajuste.append(fin.find('{urn:bvmf.217.01.xsd}AdjstdQt').text )
                preco_abertura.append(fin.find('{urn:bvmf.217.01.xsd}FrstPric').text )
                preco_minimo.append(fin.find('{urn:bvmf.217.01.xsd}MinPric').text )
                preco_maximo.append(fin.find('{urn:bvmf.217.01.xsd}MaxPric').text )
                preco_medio.append(fin.find('{urn:bvmf.217.01.xsd}TradAvrgPric').text )
                
                a = i.find('{urn:bvmf.217.01.xsd}SctyId')
                for j in a:
                    ticker.append(j.text)
                
                data1 = [j.text for j in i.find('{urn:bvmf.217.01.xsd}TradDt')]
                data.append(data1)
            
            except: pass

        df = pd.DataFrame({"Data": data,
                "Ticker": ticker,
                "n_negocios": n_negocios,
                "contratos_em_aberto": contratos_em_aberto,
                "contratos_negociados": contratos_negociados,
                "volume_reais": volume_reais,
                "valor_fechamento":valor_fechamento,
                "valor_ajuste_taxa": valor_ajuste_taxa,
                "valor_ajuste": valor_ajuste,
                "preco_abertura":preco_abertura,
                "preco_minimo": preco_minimo,
                "preco_maximo":preco_maximo,
                "preco_medio":preco_medio
                })

        df.insert(0, "data_vencimento", df["Ticker"].apply(lambda x: self.conserta_ticker(x)))
        df = df.sort_values("data_vencimento", ascending= True)
        df.reset_index(drop = True, inplace=True)

        return df
    
    def conserta_ticker(self, val):
        mes = val[-3]
        dict = {'F': 1,'G': 2,'H': 3,'J': 4,'K':5 ,'M': 6,'N': 7,'Q': 8,'U': 9,'V': 10, 'X': 11,'Z': 12}
    
        data = f"{2000+int(val[-2:])}-{dict[mes]}-1"
        return datetime.strptime(data, '%Y-%m-%d')

aplicacao()



