import streamlit as st
import json

# Biblioteca para criptografia
import bcrypt  

ARQUIVOS_USUÁRIOS = "usuarios.json"

st.set_page_config(layout="wide", initial_sidebar_state="collapsed")


st.title('Introdução à Lógica de Programação em Python')

def carregar_usuarios():
    try:
        with open(ARQUIVOS_USUÁRIOS, "r") as arquivo:
            return json.load(arquivo)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def salvar_usuarios(usuarios):
    with open(ARQUIVOS_USUÁRIOS, "w") as arquivo:
        json.dump(usuarios, arquivo)

def cadastrar():
    usuarios = carregar_usuarios()
    st.header('Cadastro de Usuário')

    aluno = st.text_input('Nome do Aluno', key="cadastro_aluno")
    senha = st.text_input('Senha', type="password", key="cadastro_senha")

    if st.button('Cadastrar', key="btn_cadastrar"):
        if aluno in usuarios:
            st.error('Usuário já existente!')
        else:
            # Criptografar a senha antes de salvar
            senha_hash = bcrypt.hashpw(senha.encode(), bcrypt.gensalt()).decode()
            usuarios[aluno] = senha_hash
            salvar_usuarios(usuarios)
            st.success('Cadastro realizado com sucesso!')

def login():
    usuarios = carregar_usuarios()
    st.header('Login')

    aluno = st.text_input('Usuário', key="login_aluno")
    senha = st.text_input('Senha', type="password", key="login_senha")
    st.session_state['nome_usuario'] = aluno

    if st.button('Entrar', key="btn_login"):
        if aluno in usuarios:
            senha_hash = usuarios[aluno].encode()  # Converter para bytes
            if bcrypt.checkpw(senha.encode(), senha_hash):
                st.switch_page("pages/Página2.py")
            else:
                st.error('Usuário ou senha incorretos.')
        else:
            st.error('Usuário não encontrado.')

# Interface com abas
aba = st.radio("Escolha uma opção:", ["Cadastro", "Login"], key="menu")

if aba == "Cadastro":
    cadastrar()
elif aba == "Login":
    login()


