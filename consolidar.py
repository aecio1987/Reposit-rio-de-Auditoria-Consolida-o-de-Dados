import os
import glob
import pandas as pd

# Define a pasta de origem de forma genérica para rodar em qualquer máquina
# Se a variável de ambiente PASTA_PLANILHAS não existir, usa a pasta './planilhas' do diretório atual
pasta_origem = os.getenv("PASTA_PLANILHAS", "./planilhas")

colunas_obrigatorias = [
    "DRE", "TipoLotacao", "Municipio", "Lotacao", "Nome Usuário", 
    "TipoVinculo", "Funcao", "CPF", "Matricula", "Vinculo", 
    "Codigo", "Ocorrencia", "Data", "Mês"
]

# Dicionário de padronização exata de ocorrências
mapeamento_ocorrencias = {
    # 1
    "ATESTADO DE COMPARECIMENTO CONSULTA OU AFASTAMENTO MÉDICO ATÉ 03 DIAS": "1 - ATESTADO DE COMPARECIMENTO CONSULTA OU AFASTAMENTO MÉDICO ATÉ 03 DIAS",
    "01  -  ATESTADO DE COMPARECIMENTO CONSULTA OU AFASTAMENTO MÉDICO ATÉ 03 DIAS": "1 - ATESTADO DE COMPARECIMENTO CONSULTA OU AFASTAMENTO MÉDICO ATÉ 03 DIAS",
    "1 -  ATESTADO DE COMPARECIMENTO CONSULTA OU AFASTAMENTO MÉDICO ATÉ 03 DIAS": "1 - ATESTADO DE COMPARECIMENTO CONSULTA OU AFASTAMENTO MÉDICO ATÉ 03 DIAS",
    # 2
    "REUNIÃO EXTERNA OU VISITA TÉCNICA": "2 - REUNIÃO EXTERNA OU VISITA TÉCNICA",
    "2 -  REUNIÃO EXTERNA OU VISITA TÉCNICA": "2 - REUNIÃO EXTERNA OU VISITA TÉCNICA",
    "02  -  REUNIÃO EXTERNA OU VISITA TÉCNICA": "2 - REUNIÃO EXTERNA OU VISITA TÉCNICA",
    # 3
    "GREVE OU REUNIÃO SINDICAL / ASSOCIAÇÃO": "3 - GREVE OU REUNIÃO SINDICAL/ASSOCIAÇÃO",
    "03  -  GREVE OU REUNIÃO SINDICAL / ASSOCIAÇÃO": "3 - GREVE OU REUNIÃO SINDICAL/ASSOCIAÇÃO",
    "3 -  GREVE OU REUNIÃO SINDICAL / ASSOCIAÇÃO": "3 - GREVE OU REUNIÃO SINDICAL/ASSOCIAÇÃO",
    "3 - GREVE OU REUNIÃO SINDICAL / ASSOCIAÇÃO": "3 - GREVE OU REUNIÃO SINDICAL/ASSOCIAÇÃO",
    # 4
    "ENTRADA COM ATRASO OU SAÍDA ANTECIPADA AUTORIZADA (ATÉ 03 VEZES NO MÊS)": "4 - ENTRADA COM ATRASO OU SAÍDA ANTECIPADA AUTORIZADA",
    "04  -  ENTRADA COM ATRASO OU SAÍDA ANTECIPADA AUTORIZADA (ATÉ 03 VEZES NO MÊS)": "4 - ENTRADA COM ATRASO OU SAÍDA ANTECIPADA AUTORIZADA",
    "4 -  ENTRADA COM ATRASO OU SAÍDA ANTECIPADA AUTORIZADA (ATÉ 03 VEZES NO MÊS)": "4 - ENTRADA COM ATRASO OU SAÍDA ANTECIPADA AUTORIZADA",
    # 5
    "PRESENÇA NÃO REGISTRADA (ATÉ 03 VEZES NO MÊS)": "5 - PRESENÇA NÃO REGISTRADA",
    "05  -  PRESENÇA NÃO REGISTRADA (ATÉ 03 VEZES NO MÊS)": "5 - PRESENÇA NÃO REGISTRADA",
    "45 -  FREQUÊNCIA REGISTRADA MANUALMENTE": "45 -  FREQUÊNCIA REGISTRADA MANUALMENTE",
    # 49
    "FALTA JUSTIFICADA": "49 -  FALTA JUSTIFICADA",
    "49 -  FALTA JUSTIFICADA": "49 -  FALTA JUSTIFICADA",
    "49  -  FALTA JUSTIFICADA": "49 -  FALTA JUSTIFICADA",
    # 50
    "AGUARDANDO APOSENTADORIA POR INVALIDEZ": "50 -  AGUARDANDO APOSENTADORIA POR INVALIDEZ",
    "50  -  AGUARDANDO APOSENTADORIA POR INVALIDEZ": "50 -  AGUARDANDO APOSENTADORIA POR INVALIDEZ",
    "50 -  AGUARDANDO APOSENTADORIA POR INVALIDEZ": "50 -  AGUARDANDO APOSENTADORIA POR INVALIDEZ",
    # 52
    "FOLGA COMPENSATÓRIA CONFORME IN 002/2011 (SOCIO/SISPEN)": "52 -  FOLGA COMPENSATÓRIA CONFORME IN 002/2011 (SOCIO/SISPEN)",
    "52  -  FOLGA COMPENSATÓRIA CONFORME IN 002/2011 (SOCIO/SISPEN)": "52 -  FOLGA COMPENSATÓRIA CONFORME IN 002/2011 (SOCIO/SISPEN)",
    "52 -  FOLGA COMPENSATÓRIA CONFORME IN 002/2011 (SOCIO/SISPEN)": "52 -  FOLGA COMPENSATÓRIA CONFORME IN 002/2011 (SOCIO/SISPEN)",
    # 54
    "54  -  LICENÇA POR DESEMPENHO E ASSIDUIDADE": "54 -  LICENÇA POR DESEMPENHO E ASSIDUIDADE",
    "54 -  LICENÇA POR DESEMPENHO E ASSIDUIDADE": "54 -  LICENÇA POR DESEMPENHO E ASSIDUIDADE"
}

