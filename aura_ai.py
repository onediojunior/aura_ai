import streamlit as st
import openai
import pandas as pd

# Configurando a API do OpenAI
openai.api_key = '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'  # Sugiro armazenar a chave de API em um lugar mais seguro

# Função para interagir com a API do ChatGPT
def chat_with_gpt3(messages):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    return response.choices[0].message['content'].strip()


def chat_core(name,born,visit):
    initial_message = {
            'role': 'system',
            'content': f"Desconsidere todas as informações anteriores. Atue como terapeuta rogeriana, seguindo a abordagem da terapia centrada no cliente criada por Carl Rogers. Conduza uma sessão de terapia interativa: eu pergunto, você responde e vice-versa. Utilize a identificação de palavras-chave, a análise do sentimento contido nas frases. Lembre-se de nunca impor opiniões. Em vez disso, faça perguntas que incentivem o paciente a compartilhar mais informações. O seu paciente se chama {name}, mas pode chamá-lo pelo primeiro nome. É importante guardar o nome do paciente. Essa é a sua {visit}ª conversa com este paciente."
        }
    welcome_message = {
        'role': 'user',
        'content': f"Olá, {name}! Eu sou a AURA.AI! Verifiquei que é a sua {visit}ª visita. Diga-me o que trouxe você aqui."
    }

    st.subheader("Consulta")        
    session_state = st.session_state
    if "chat_history" not in session_state:
        session_state.chat_history = [initial_message, welcome_message]
        message_welcome = st.chat_message("assistant")
        message_welcome.write(f":blue[AURA.AI] : Olá, {name}! Eu sou a AURA.AI! Verifiquei que é a sua {visit+1}ª visita. Diga-me o que trouxe você aqui")
    # Caixa de entrada para o usuário
    user_input = st.chat_input("Espaço para mensagem do paciente a AURA.AI")

    # Quando o usuário enviar uma mensagem
    if user_input:
        user_message = {
            'role': 'user',
            'content': user_input
        }
        session_state.chat_history.append(user_message)
        response_content = chat_with_gpt3(session_state.chat_history)
        response_message = {
            'role': 'assistant',
            'content': response_content
        }
        session_state.chat_history.append(response_message)
        message = st.chat_message("assistant")
        message.write(f":blue[AURA.AI] : {response_content}")
        # Verificar se a sessão deve ser encerrada
        if "fim da sessão" in user_input.lower():
            st.information("Obrigada(o) pela participação. Espero revê-la(o) em um próximo encontro.")
            del session_state.chat_history
    

# Configuração da página
st.set_page_config(
    page_title="AURA.AI",
    page_icon="https://i.postimg.cc/TP6DwXT8/aura-ai-icon.png",
    layout="wide",
    initial_sidebar_state="auto"
)


# Configuração da barra lateral
st.sidebar.header(":red[**AURA.AI**]")
menu_item = st.sidebar.radio("Selecione o serviço:", ["Home", "Iniciar Consulta"])

# Função para exibir a página inicial
def display_home():
    col1, col2 = st.columns([1, 2])
    col1.image("https://i.postimg.cc/cLzKG6cT/logo-aura-ai-h96.png", use_column_width=False)
    with col2:
        st.markdown("""
            <style>
                .right-aligned {
                    text-align: right;
                    font-size:20px;
                    font-weight: bold;
                }
            </style>
            <div class="right-aligned">
                Funcionamento: Seg - Dom 24h<br/>
                Nosso e-mail : contato@aura_ai.com.br<br/>
                <img src="https://i.postimg.cc/j5fsW01r/rede-social.png" />
            </div>
        """, unsafe_allow_html=True)
    st.image("https://i.postimg.cc/bvVVc7C1/header-aura.png", use_column_width=True)
    h1col2 = st.columns([1,4,1])[1]
    
    # Utilizando HTML para personalizar a exibição do texto centralizado
    st.markdown(
        """
        <style>
            .big-font {
                font-size: 24px !important;
                text-align: center;
                font-weight: bold;
            }
        </style>
        """, unsafe_allow_html=True
    )
    # Usando a classe .big-font para exibir o texto com a formatação desejada
    st.markdown("<div class='big-font'><i>Toda jornada começa com o primeiro passo,<br/> então você acabou de dar o seu</i>.<br/><br/></div>", unsafe_allow_html=True)
    h2col1, h2col2 = st.columns([1, 1])
    h2col1.image("https://i.postimg.cc/KjFSWXsx/left-sec1.png")
    h2col2.title("POR QUE :red[AURA.AI]?")
    reasons = [
        "◼ Disponibilidade Contínua",
        "◼ Consistência nas Respostas",
        "◼ Privacidade Garantida",
        "◼ Acessibilidade e Custo",
        "Assim, enquanto a terapia tradicional tem seu valor inestimável, a terapeuta baseada em IA oferece uma alternativa acessível e consistente para a saúde mental moderna"
    ]
    for reason in reasons:
        h2col2.subheader(reason)
    # Utilizando HTML para personalizar a exibição do rodapé
    st.markdown(
        """
        <style>
            .rodape {
                background : #ff0000;
                width: 100%;
                font-size: 14px;
                color: #fff;
                text-align: center;
                font-weight: bold;
                height:24px
            }
        </style>
        """, unsafe_allow_html=True
    )
    # Usando a classe .rodape para exibir o texto com a formatação desejada
    st.markdown("<div class='rodape'><center>Todos os direitos reservados - Curso IA Generativa I2A2 2023</center></div>", unsafe_allow_html=True)
    
# Função para iniciar a consulta
def initiate_consultation():
    st.image("https://i.postimg.cc/8cbR5BPh/banner-2.png", use_column_width=True)
    st.subheader("Seja bem-vinda(o)!")
    
    # Se o CPF já foi inserido, vá diretamente para a consulta
    cpf_input = st.session_state.get('cpf_input', '')
    if not cpf_input:
        # Ler o dataset
        df = pd.read_csv("users.csv")
        # cliente informa cpf
        cpf_input = st.text_input("CPF (Digite apenas os números)", value="", max_chars=11)
        if st.button('Iniciar consulta'):
            filtered_df = df.query(f"cpf == {cpf_input}")
            if not filtered_df.empty:
                user_info = filtered_df.values.tolist()
                name = user_info[0][1]
                born = user_info[0][2]
                visit = user_info[0][3]
                # Adiciona ao session_state
                st.session_state.cpf_input = cpf_input
                st.session_state.user_info = user_info
                st.session_state.name = name
                st.session_state.born = born
                st.session_state.visit = visit
                chat_core(name,born,visit)
            else:
                st.warning("CPF não encontrado.")
    else:
        # Inicie a conversa se o CPF estiver no session_state
        user_info = st.session_state.user_info
        name = st.session_state.name
        born = st.session_state.born
        visit = st.session_state.visit
        chat_core(name, born, visit)
        
# Página principal
if menu_item == "Home":
    display_home()
elif menu_item == "Iniciar Consulta":
    initiate_consultation()
