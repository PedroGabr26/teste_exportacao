import streamlit as st
import requests        

# Trazer para cá os filtros obtidos

def app():
    nome = st.text_input("Nome do arquivo","")
    email = st.text_input("Email a ser enviado","")
    if "@" not in email or "." not in email.split("@")[-1]:
        st.write("Escreva um email correto")
    
    if st.button("Gerar arquivo"):
        url = "https://api.casadosdados.com.br/v5/cnpj/pesquisa/arquivo"
        headers = {
            "api-key": "485a4129e6a8763fe42c87b03996ab87b93092727623ddf2763da480588d8ed8f36f7b092cfc5af5ec1b5062b9eac8cd8e2ed9298c95f6f25d2908dd8287012c"
        }
        filtros = {}
        pagina_atual = 1

        if "filtros" in st.session_state:
            filtros = st.session_state.filtros
        if "pagina_atual" in st.session_state:
            pagina_atual = st.session_state.pagina_atual
        
        body = {
            "total_linhas": 0,
            "nome": nome,
            "tipo": "csv",
            "enviar_para": [email],
            "pesquisa": filtros,  # Adicionando os filtros
            "pagina": pagina_atual,  # Número da página
            "quantidade": 10  # Quantidade de itens por página
        } # Número de itens por página

        # Realizando a requisição
        response = requests.post(url, headers=headers, json=body)

        # Verificando a resposta
        if response.status_code == 200:
            st.success("Arquivo gerado com sucesso e enviado para o e-mail!")
            st.write(response.json())
        else:
            st.write({"erro": response.status_code})
        
if __name__ == "__main__":
    app()