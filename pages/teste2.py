import re
import streamlit as st
import requests
import pandas as pd

# Função para remover caracteres especiais
def remover_caracteres_especiais(texto):
    # Substitui qualquer caractere que não seja alfanumérico ou espaço por uma string vazia
    texto_limpo = re.sub(r'[^A-Za-z0-9\s]', '', texto)
    return texto_limpo

# Função para realizar a requisição à API
def fazer_requisicao(filtros, pagina):
    url = "https://api.casadosdados.com.br/v5/cnpj/pesquisa"
    headers = {
        "api-key": "485a4129e6a8763fe42c87b03996ab87b93092727623ddf2763da480588d8ed8f36f7b092cfc5af5ec1b5062b9eac8cd8e2ed9298c95f6f25d2908dd8287012c"
    }

    # Corpo da requisição com os filtros e a página atual
    body = filtros if filtros else {}
    body["pagina"] = pagina  # Adicionar o número da página ao body
    body["quantidade"] = 10  # Número de itens por página

    # Realizando a requisição
    response = requests.post(url, headers=headers, json=body)

    # Verificando a resposta
    if response.status_code == 200:
        return response.json()
    else:
        return {"erro": response.status_code}

# Interface com Streamlit
def app():
    st.title("Busca Avançada CNPJ")

    # Campos de input para os filtros (removendo caracteres especiais)
    cnpj = remover_caracteres_especiais(st.text_input("CNPJ", ""))
    cnae = remover_caracteres_especiais(st.text_input("Código de Atividade Principal", ""))
    estado = remover_caracteres_especiais(st.text_input("Estado", ""))
    bairro = remover_caracteres_especiais(st.text_input("Bairro", ""))
    ddd = remover_caracteres_especiais(st.text_input("DDD", ""))
    nome_empresa = remover_caracteres_especiais(st.text_input("Nome da Empresa", ""))
    municipio = remover_caracteres_especiais(st.text_input("Município", ""))
    situacao_cadastral = st.selectbox("Situação Cadastral", ["", "ATIVA", "INAPTA", "BAIXADA", "NULA", "SUSPENSA"])
    capital_social_minimo = st.number_input("Capital Social Mínimo", min_value=0, step=1000, value=0)
    capital_social_maximo = st.number_input("Capital Social Máximo", min_value=0, step=1000, value=0)

    # Criando o dicionário de filtros
    filtros = {}
    if cnpj:
        filtros['cnpj'] = [x.strip() for x in cnpj.split(',')]
    if cnae:
        filtros['codigo_atividade_principal'] = [x.strip() for x in cnae.split(',')]
    if estado:
        filtros['uf'] = [x.strip() for x in estado.split(',')]
    if bairro:
        filtros['bairro'] = [x.strip() for x in bairro.split(',')]
    if ddd:
        filtros['ddd'] = [x.strip() for x in ddd.split(',')]
    if nome_empresa:
        filtros['nome_empresa'] = [x.strip() for x in nome_empresa.split(',')]
    if municipio:
        filtros['municipio'] = [x.strip() for x in municipio.split(',')]
    if situacao_cadastral:
        filtros['situacao_cadastral'] = [situacao_cadastral]
    if capital_social_minimo or capital_social_maximo:
        filtros['capital_social'] = {
            "minimo": capital_social_minimo,
            "maximo": capital_social_maximo
        }

    # Botão para realizar a busca
    if st.button("Buscar"):
        # Fazer a requisição inicial com a página 1
        resultados = fazer_requisicao(filtros, 1)

        # Verificar a resposta
        if "erro" in resultados:
            st.error(f"Erro na requisição: {resultados['erro']}")
        else:
            # Salvar os resultados na sessão
            st.session_state.resultados = resultados['cnpjs']
            st.session_state.total_resultados = resultados['total']
            st.session_state.filtros = filtros  # Salvar os filtros na sessão
            st.session_state.pagina_atual = 1  # Resetar para a página 1

    # Verificar se há resultados salvos na sessão
    if "resultados" in st.session_state:
        total = st.session_state.total_resultados
        filtros = st.session_state.filtros
        pagina_atual = st.session_state.pagina_atual

        st.subheader(f"Total de resultados: {total}")

        # Paginação
        itens_por_pagina = 10
        num_paginas = (total + itens_por_pagina - 1) // itens_por_pagina

        # Atualizar os resultados ao mudar de página
        if "pagina_atual" not in st.session_state:
            st.session_state.pagina_atual = 1

        pagina_atual = st.session_state.pagina_atual
        resultados = fazer_requisicao(filtros, pagina_atual)['cnpjs']

        # Exibir os resultados da página atual
        df = pd.DataFrame(resultados)
        st.dataframe(df)

        # Controle de paginação
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("Página Anterior") and pagina_atual > 1:
                st.session_state.pagina_atual -= 1
        with col2:
            st.write(f"Página {pagina_atual} de {num_paginas}")
        with col3:
            if st.button("Próxima Página") and pagina_atual < num_paginas:
                st.session_state.pagina_atual += 1

# Rodar a aplicação
if __name__ == "__main__":
    app()