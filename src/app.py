import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st


def load_data(path):
    data = pd.read_csv(path)
    return data

def comparing_graph(df_2019,df_2020,df_2021,causa,state="BRAZIL"):
    # 2019 dataset was updated and no covid cases are found. zero observations give error. To solve this proble, I added the try condition.
    
    if state == "BRAZIL":
        total_deaths_2019 = df_2019.groupby("tipo_doenca").sum()
        total_deaths_2020 = df_2020.groupby("tipo_doenca").sum()
        total_deaths_2021 = df_2021.groupby("tipo_doenca").sum()

        try: 
            lista = [int(total_deaths_2019.loc[causa]),
                    int(total_deaths_2020.loc[causa]),
                    int(total_deaths_2021.loc[causa])]
        except:
            lista = [0,
                    int(total_deaths_2020.loc[causa]),
                    int(total_deaths_2021.loc[causa])]
    else:
        total_deaths_2019 = df_2019.groupby(["uf","tipo_doenca"]).sum()
        total_deaths_2020 = df_2020.groupby(["uf","tipo_doenca"]).sum()
        total_deaths_2021 = df_2021.groupby(["uf","tipo_doenca"]).sum()

        try:

            lista = [int(total_deaths_2019.loc[state,causa]),
                    int(total_deaths_2020.loc[state,causa]),
                    int(total_deaths_2021.loc[state,causa])]
        except:
            lista = [int(0),
                    int(total_deaths_2020.loc[state,causa]),
                    int(total_deaths_2021.loc[state,causa])]
    
    data = pd.DataFrame({"Total" : lista,
                         "Year"  : [2019,2020,2021]})

    fig, ax = plt.subplots()
    ax = sns.barplot(x = "Year", y = "Total", data = data)
    ax.set_title(f"Deaths by {causa} - {state}")

    return fig



def main():
    #Variables
    deaths_2019 = load_data("data/raw/obitos-2019_Periodo_01012019_ate_31122019.csv")
    deaths_2020 = load_data("data/raw/obitos-2020_Periodo_01012020_ate_31122020.csv")
    deaths_2021 = load_data("data/raw/obitos-2021_Periodo_01012021_ate_19032021.csv")
    states = np.append("BRAZIL", deaths_2020.uf.unique())
    dis_eng = {"OUTRAS" : "OTHER","COVID" : "COVID","INDETERMINADA" : "NOT DETERMINED","INSUFICIENCIA_RESPIRATORIA" : "RESPIRATORY FAILURE","PNEUMONIA" : "PNEUMONIA","SEPTICEMIA" : "SEPTICEMIA","SRAG" : "SARS"}
    list_key_dis_PT = list(dis_eng.keys())
    list_val_dis_EN = list(dis_eng.values())

    st.title("My first application")
    st.markdown("This project analyse the data related to deaths on Brazil in the period from 2019 to 2021")
    
    option_disease = st.selectbox("Select disease type:",list_val_dis_EN)
    option_disease_position = list_val_dis_EN.index(option_disease)
    option_disease_selected = list_key_dis_PT[option_disease_position]

    option_state = st.selectbox("Select the state:",
                states)

    image = comparing_graph(deaths_2019,deaths_2020,deaths_2021,
                            option_disease_selected,option_state)
    st.pyplot(image)


if __name__ == "__main__":
    main()

