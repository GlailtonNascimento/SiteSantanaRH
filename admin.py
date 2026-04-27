
import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="SANTANA RH - Painel Admin", page_icon="👥", layout="wide")

# ============================================================
# LOGIN
# ============================================================
if "logado" not in st.session_state:
    st.session_state.logado = False

def fazer_login():
    st.session_state.logado = True

def fazer_logout():
    st.session_state.logado = False

if not st.session_state.logado:
    st.title("👥 SANTANA RH SOLUÇÕES")
    st.caption("Painel Administrativo")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("### 🔐 Acesso Restrito")
        senha = st.text_input("Digite a senha:", type="password")
        if st.button("🔓 Entrar", use_container_width=True):
            if senha == "admin123":
                fazer_login()
                st.rerun()
            else:
                st.error("Senha incorreta!")
    st.stop()

# ============================================================
# INICIALIZAÇÃO DAS BASES (simulando banco)
# ============================================================
if "vagas" not in st.session_state:
    st.session_state.vagas = []

if "candidatos" not in st.session_state:
    st.session_state.candidatos = []

# ============================================================
# MENU LATERAL
# ============================================================
st.sidebar.title("👥 SANTANA RH")
st.sidebar.markdown("---")
menu = st.sidebar.radio("📌 Navegação", ["📋 Vagas", "➕ Nova Vaga", "📝 Candidatos", "📊 Dashboard"])

if st.sidebar.button("🚪 Sair", use_container_width=True):
    fazer_logout()
    st.rerun()

# ============================================================
# TELA: VAGAS (listar)
# ============================================================
if menu == "📋 Vagas":
    st.title("📋 Vagas Cadastradas")
    if not st.session_state.vagas:
        st.info("Nenhuma vaga cadastrada. Clique em '+ Nova Vaga' para adicionar.")
    else:
        for i, vaga in enumerate(st.session_state.vagas):
            with st.expander(f"📌 {vaga['titulo']} - {vaga['tipo_vaga']} - {vaga['status']}"):
                st.markdown(f"**📝 Descrição:** {vaga['descricao']}")
                
                if vaga['tipo_vaga'] == 'Própria':
                    st.markdown(f"**📍 Local:** {vaga['local']}")
                    st.markdown(f"**📌 Tipo:** {vaga['tipo_contrato']}")
                    st.markdown(f"**💰 Salário:** {vaga['salario']}")
                else:
                    st.markdown(f"**🔗 Link externo:** [Acessar vaga]({vaga['link_externo']})")
                
                if st.button(f"🗑️ Remover", key=f"del_{i}"):
                    st.session_state.vagas.pop(i)
                    st.rerun()

# ============================================================
# TELA: NOVA VAGA (com escolha do tipo)
# ============================================================
elif menu == "➕ Nova Vaga":
    st.title("➕ Cadastrar Nova Vaga")
    
    tipo_vaga = st.radio("Tipo de vaga:", ["Própria", "Externa (só link)"], horizontal=True)
    
    with st.form("form_nova_vaga"):
        titulo = st.text_input("Título da Vaga *")
        descricao = st.text_area("Descrição da Vaga *")
        
        if tipo_vaga == "Própria":
            local = st.text_input("Local *")
            tipo_contrato = st.text_input("Tipo de contrato (ex: CLT, PJ)")
            salario = st.text_input("Salário")
            link_externo = ""
        else:
            local = ""
            tipo_contrato = ""
            salario = ""
            link_externo = st.text_input("Link externo da vaga *", placeholder="https://linkedin.com/...")
        
        status = st.selectbox("Status", ["Ativa", "Pausada", "Fechada"])
        
        if st.form_submit_button("✅ Publicar Vaga", use_container_width=True):
            if titulo and descricao:
                if tipo_vaga == "Externa (só link)" and not link_externo:
                    st.error("Para vaga externa, o link é obrigatório!")
                else:
                    nova_vaga = {
                        "id": len(st.session_state.vagas) + 1,
                        "titulo": titulo,
                        "descricao": descricao,
                        "tipo_vaga": tipo_vaga,
                        "local": local,
                        "tipo_contrato": tipo_contrato,
                        "salario": salario if salario else "A combinar",
                        "link_externo": link_externo,
                        "status": status,
                        "data": datetime.now().strftime("%d/%m/%Y")
                    }
                    st.session_state.vagas.append(nova_vaga)
                    st.success(f"✅ Vaga '{titulo}' publicada com sucesso!")
                    st.rerun()
            else:
                st.error("Preencha título e descrição!")

# ============================================================
# TELA: CANDIDATOS (futura integração)
# ============================================================
elif menu == "📝 Candidatos":
    st.title("📝 Candidatos Recebidos")
    if not st.session_state.candidatos:
        st.info("Nenhum candidato cadastrado ainda. Os candidatos aparecerão aqui quando enviarem currículo.")
    else:
        for i, cand in enumerate(st.session_state.candidatos):
            with st.expander(f"👤 {cand['nome']} - {cand['vaga']}"):
                st.markdown(f"**📧 E-mail:** {cand['email']}")
                st.markdown(f"**📱 Telefone:** {cand['telefone']}")
                st.markdown(f"**📍 Cidade:** {cand['cidade']}/{cand['estado']}")
                st.markdown(f"**📅 Data:** {cand['data']}")

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
        st.dataframe(df_vagas[['titulo', 'tipo_vaga', 'status']], use_container_width=True)
    else:
        st.info("Nenhuma vaga cadastrada ainda")

st.markdown("---")
st.caption("👥 SANTANA RH SOLUÇÕES - Painel Administrativo")
