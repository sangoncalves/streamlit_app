import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def load_data(path):
    data = pd.read_csv(path)
    return data

def comparing_graph(df_2019,df_2020,df_2021,causa,state="BRASIL"):
    if state == "BRASIL":
        total_deaths_2019 = df_2019.groupby("tipo_doenca").sum()
        total_deaths_2020 = df_2020.groupby("tipo_doenca").sum()
        total_deaths_2021 = df_2021.groupby("tipo_doenca").sum()
        lista = [int(total_deaths_2019.loc[causa]),int(total_deaths_2020.loc[causa])]
    else:
        total_deaths_2019 = df_2019.groupby(["uf","tipo_doenca"]).sum()
        total_deaths_2020 = df_2020.groupby(["uf","tipo_doenca"]).sum()
        total_deaths_2021 = df_2021.groupby(["uf","tipo_doenca"]).sum()
        lista = [int(total_deaths_2019.loc[state,causa]),int(total_deaths_2020.loc[state,causa])]
    data = pd.DataFrame({"Total" : lista,
                         "Year"  : [2019,2020]})

    # plt.figure(figsize=(8,6))
    sns.barplot(x = "Year", y = "Total", data = data)
    # plt.title(f"Deaths by {causa} - {state}")
    # plt.show()

def main():
    #Variables
    deaths_2019 = load_data("data/raw/obitos-2019_Periodo_01012019_ate_31122019.csv")
    deaths_2020 = load_data("data/raw/obitos-2020_Periodo_01012020_ate_31122020.csv")
    deaths_2021 = load_data("data/raw/obitos-2021_Periodo_01012021_ate_19032021.csv")
    image = comparing_graph(deaths_2019,deaths_2020,deaths_2021,"SRAG")
    
    st.title("My first application")
    st.markdown("This project analyse the data related to deaths on Brazil in the period from 2019 to 2021")
    st.pyplot(image)
    #Presenting Data
    #st.dataframe(df_2019)

if __name__ == "__main__":
    main()