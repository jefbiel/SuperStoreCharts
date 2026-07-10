# SuperStore Charts

Dashboard em Streamlit para análise exploratória do conjunto de dados Superstore.

## Rodar localmente

```bash
pip install -r requirements.txt
streamlit run dashboard.py
```

## Deploy online

### Opção 1: Streamlit Community Cloud

1. Faça push deste repositório para o GitHub.
2. Entre em https://share.streamlit.io.
3. Selecione o repositório `jefbiel/SuperStoreCharts`.
4. Informe o arquivo principal como `dashboard.py`.
5. Clique em Deploy.

### Opção 2: Render

1. Crie um novo Web Service apontando para o repositório.
2. Use o comando de start:

```bash
streamlit run dashboard.py --server.port $PORT --server.address 0.0.0.0
```

3. Garanta que as dependências do `requirements.txt` sejam instaladas.

## Observação

O app aceita upload de arquivos CSV e Excel. Se nenhum arquivo for enviado, ele usa o `Superstore.csv` incluído no repositório.