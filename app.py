import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configuração da página
st.set_page_config(page_title="Análise Climática", layout="wide")

# Carregar os dados
def load_data():
    df = pd.read_csv("https://raw.githubusercontent.com/MarceloMFerreira/archives/refs/heads/main/previsoes_tempo.csv")
    df["Data"] = pd.to_datetime(df["Data"])
    return df

df = load_data()

st.title("📊 Análise de Dados Meteorológicos")

# Seleção de cidades
cidades = st.multiselect("Selecione as cidades:", df["Cidade"].unique(), default=df["Cidade"].unique())
df_filtered = df[df["Cidade"].isin(cidades)]

# Gráficos
st.subheader("Temperatura Máxima e Mínima por Data e Cidade")
fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(data=df_filtered, x="Data", y="Temp_Max", hue="Cidade", marker="o", ax=ax)
plt.title("Evolução da Temperatura Máxima")
plt.xlabel("Data")
plt.ylabel("Temp Max (°C)")
plt.xticks(rotation=45)
st.pyplot(fig)

fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(data=df_filtered, x="Data", y="Temp_Min", hue="Cidade", marker="o", linestyle="dashed", ax=ax)
plt.title("Evolução da Temperatura Mínima")
plt.xlabel("Data")
plt.ylabel("Temp Min (°C)")
plt.xticks(rotation=45)
st.pyplot(fig)

st.subheader("Média de Temperaturas e Precipitação")
df_pivot = df_filtered.pivot_table(values=["Temp_Max", "Temp_Min", "Precipitacao"], index=["Data", "Cidade"], aggfunc="mean").reset_index()

fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(data=df_pivot, x="Data", y="Temp_Max", hue="Cidade", palette="tab10", ax=ax)
plt.title("Média de Temp Max por Data e Cidade")
plt.xticks(rotation=45)
st.pyplot(fig)

fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(data=df_pivot, x="Data", y="Temp_Min", hue="Cidade", palette="tab10", ax=ax)
plt.title("Média de Temp Min por Data e Cidade")
plt.xticks(rotation=45)
st.pyplot(fig)

fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(data=df_pivot, x="Data", y="Precipitacao", hue="Cidade", palette="tab10", ax=ax)
plt.title("Média de Precipitação por Data e Cidade")
plt.xticks(rotation=45)
st.pyplot(fig)

st.subheader("Temperatura e Precipitação por Condição do Tempo")
df_grouped = df_filtered.groupby(["Cidade", "Condicao"], as_index=False)[["Temp_Max", "Temp_Min", "Precipitacao"]].mean()

fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(data=df_grouped, x="Cidade", y="Temp_Max", hue="Condicao", palette="viridis", ax=ax)
plt.title("Temperatura Máxima por Cidade e Condição")
st.pyplot(fig)

fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(data=df_grouped, x="Cidade", y="Temp_Min", hue="Condicao", palette="viridis", ax=ax)
plt.title("Temperatura Mínima por Cidade e Condição")
st.pyplot(fig)

fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(data=df_grouped, x="Cidade", y="Precipitacao", hue="Condicao", palette="viridis", ax=ax)
plt.title("Precipitação por Cidade e Condição")
st.pyplot(fig)

# Ajustar a data para exibir de forma bonita (sem horário)
df_filtered['Data'] = df_filtered['Data'].dt.strftime('%d/%m/%Y')

# Precipitação
df_pivot_precip = df_filtered.pivot_table(values="Precipitacao", index="Cidade", columns="Data", aggfunc="mean")
fig, ax = plt.subplots(figsize=(12, 6))
sns.heatmap(df_pivot_precip, annot=True, cmap="Blues", fmt=".1f", ax=ax)
plt.title("Precipitação por Cidade e Data")
plt.xticks(rotation=45)
st.pyplot(fig)

# Temperatura Máxima
df_pivot_max = df_filtered.pivot_table(values="Temp_Max", index="Cidade", columns="Data", aggfunc="mean")
fig, ax = plt.subplots(figsize=(12, 6))
sns.heatmap(df_pivot_max, annot=True, cmap="coolwarm", fmt=".1f", ax=ax)
plt.title("Temperatura Máxima por Cidade e Data")
plt.xticks(rotation=45)
st.pyplot(fig)

# Temperatura Mínima
df_pivot_min = df_filtered.pivot_table(values="Temp_Min", index="Cidade", columns="Data", aggfunc="mean")
fig, ax = plt.subplots(figsize=(12, 6))
sns.heatmap(df_pivot_min, annot=True, cmap="coolwarm", fmt=".1f", ax=ax)
plt.title("Temperatura Mínima por Cidade e Data")
plt.xticks(rotation=45)
st.pyplot(fig)


st.write("📌 **Dica:** Selecione apenas algumas cidades para visualizar melhor os gráficos!")
