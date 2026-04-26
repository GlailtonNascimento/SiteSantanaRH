
import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="SANTANA RH - Painel Admin",
    page_icon="👥",
    layout="wide"
)

# ============================================================
# LOGIN SIMPLES (depois pode trocar por Google)
# ============================================================

if "logado" not in st.session_state:
    st.session_state.logado = False

def fazer_login():
    st.session_state.logado = True

def fazer_logout():
    st.session_state.logado = False

# Tela de login
if not st.session_state.logado:
    st.title("👥 SANTANA RH SOLUÇÕES")
    st.caption("Painel Administrativo")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("### 🔐 Acesso Restrito")
        senha = st.text_input("Digite a senha:", type="password")
        if st.button("🔓 Entrar", use_container_width=True):
            if senha == "admin123":  # Altere para a senha que ela quiser
                fazer_login()
                st.rerun()
            else:
                st.error("Senha incorreta!")
    st.stop()

# ============================================================
# MENU PRINCIPAL (DEPOIS DO LOGIN)
# ============================================================

st.sidebar.title("👥 SANTANA RH")
st.sidebar.markdown("---")
menu = st.sidebar.radio(
    "📌 Navegação",
    ["📋 Vagas", "📝 Candidatos", "➕ Nova Vaga", "📊 Dashboard"]
)

# Botão sair no sidebar
if st.sidebar.button("🚪 Sair", use_container_width=True):
    fazer_logout()
    st.rerun()

# ============================================================
# 1. GERENCIAMENTO DE VAGAS (Exemplo local - depois Google Sheets)
# ============================================================

if "vagas" not in st.session_state:
    st.session_state.vagas = [
        {
            "id": 1,
            "titulo": "Coordenador(a) de RH",
            "tipo": "CLT | Especialista",
            "local": "Recife, PE",
            "salario": "A combinar",
            "descricao": "Buscamos profissional com experiência em gestão de pessoas e processos de RH.",
            "status": "Ativa"
        },
        {
            "id": 2,
            "titulo": "Analista de Recursos Humanos",
            "tipo": "CLT | Pleno",
            "local": "Recife, PE",
            "salario": "R$ 3.500 - R$ 4.500",
            "descricao": "Atuar no recrutamento e seleção, treinamento e desenvolvimento.",
            "status": "Ativa"
        }
    ]

if "candidatos" not in st.session_state:
    st.session_state.candidatos = []

# ============================================================
# TELA: VAGAS
# ============================================================
if menu == "📋 Vagas":
    st.title("📋 Vagas Cadastradas")
    
    if not st.session_state.vagas:
        st.info("Nenhuma vaga cadastrada. Clique em '+ Nova Vaga' para adicionar.")
    else:
        for vaga in st.session_state.vagas:
            with st.expander(f"📌 {vaga['titulo']} - {vaga['status']}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"**📍 Local:** {vaga['local']}")
                    st.markdown(f"**📌 Tipo:** {vaga['tipo']}")
                with col2:
                    st.markdown(f"**💰 Salário:** {vaga['salario']}")
                    st.markdown(f"**📋 Descrição:** {vaga['descricao']}")
                
                # Botão para desativar vaga
                if st.button(f"🗑️ Remover", key=f"del_{vaga['id']}"):
                    st.session_state.vagas = [v for v in st.session_state.vagas if v['id'] != vaga['id']]
                    st.rerun()

# ============================================================
# TELA: NOVA VAGA
# ============================================================
elif menu == "➕ Nova Vaga":
    st.title("➕ Cadastrar Nova Vaga")
    
    with st.form("form_nova_vaga"):
        titulo = st.text_input("Título da Vaga *")
        tipo = st.text_input("Tipo (ex: CLT | Especialista)")
        local = st.text_input("Local *")
        salario = st.text_input("Salário")
        descricao = st.text_area("Descrição da Vaga *")
        status = st.selectbox("Status", ["Ativa", "Pausada", "Fechada"])
        
        if st.form_submit_button("✅ Publicar Vaga", use_container_width=True):
            if titulo and local and descricao:
                nova_vaga = {
                    "id": len(st.session_state.vagas) + 1,
                    "titulo": titulo,
                    "tipo": tipo,
                    "local": local,
                    "salario": salario if salario else "A combinar",
                    "descricao": descricao,
                    "status": status
                }
                st.session_state.vagas.append(nova_vaga)
                st.success(f"✅ Vaga '{titulo}' publicada com sucesso!")
                st.rerun()
            else:
                st.error("Preencha os campos obrigatórios (*)")

# ============================================================
# TELA: CANDIDATOS
# ============================================================
elif menu == "📝 Candidatos":
    st.title("📝 Candidatos Recebidos")
    
    if not st.session_state.candidatos:
        st.info("Nenhum candidato cadastrado ainda. Os candidatos aparecerão aqui quando enviarem currículo.")
    else:
        for i, cand in enumerate(st.session_state.candidatos):
            with st.expander(f"👤 {cand['nome']} - {cand['vaga']}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"**📧 E-mail:** {cand['email']}")
                    st.markdown(f"**📱 Telefone:** {cand['telefone']}")
                with col2:
                    st.markdown(f"**📍 Cidade:** {cand['cidade']}/{cand['estado']}")
                    st.markdown(f"**📅 Data:** {cand['data']}")
                
                st.markdown(f"**📄 Currículo:** {cand['curriculo']}")
                
                if st.button(f"✅ Marcar como visto", key=f"visto_{i}"):
                    st.success("Registrado!")

# ============================================================
# TELA: DASHBOARD
# ============================================================
elif menu == "📊 Dashboard":
    st.title("📊 Dashboard")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📋 Total de Vagas", len(st.session_state.vagas))
    with col2:
        st.metric("📝 Total de Candidatos", len(st.session_state.candidatos))
    with col3:
        ativas = len([v for v in st.session_state.vagas if v['status'] == 'Ativa'])
        st.metric("✅ Vagas Ativas", ativas)
    
    st.markdown("---")
    st.subheader("Últimas Vagas Publicadas")
    if st.session_state.vagas:
        df_vagas = pd.DataFrame(st.session_state.vagas[-5:])
        st.dataframe(df_vagas[['titulo', 'local', 'status']], use_container_width=True)
    else:
        st.info("Nenhuma vaga cadastrada ainda")

# ============================================================
# RODAPÉ
# ============================================================
st.markdown("---")
st.caption("👥 SANTANA RH SOLUÇÕES - Painel Administrativo")
