import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class DataQuality:
    def __init__(self, df_path="C:/Users/fabio/Desktop/DNC/Desafios e bases/CarPrice_Assignment.csv"):
        self.df_path = df_path
        self.df = None
    
    def load_data(self):
        """Carrega o DataFrame usando a função Ler_DF"""
        self.df = Ler_DF(self.df_path)
        if self.df is not None:
            print("Dados carregados com sucesso!")
        else:
            print("Falha ao carregar os dados.")
    
    def unique_values(self):
        """Remove colunas com um único valor e imprime os valores únicos"""
        if self.df is not None:
            print("\nVerificando valores únicos...")
            self.df = valores_unicos(self.df)
        else:
            print("O DataFrame não foi carregado corretamente.")
    
    def numeric_columns(self):
        """Processa e retorna colunas numéricas"""
        if self.df is not None:
            print("\nProcessando colunas numéricas...")
            return cols_num(self.df)
        else:
            print("O DataFrame não foi carregado corretamente.")
    
    def non_numeric_columns(self):
        """Processa e imprime informações sobre colunas categóricas"""
        if self.df is not None:
            print("\nProcessando colunas não numéricas...")
            return cols_notnum(self.df)
        else:
            print("O DataFrame não foi carregado corretamente.")
    
    def run_analysis(self):
        """Executa o fluxo completo na ordem correta"""
        self.load_data()
        if self.df is not None:
            self.unique_values()
            df_num = self.numeric_columns()
            self.non_numeric_columns()
            print("\nAnálise de dados concluída.")
        else:
            print("Erro ao realizar a análise de dados.")

# Funções auxiliares
def Ler_DF(df_path):
    try:
        df1 = pd.read_csv(df_path)
        if not isinstance(df1, pd.DataFrame):
            raise ValueError("O objeto retornado não é um DataFrame.")
    except UnicodeDecodeError:
        try:
            df1 = pd.read_csv(df_path, encoding='latin', sep=';')
        except Exception as e:
            print(f"Erro ao ler o arquivo: {e}")
            return None
    except Exception as e:
        print(f"Erro: {e}")
        return None
    return df1

def valores_unicos(df1):
    del_cols = []
    for col in df1.columns:
        if df1[col].nunique() == 1:
            del_cols.append(col)            
            print(f'A coluna {col} possui um único valor: {df1[col].unique()[0]}')
    return df1.drop(columns=del_cols)

def cols_num(df1):
    df2 = pd.DataFrame()
    for col in df1.columns:
        df2[col] = pd.to_numeric(df1[col], errors='coerce')
        if df2[col].isna().all():
            df2.drop(columns=[col], inplace=True)
        else:
            df2[col].fillna(df2[col].mean(), inplace=True)
    
    df_num = df2.select_dtypes(include=['number'])
    
    for col in df_num.columns:
        plt.figure(figsize=(10, 6))
        df_num[col].plot(title=col, kind='line')
        plt.xlabel('Índice')
        plt.ylabel(col)
        plt.grid()
        plt.show()
    
    print("Correlação entre as colunas numéricas:")
    print(df_num.corr())  # Use print ao invés de display
    return df_num

def cols_notnum(df1):
    df2 = df1.select_dtypes(exclude='number').dropna(axis=1, how='all')
    for col in df2.columns:
        print(f'Distribuição percentual para a coluna {col}:')
        print(round((df2[col].value_counts(normalize=True) * 100), 2), '\n')
        print(f'Contagem dos valores para a coluna {col}:')
        print(df2[col].value_counts(), '\n')
        
        if len(df2[col].unique()) < 8:
            plt.figure(figsize=(10, 6))
            df2[col].value_counts().plot(kind='barh', title=f'Distribuição de {col}')
            plt.xlabel('Contagem')
            plt.ylabel(col)
            plt.grid()
            plt.show()
        else:
            print(f'Muitos valores a serem plotados. Existem {len(df2[col].unique())} valores únicos nessa coluna.')
    return df1

def plot_null_values(self):
    """Plota a quantidade de valores nulos em cada coluna."""
    if self.df is not None:
        null_counts = self.df.isnull().sum()
        plt.figure(figsize=(12, 6))
        null_counts[null_counts > 0].plot(kind='bar', color='skyblue')
        plt.title('Valores Nulos por Coluna')
        plt.xlabel('Colunas')
        plt.ylabel('Quantidade de Valores Nulos')
        plt.xticks(rotation=45)
        plt.grid(axis='y')
        plt.show()
    else:
        print("O DataFrame não foi carregado corretamente.")


