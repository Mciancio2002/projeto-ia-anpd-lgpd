"""
Projeto: Analise de Decisoes Sancionadoras da ANPD sob a otica da
Responsabilidade Civil na LGPD - apoiada por IA/LLM
Disciplina: Inteligencia Artificial - Prof. Dr. Leandro Zerbinatti - 7oJ SI Noite
Universidade Presbiteriana Mackenzie

Cabecalho de identificacao (entrega individual):
- Mateus Ciancio - RA 10390145 - 10390145@mackenzista.com.br

Sintese do arquivo:
Script de analise exploratoria e preparacao inicial do dataset de decisoes
sancionadoras da ANPD (Autoridade Nacional de Protecao de Dados), coletado
manualmente a partir de fontes publicas oficiais (gov.br/anpd), para uso
como dataset original do Projeto N1 da disciplina de Inteligencia Artificial.

Historico de alteracoes:
- 15/09/2026, Mateus Ciancio, criacao do script e da analise exploratoria inicial
"""

import pandas as pd
import matplotlib.pyplot as plt

# --- Carregamento do dataset original ---
df = pd.read_csv("dataset/anpd_decisoes_sancionadoras.csv")

print("=== Visao geral do dataset ===")
print(f"Numero de processos coletados: {len(df)}")
print(f"Colunas: {list(df.columns)}\n")

print("=== Distribuicao por setor (agente de tratamento) ===")
print(df["setor"].value_counts(), "\n")

print("=== Distribuicao por status do processo ===")
print(df["status"].value_counts(), "\n")

print("=== Distribuicao por ano de instrucao ===")
print(df["ano_instrucao"].value_counts().sort_index(), "\n")

print("=== Completude dos campos qualitativos (motivo/artigo) ===")
pendentes_motivo = df["motivo_resumido"].str.contains("A verificar", na=False).sum()
pendentes_artigo = df["artigo_lgpd_citado"].str.contains("A verificar", na=False).sum()
print(f"Registros com motivo ainda nao extraido do relatorio integral: {pendentes_motivo}/{len(df)}")
print(f"Registros com artigo da LGPD ainda nao identificado: {pendentes_artigo}/{len(df)}")
print("-> Esses campos serao preenchidos na proxima etapa, com apoio de um LLM")
print("   que lera o inteiro teor dos Relatorios de Instrucao (PDFs oficiais).\n")

# --- Preparacao dos dados: variavel derivada (multa pecuniaria sim/nao) ---
df["teve_multa_pecuniaria"] = df["tipo_sancao"].str.contains("Multa pecuniaria", na=False)
df.to_csv("dataset/anpd_decisoes_sancionadoras_preparado.csv", index=False)

# --- Graficos ---
plt.figure(figsize=(6, 4))
df["setor"].value_counts().plot(kind="bar", color=["#2E5C8A", "#8AA9C7"])
plt.title("Processos sancionadores da ANPD por setor do agente de tratamento")
plt.ylabel("Numero de processos")
plt.xlabel("Setor")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("figs/distribuicao_setor.png", dpi=150)
plt.close()

plt.figure(figsize=(7, 4))
df["ano_instrucao"].value_counts().sort_index().plot(kind="bar", color="#2E5C8A")
plt.title("Processos sancionadores por ano de instrucao")
plt.ylabel("Numero de processos")
plt.xlabel("Ano")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("figs/distribuicao_ano.png", dpi=150)
plt.close()

plt.figure(figsize=(6, 4))
df["teve_multa_pecuniaria"].value_counts().rename({True: "Com multa", False: "Sem multa"}).plot(
    kind="bar", color=["#C0392B", "#2E5C8A"]
)
plt.title("Processos com aplicacao de multa pecuniaria")
plt.ylabel("Numero de processos")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("figs/multa_pecuniaria.png", dpi=150)
plt.close()

print("Graficos salvos em figs/. Dataset preparado salvo em dataset/anpd_decisoes_sancionadoras_preparado.csv")
