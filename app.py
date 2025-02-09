import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configuração da página
st.set_page_config(page_title="Análise Climática", layout="wide")

# Carregar os dados
def load_data():
    df = pd.read_csv("https://raw.githubusercontent.com/MarceloMFerreira/archives/refs/heads/main/tempo_final.csv")
    df["Data"] = pd.to_datetime(df["Data"])
    return df

df = load_data()

st.title("📊 Análise de Dados Meteorológicos")

# Seleção de cidades
cidades = st.multiselect("Selecione as cidades:", df["Cidade"].unique(), default=df["Cidade"].unique())
df_filtered = df[df["Cidade"].isin(cidades)]

# Função para gerar histórias de clima
def generate_stories(df):
    df["Data"] = df["Data"].dt.strftime('%Y-%m-%d')
    stories = []
    
    for _, row in df.iterrows():
        story = ""
        
        if row["Temp_Max"] > 30:
            if "Chuva" in row["Condicao"]:
                story = f"Hoje, {row['Cidade']} está muito quente, com grandes chances de chuva, tornando o dia desconfortável."
            elif "Nublado" in row["Condicao"]:
                story = f"Em {row['Cidade']}, o calor excessivo combinado com o tempo nublado pode tornar o clima abafado e desconfortável."
            else:
                story = f"Hoje, {row['Cidade']} está bastante quente, ideal para atividades externas."
        
        elif 18 <= row["Temp_Max"] <= 26:
            if "Chuva" in row["Condicao"]:
                story = f"{row['Cidade']} tem uma temperatura agradável, mas a chuva pode atrapalhar atividades ao ar livre."
            elif "Nublado" in row["Condicao"]:
                story = f"{row['Cidade']} tem uma temperatura agradável, mas o céu nublado pode tornar as caminhadas menos agradáveis."
            else:
                story = f"{row['Cidade']} tem um clima perfeito para caminhadas ao ar livre."
        
        elif row["Temp_Max"] < 18:
            if "Chuva" in row["Condicao"]:
                story = f"Em {row['Cidade']}, a temperatura baixa e a chuva forte tornam o dia desconfortável."
            elif row["Condicao"] == "Neve":
                story = f"{row['Cidade']} está com temperatura baixa e neve, ideal para quem gosta de atividades de inverno."
            else:
                story = f"{row['Cidade']} tem um clima ameno, ótimo para relaxar em ambientes fechados."
        
        if not story:
            story = f"O clima em {row['Cidade']} hoje é {row['Condicao']}, com temperatura máxima de {row['Temp_Max']}°C."
        
        stories.append(story)
    
    return stories

# Gerando as histórias
stories = generate_stories(df_filtered)
df_filtered['História Climática'] = stories

# Sidebar para seleção dos gráficos
st.sidebar.header("Selecione os gráficos a serem exibidos")
show_temp_max_min = st.sidebar.checkbox("Temperatura Máxima e Mínima", True)
show_evolucao = st.sidebar.checkbox("Evolução da Temperatura Mínima", True)
show_precip = st.sidebar.checkbox("Precipitação", True)
show_temp_max = st.sidebar.checkbox("Temperatura Máxima", True)
show_temp_min = st.sidebar.checkbox("Temperatura Mínima", True)

# Exibindo a tabela interativa com as histórias
st.subheader("📅 Tabela de Dados Climáticos por Data e Cidade")
st.dataframe(df_filtered[['Data', 'Cidade', 'Temp_Max', 'Temp_Min', 'Precipitacao', 'Condicao', 'História Climática']], use_container_width=True)

# Gráficos de Análise
if show_temp_max_min:
    st.subheader("Temperatura Máxima por Data e Cidade")
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.lineplot(data=df_filtered, x="Data", y="Temp_Max", hue="Cidade", marker="o", ax=ax)
    plt.title("Evolução da Temperatura Máxima")
    plt.xlabel("Data")
    plt.ylabel("Temp Max (°C)")
    plt.xticks(rotation=45)
    st.pyplot(fig)

if show_evolucao:
    st.subheader("Temperatura Mínima por Data e Cidade")
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.lineplot(data=df_filtered, x="Data", y="Temp_Min", hue="Cidade", marker="o", linestyle="dashed", ax=ax)
    plt.title("Evolução da Temperatura Mínima")
    plt.xlabel("Data")
    plt.ylabel("Temp Min (°C)")
    plt.xticks(rotation=45)
    st.pyplot(fig)

if show_precip:
    st.subheader("Precipitação por Cidade e Data")
    df_pivot_precip = df_filtered.pivot_table(values="Precipitacao", index="Cidade", columns="Data", aggfunc="mean")
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.heatmap(df_pivot_precip, annot=True, cmap="Blues", fmt=".1f", ax=ax)
    plt.title("Precipitação por Cidade e Data")
    plt.xticks(rotation=45)
    st.pyplot(fig)

if show_temp_max:
    st.subheader("Temperatura Máxima por Cidade e Data")
    df_pivot_max = df_filtered.pivot_table(values="Temp_Max", index="Cidade", columns="Data", aggfunc="mean")
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.heatmap(df_pivot_max, annot=True, cmap="coolwarm", fmt=".1f", ax=ax)
    plt.title("Temperatura Máxima por Cidade e Data")
    plt.xticks(rotation=45)
    st.pyplot(fig)

if show_temp_min:
    st.subheader("Temperatura Mínima por Cidade e Data")
    df_pivot_min = df_filtered.pivot_table(values="Temp_Min", index="Cidade", columns="Data", aggfunc="mean")
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.heatmap(df_pivot_min, annot=True, cmap="coolwarm", fmt=".1f", ax=ax)
    plt.title("Temperatura Mínima por Cidade e Data")
    plt.xticks(rotation=45)
    st.pyplot(fig)

st.write("📌 **Dica:** Selecione apenas algumas cidades para visualizar melhor os gráficos!")
