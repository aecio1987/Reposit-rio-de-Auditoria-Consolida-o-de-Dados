# Pipeline de Auditoria de Frequência e Ocorrências

Este projeto automatiza o processo de ETL (Extração, Transformação e Carga) de dados brutos de auditoria extraídos de planilhas eletrônicas. O pipeline realiza a leitura de múltiplos arquivos Excel, executa uma limpeza e padronização rigorosa das strings de ocorrências e gera um arquivo consolidado em formato CSV pronto para ingestão em nuvem e conexão com o Looker Studio.

## 🚀 Arquitetura do Processo

1. **`consolidar.py`**: Localiza planilhas `.xlsx`, extrai as colunas obrigatórias, aplica regras de negócios (como conversão de faltas injustificadas para justificadas e remoção de caracteres de controle) e unifica tudo em um dataset consolidado.
2. **`upload_bigquery.py`**: Efetua a carga incremental ou total nativamente no ambiente de Big Data (Google BigQuery), forçando a tipagem estrutural como string para blindar o banco contra quebras de linha e caracteres especiais.

## 📋 Pré-requisitos

Certifique-se de possuir o Python instalado em sua máquina e execute a instalação das dependências obrigatórias utilizando o gerenciador de pacotes:

```bash
python -m pip install pandas openpyxl google-cloud-bigquery
