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
    df_filtered['Data'] = pd.to_datetime(df_filtered['Data'], errors='coerce')  # Certificar que 'Data' é datetime
    df_filtered['Data'] = df_filtered['Data'].dt.strftime('%Y-%m-%d')

    stories = []
    for _, row in df.iterrows():
        story = ""

        if row["Temp_Max"] > 30:
            if row["Condicao"] in ["Chuva", "Chuva forte", "Chuva com trovoada", "Períodos de chuva", "Chuvas e trovoadas ocasionais"]:
                story = f"Hoje, {row['Cidade']} está muito quente, com grandes chances de chuva, tornando o dia desconfortável."
            elif row["Condicao"] in ["Nevoeiro", "Nublado", "Nebulosidade variável"]:
                story = f"Em {row['Cidade']}, o calor excessivo combinado com o tempo nublado pode tornar o clima abafado e desconfortável."
            elif row["Condicao"] == "Maioritariamente nublado":
                story = f"Em {row['Cidade']}, o calor excessivo combinado com um céu predominantemente nublado pode tornar o clima abafado."
            else:
                story = f"Hoje, {row['Cidade']} está bastante quente, ideal para atividades externas."

        elif 18 <= row["Temp_Max"] <= 26:
            if row["Condicao"] in ["Chuva", "Chuva forte", "Chuva com trovoada", "Períodos de chuva", "Chuvas e trovoadas ocasionais"]:
                story = f"{row['Cidade']} tem uma temperatura agradável, mas a chuva pode atrapalhar atividades ao ar livre."
            elif row["Condicao"] in ["Nublado", "Nebulosidade variável"]:
                story = f"{row['Cidade']} tem uma temperatura agradável, mas o céu nublado pode tornar as caminhadas menos agradáveis."
            elif row["Condicao"] == "Maioritariamente com sol":
                story = f"{row['Cidade']} tem um clima perfeito para atividades ao ar livre, com predominância de sol."
            elif row["Condicao"] in ["Ventos fortes", "Tempestade com ventos fortes"]:
                story = f"{row['Cidade']} tem uma temperatura confortável, mas ventos fortes tornam as atividades ao ar livre mais difíceis."
            else:
                story = f"{row['Cidade']} tem um clima perfeito para caminhadas ao ar livre."

        elif row["Temp_Max"] < 18:
            if row["Condicao"] in ["Chuva", "Chuva forte", "Períodos de chuva"]:
                story = f"Em {row['Cidade']}, a temperatura baixa e a chuva forte tornam o dia desconfortável e pouco propício para atividades ao ar livre."
            elif row["Condicao"] == "Neve":
                story = f"{row['Cidade']} está com temperatura baixa e neve, tornando o clima ideal para quem gosta de atividades de inverno."
            elif row["Condicao"] in ["Nublado", "Maioritariamente nublado"]:
                story = f"A temperatura está fria em {row['Cidade']}, e o céu nublado faz o dia parecer ainda mais gelado."
            else:
                story = f"{row['Cidade']} tem um clima ameno, ótimo para relaxar em ambientes fechados."

        elif row["Condicao"] in ["Tempestade", "Neve", "Granizo"]:
            story = f"Em {row['Cidade']}, condições climáticas extremas, como {row['Condicao']}, tornam o dia mais difícil."

        elif row["Condicao"] in ["Ventos fortes", "Tempestade com ventos fortes"]:
            story = f"Os ventos fortes em {row['Cidade']} tornam o clima mais intenso, ideal para se proteger em ambientes fechados."
        elif row["Condicao"] == "Nevoeiro":
            story = f"Nevoeiro em {row['Cidade']} pode dificultar a visibilidade, cuidado nas estradas."
        elif row["Condicao"] in ["Trovoada em partes da zona", "Aguaceiro ou trovoada"]:
            story = f"Em {row['Cidade']}, a trovoada em partes da zona pode trazer chuvas e ventos fortes em algumas áreas."

        # 🔹 Se nenhuma condição for atendida, cria uma história genérica
        if not story:
            story = f"O clima em {row['Cidade']} hoje é {row['Condicao']}, com temperatura máxima de {row['Temp_Max']}°C."

        stories.append(story)

    return stories



# Gerando as histórias
stories = generate_stories(df_filtered)

# Adicionando as histórias ao dataframe
df_filtered['História Climática'] = stories

# Exibindo a tabela interativa com as histórias
st.subheader("📅 Tabela de Dados Climáticos por Data e Cidade")
st.dataframe(df_filtered[['Data', 'Cidade', 'Temp_Max', 'Temp_Min', 'Precipitacao', 'Condicao', 'História Climática']], use_container_width=True)

# Gráficos de Análise
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
