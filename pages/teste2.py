import re
import streamlit as st
import requests
import pandas as pd

def logica_search(cnpj):
    url = f"https://api.casadosdados.com.br/v4/cnpj/{cnpj}"
    headers = {
    "api-key":"485a4129e6a8763fe42c87b03996ab87b93092727623ddf2763da480588d8ed8f36f7b092cfc5af5ec1b5062b9eac8cd8e2ed9298c95f6f25d2908dd8287012c"
        }
    response = requests.get(url,headers=headers)
    if response.status_code == 200:
        data = response.json()
        if "cnpj" in data: # OU if data:
                    # Exibe as informações de forma organizada
            st.success("✅ Consulta realizada com sucesso!")
            st.write("---")
            st.subheader("📊 Informações Gerais")
            st.write(f"**Razão Social**: {data['razao_social']}")
            st.write(f"**CNPJ**: {data['cnpj']}")
            st.write(f"**CNPJ Raiz**: {data['cnpj_raiz']}")
            st.write(f"**Matriz ou Filial**: {data['matriz_filial']}")
            st.write(f"**Natureza Jurídica**: {data['descricao_natureza_juridica']}")
            st.write(f"**Qualificação do Responsável**: {data['qualificacao_responsavel']['descricao']}")
            st.write(f"**Porte da Empresa**: {data['porte_empresa']['descricao']}")
            st.write(f"**Situação Cadastral**: {data['situacao_cadastral']['situacao_atual']}")
            st.write(f"**Motivo da Situação Cadastral**: {data['situacao_cadastral']['motivo']}")
            st.write(f"**Data da Situação Cadastral**: {data['situacao_cadastral']['data']}")

                    # Exibe o endereço
            st.subheader("📍 Endereço")
            st.write("**Endereço**:")
            st.write(f"**Logradouro**: {data['endereco']['logradouro']}, {data['endereco']['numero']}")
            st.write(f"**Bairro**: {data['endereco']['bairro']}")
            st.write(f"**Cidade**: {data['endereco']['municipio']}")
            st.write(f"**Estado**: {data['endereco']['uf']}")
            st.write(f"**CEP**: {data['endereco']['cep']}")

                    # Exibe as atividades econômicas
            st.subheader("💼 Atividades Econômicas")
            st.write(f"**Atividade Principal**: {data['atividade_principal']['descricao']}")
            st.write("**Atividades Secundárias**:")
            for atividade in data['atividade_secundaria']:
                    st.write(f"{atividade['codigo']} - {atividade['descricao']}")

                    # Exibe informações do IBGE
                    st.subheader("📊 Informações do IBGE")
                    st.write(f"**Código Município**: {data['endereco']['ibge']['codigo_municipio']}")
                    st.write(f"**Código UF**: {data['endereco']['ibge']['codigo_uf']}")
                    st.write(f"**Latitude**: {data['endereco']['ibge']['latitude']}")
                    st.write(f"**Longitude**: {data['endereco']['ibge']['longitude']}")

                    st.subheader("📅 Dados Cadastrais")
                    st.write(f"**Data de abertura **:{data['data_abertura']}")
                    st.write(f"**Capital Social**: R$ {data['capital_social']:,.2f}")

                    # Exibe informações sobre o MEI (Microempreendedor Individual)

                    st.write("**Informações sobre o MEI**:")
                    if data['mei']['optante']:
                        st.write(f"Optante pelo MEI desde: {data['mei']['data_opcao_mei']}")
                    else:
                        st.write("Não é optante pelo MEI.")

                    # Exibe informações sobre o Simples Nacional
                    st.subheader("🟢 Simples Nacional")
                    st.write("**Informações sobre o Simples Nacional**:")
                    if data['simples']['optante']:
                        st.write(f"Optante pelo Simples Nacional desde: {data['simples']['data_opcao_simples']}")
                    else:
                        st.write("Não é optante pelo Simples Nacional.")

                    # Exibe os contatos telefônicos
                    st.subheader("📞 Contatos")
                    st.write("**Contatos Telefônicos**:")
                    for contato in data['contato_telefonico']:
                        st.write(f"- {contato['completo']} (Tipo: {contato['tipo']})")

                    # Exibe contatos de email (caso existam)

                    if data['contato_email']:
                        st.write("**Emails de Contato**:")
                        for email in data['contato_email']:
                            st.write(f"- {email}")
                    else:
                        st.write("**Emails de Contato**: Nenhum email disponível.")
            else:
                st.error("❌ CNPJ não encontrado ou inválido.")
                st.error(f"❌ ERROR:{response.status_code}")