print("Lendo e juntando tudo em um arquivo único...")

# Busca todos os arquivos Excel no diretório configurado
arquivos_excel = glob.glob(os.path.join(pasta_origem, "*.xlsx"))
arquivos_dados = [arq for arq in arquivos_excel if "csv_unico_auditoria" not in os.path.basename(arq).lower()]

lista_dataframes = []

for arquivo in arquivos_dados:
    print(f"Lendo: {os.path.basename(arquivo)}")
    try:
        df = pd.read_excel(arquivo, dtype={"CPF": str, "Matricula": str, "Ocorrencia": str})
        if not df.empty:
            df = df.reindex(columns=colunas_obrigatorias)
            
            # Remove espaços extras nas pontas para garantir o casamento perfeito do texto
            df["Ocorrencia"] = df["Ocorrencia"].astype(str).str.strip()
            
            # Executa a substituição em lote baseada no mapeamento de padronização
            df["Ocorrencia"] = df["Ocorrencia"].replace(mapeamento_ocorrencias)
            
            # Tratamento para as variações de FALTA INJUSTIFICADA
            df.loc[df["Ocorrencia"].str.startswith("FALTA INJUSTIFICADA", na=False), "Ocorrencia"] = "49 -  FALTA JUSTIFICADA"
            
            lista_dataframes.append(df)
    except Exception as e:
        print(f"Erro ao ler {os.path.basename(arquivo)}: {e}")

if lista_dataframes:
    base_total = pd.concat(lista_dataframes, ignore_index=True)
    caminho_saida = os.path.join(pasta_origem, "csv_unico_auditoria.csv")

    base_total.to_csv(caminho_saida, index=False, sep=",", encoding="utf-8")
    print(f"\nSucesso! Arquivo gerado com dados padronizados: csv_unico_auditoria.csv")
    print(f"Total de linhas processadas: {len(base_total)}")
else:
    print("\nNenhum arquivo válido encontrado para consolidação.")