def extrair_telefones(lista_telefones):
    """
    Essa função pode receber somente um único número ou pode retornar tambem uma lista de um dataframe
    """
    if isinstance(lista_telefones,list): # Verifica se é uma lista
        resultado = [] # iniciamos a lista vazia que será levada para a nova coluna criada
        for tel in lista_telefones: # passa por cada item (que é uma lista) na lista de telefones
            if 'completo' in tel: # verifica se existe a chave completo existe dentro do item
                resultado.append(tel['completo']) # se houver ele adiciona cada item dentro de "resultado"
            return resultado
    else:
        numero_limpo = re.sub(r'[^\d]', '', lista_telefones)
        pattern = r'^\d{2}9\d{4}\d{4}$'
        if re.match(pattern, numero_limpo):
            return True
        else:
            return False

# passar somente o número aqui e RETIRAR O TOKEN
def verificar_whatsapp(numero):
    numero_limpo = re.sub(r'\D', '', numero)
    url = "https://evo2-gcp8.blubots.com/chat/whatsappNumbers/testegabriel"

    payload = {"numbers": [f"55{numero_limpo}"]}
    headers = {
        "apikey": "bb5wil41ltf76p59klk1ko",
        "Content-Type": "application/json"
    }

    response = requests.request("POST", url, json=payload, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data
        print( "-" * 20)
    else:
        print(f"Erro:{response.status_code}")


# Função para remover caracteres especiais
def remover_caracteres_especiais(texto):
    # Substitui qualquer caractere que não seja alfanumérico ou espaço por uma string vazia
    texto_limpo = re.sub(r'[^A-Za-z0-9\s]', '', texto)
    return texto_limpo

# Função para realizar a requisição à API

def formatar_whatsapp_data(data):
    if not data or not isinstance(data, list):  # Se não for uma lista, retorna vazio
        return ""
    
    resultado_formatado = []
    for sublist in data:  # Percorre cada lista
        for item in sublist:  # Percorre cada dicionário na lista
            numero = item.get("number", "N/A")
            existe = "Sim" if item.get("exists", False) else "Não"
            resultado_formatado.append(f"Número: {numero} - Existe: {existe}")
    
    return "\n".join(resultado_formatado)


def fazer_requisicao(filtros, pagina):
    url = "https://api.casadosdados.com.br/v5/cnpj/pesquisa?tipo_resultado=completo"
    headers = {
        "api-key": "485a4129e6a8763fe42c87b03996ab87b93092727623ddf2763da480588d8ed8f36f7b092cfc5af5ec1b5062b9eac8cd8e2ed9298c95f6f25d2908dd8287012c"
    }


    # Corpo da requisição com os filtros e a página atual
    body = filtros if filtros else {}
    body["mais_filtros"] = {  
        "com_email": True, 
        "somente_celular": True 
    }
    body["pagina"] = pagina  # Adicionar o número da página ao body
    body["quantidade"] = 10  # Número de itens por página

    st.session_state.body = body # sakva o body da sessão
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
        # Quando o botão é clicado ele faz a requisição e inicia na página 1
        resultados = fazer_requisicao(filtros, 1)

        # Verificar a resposta
            # se houver um erro ele imprime essa mensagem
        if "erro" in resultados:
            st.error(f"Erro na requisição: {resultados['erro']}")
            # se não houver um erro ele salva os resultados 
        else:
            # O que é sessão ? Uma área (streamlit salva tudo na própria página), Reaproveitar dados, Excluir ou atualizar dados, Fazer buscas sem precisar recarregar a página 
            # Salvar os seguintes resultados na sessão:
            st.session_state.resultados = resultados['cnpjs'] # Lista de CNPJs obtidos
            st.session_state.total_resultados = resultados['total'] # Total de CNPJs obtido
            st.session_state.filtros = filtros  # Filtros usados na busca
            st.session_state.pagina_atual = 1 # Página atual, que começa na página 1


    # Verificar se há resultados salvos na sessão
    if "resultados" in st.session_state:
        # Se houver
        total = st.session_state.total_resultados # Salva o total de CNPJs obtidos 
        filtros = st.session_state.filtros # Pega os filtros na busca
        pagina_atual = st.session_state.pagina_atual # Pega a página atual

    if "filtros" in st.session_state:
        filtros = st.session_state.filtros
        
        st.subheader(f"Total de resultados: {total}") # Mostra na tela o total de resultados

        # Paginação
        itens_por_pagina = 10 # Cada página contém 10 cnpj's
        num_paginas = (total + itens_por_pagina - 1) // itens_por_pagina # Calcula o total de páginas

        # Atualizar os resultados ao mudar de página
            # Verifica se for a primeira vez que o usuário está interagindo com a página
        if "pagina_atual" not in st.session_state:
            st.session_state.pagina_atual = 1 # Se for mostra a página 1

        pagina_atual = st.session_state.pagina_atual # Guarda a página atual no site
        resultados = fazer_requisicao(filtros, pagina_atual)['cnpjs'] # utiliza a função de requisição e pega o resultado da requisição
        base_url = 'https://casadosdados.com.br/solucao/cnpj/' # cria nossa base url que vai no link clicável
        for item in resultados: # passa por cada item dentro do resultado da requisição
            cnpj = item['cnpj'] # acessa o campo cnpj dentro de item
            item['link_cnpj'] = f'<a href="{base_url}{cnpj}" target="_blank">{cnpj}</a>' # passa no link clicável 
            
                
        # Exibir os resultados da página atual
        df = pd.DataFrame(resultados)
        
        # criamos uma nova coluna dentro do dataframe e aplicamos a função dentro da coluna pra passar por cada item
        #df['Telefone_extraido'] = df['contato_telefonico'].apply(extrair_telefones) # é uma função que pega uma lista, entra nela, extrai dela só uma chave específica e cria uma nova coluna com essa chave
        df['Telefone_extraido'] = df['contato_telefonico'].apply(
            lambda lista:([d["completo"] for d in lista])  # Extrai apenas a chave 'completo' de cada dicionário
        )

        # criamos ua nova coluna que vai ser baseada em outra coluna, a "telefone extraido", acessamos a lista, passamos por cada item dentro da lista e jogamos a função "validate_numero_telefone" dentro de cada item
        # guarda numa variável pra usar depois e não aparecer como nova coluna do DataFrame
        teste = df['Telefone_extraido'].apply(
            lambda lista: [verificar_whatsapp(num) for num in lista]
        )

        df['numero_whatsapp'] = teste.apply(formatar_whatsapp_data)
        st.markdown("<h5 style='font-size:14px;'>Tabela Estática:</h5>", unsafe_allow_html=True)
        st.table(df.style.set_properties(**{'font-size': '10pt', 'padding': '2px'}))

        st.link_button("Exportar","http://localhost:8501/")

        # Coluna do botão de páginas        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("Página Anterior") and pagina_atual > 1:
                st.session_state.pagina_atual -= 1
        # Mostra o número da página atual e o total de páginas.
        with col2: 
            st.write(f"Página {pagina_atual} de {num_paginas}")
        # 
        with col3:
            if st.button("Próxima Página") and pagina_atual < num_paginas:
                st.session_state.pagina_atual += 1

# Rodar a aplicação
if __name__ == "__main__":
    app()
