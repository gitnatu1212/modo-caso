import streamlit as st

st.set_page_config(
    page_title="MODO CASO",
    page_icon="🔎",
    layout="centered"
)

st.set_page_config(
    page_title="MODO CASO",
    page_icon="🔎",
    layout="centered"
)

# =========================================================
# IDENTIDADE VISUAL — MODO CASO
# =========================================================

st.markdown("""
<style>

/* FUNDO GERAL */
.stApp {
    background:
        radial-gradient(circle at 10% 10%, rgba(0, 229, 255, 0.08), transparent 25%),
        radial-gradient(circle at 90% 80%, rgba(139, 92, 246, 0.08), transparent 25%),
        #07111c;
    color: #F4F7FA;
}

/* ÁREA PRINCIPAL */
.block-container {
    max-width: 780px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

/* TEXTOS */
h1, h2, h3 {
    color: #F4F7FA !important;
    font-weight: 800 !important;
}

p, label, .stMarkdown {
    color: #DCE6EE;
}

/* BOTÕES */
.stButton > button {
    width: 100%;
    min-height: 52px;
    border-radius: 12px;
    border: 1px solid #20D9F5;
    background: linear-gradient(90deg, #15D9F4, #7657FF);
    color: #061019;
    font-weight: 800;
    letter-spacing: 0.3px;
    transition: 0.2s;
}

.stButton > button:hover {
    border-color: #FFFFFF;
    color: #FFFFFF;
    transform: translateY(-1px);
}

/* CAMPOS */
.stTextInput input {
    background-color: #101E2B !important;
    color: #FFFFFF !important;
    border: 1px solid #315064 !important;
    border-radius: 10px !important;
}

div[data-baseweb="select"] > div {
    background-color: #101E2B !important;
    color: #FFFFFF !important;
    border-color: #315064 !important;
}

/* RADIO */
div[role="radiogroup"] {
    background: #0D1A26;
    border: 1px solid #1F3B4D;
    border-radius: 14px;
    padding: 14px;
}

/* BARRA DE PROGRESSO */
.stProgress > div > div > div > div {
    background: linear-gradient(
        90deg,
        #20D9F5,
        #7657FF
    );
}

/* ALERTAS / CARDS */
div[data-testid="stAlert"] {
    border-radius: 14px;
    border: 1px solid #294A5D;
}

/* MOBILE */
@media (max-width: 600px) {

    .block-container {
        padding: 1.2rem 1rem 3rem 1rem;
    }

    h1 {
        font-size: 2rem !important;
    }

    h2 {
        font-size: 1.55rem !important;
    }

    h3 {
        font-size: 1.25rem !important;
    }

    .stButton > button {
        min-height: 56px;
        font-size: 0.95rem;
    }
}

</style>
""", unsafe_allow_html=True)


# ---------- BANCO DE DADOS ----------
import sqlite3

def conectar_banco():
    conn = sqlite3.connect("modo_caso.db")
    conn.row_factory = sqlite3.Row
    return conn
def criar_tabelas():
    conn = conectar_banco()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS turmas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            escola TEXT NOT NULL,
            serie TEXT NOT NULL,
            turma TEXT NOT NULL,
            turno TEXT NOT NULL,
            caso TEXT NOT NULL,
            quantidade_equipes INTEGER NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS equipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            turma_id INTEGER NOT NULL,
            nome TEXT NOT NULL,
            codigo TEXT NOT NULL UNIQUE,
            FOREIGN KEY (turma_id) REFERENCES turmas(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS progresso (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            equipe_codigo TEXT NOT NULL,
            etapa INTEGER NOT NULL,
            concluido INTEGER DEFAULT 0
        )
    """)

    conn.commit()
    conn.close()

criar_tabelas()
def salvar_progresso(codigo_equipe, etapa, concluido=0):
    conn = conectar_banco()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id FROM progresso WHERE equipe_codigo = ?",
        (codigo_equipe,)
    )

    registro = cursor.fetchone()

    if registro:
        cursor.execute(
            """
            UPDATE progresso
            SET etapa = ?, concluido = ?
            WHERE equipe_codigo = ?
            """,
            (etapa, concluido, codigo_equipe)
        )
    else:
        cursor.execute(
            """
            INSERT INTO progresso (equipe_codigo, etapa, concluido)
            VALUES (?, ?, ?)
            """,
            (codigo_equipe, etapa, concluido)
        )

    conn.commit()
    conn.close()
    

# ---------- ESTADO ----------
if "turma" not in st.session_state:
    st.session_state.turma = None

if "jogando" not in st.session_state:
    st.session_state.jogando = False

if "etapa" not in st.session_state:
    st.session_state.etapa = 1

# ---------- CABEÇALHO ----------
st.title("🔎 MODO CASO")
st.caption("Investigar. Aprender. Transformar.")
st.divider()

perfil = st.radio(
    "Como você deseja entrar?",
    ["👩🏾‍🏫 Professor", "🔎 Equipe"],
    horizontal=True
)

# =========================================================
# PROFESSOR
# =========================================================

if perfil == "👩🏾‍🏫 Professor":

    st.header("Painel do Professor")
    st.write("Crie a turma e prepare a investigação.")

    escola = st.text_input("Nome da escola")

    serie = st.selectbox(
        "Série",
        ["1º ano EM", "2º ano EM", "3º ano EM"]
    )

    turma = st.text_input("Turma", placeholder="Ex.: 2001")

    turno = st.selectbox(
        "Turno",
        ["Manhã", "Tarde", "Noite"]
    )

    equipes = st.number_input(
        "Quantidade de equipes",
        min_value=2,
        max_value=10,
        value=6
    )

    caso = st.selectbox(
        "Escolha o caso",
        [
            "🔐 Não Cai Nessa",
            "🧮 A Conta Não Fecha",
            "📰 Quem Disse Isso?"
        ]
    )

    if st.button("CRIAR TURMA", type="primary"):

        if escola and turma:

            codigos = [
                f"{turma}-MC{i:02d}"
                for i in range(1, int(equipes) + 1)
            ]
            st.session_state.turma = {
                            "escola": escola,
                            "serie": serie,
                            "turma": turma,
                            "turno": turno,
                            "caso": caso,
                            "equipes": int(equipes),
                            
                            }                

            # Salvar turma no banco de dados
            conn = conectar_banco()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO turmas
                (escola, serie, turma, turno, caso, quantidade_equipes)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (escola, serie, turma, turno, caso, int(equipes)))

            turma_id = cursor.lastrowid

            for i, codigo in enumerate(codigos, start=1):
                cursor.execute("""
                    INSERT INTO equipes (turma_id, nome, codigo)
                    VALUES (?, ?, ?)
                """, (turma_id, f"Equipe {i}", codigo))

            conn.commit()
            conn.close()

            st.success("✓ TURMA CRIADA")

        else:
            st.warning("Preencha o nome da escola e da turma.")

    if st.session_state.turma:

        dados = st.session_state.turma

        st.subheader("Turma pronta para jogar")

        st.write(f"🏫 **{dados['escola']}**")
        st.write(
            f"🎓 {dados['serie']} • "
            f"Turma {dados['turma']} • "
            f"{dados['turno']}"
        )

        st.write(f"🎮 **Caso:** {dados['caso']}")

        st.subheader("Equipes")

conn = conectar_banco()
cursor = conn.cursor()

cursor.execute(
    "SELECT nome, codigo FROM equipes WHERE turma_id = (SELECT MAX(id) FROM turmas)"
)
equipes_salvas = cursor.fetchall()

conn.close()

# Resumo geral da turma
total_equipes = len(equipes_salvas)
em_andamento = 0
concluidas = 0
soma_progresso = 0

for equipe in equipes_salvas:
    conn = conectar_banco()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT etapa, concluido
        FROM progresso
        WHERE equipe_codigo = ?
        """,
        (equipe["codigo"],)
    )

    progresso_resumo = cursor.fetchone()
    conn.close()

    if progresso_resumo:
        etapa = progresso_resumo["etapa"]
        soma_progresso += etapa

        if progresso_resumo["concluido"]:
            concluidas += 1
        else:
            em_andamento += 1

# Calcula o progresso geral da turma
if total_equipes > 0:
    percentual = int(
        (soma_progresso / (total_equipes * 6)) * 100
    )
else:
    percentual = 0

col1, col2, col3 = st.columns(3)

col1.metric("👥 Equipes", total_equipes)
col2.metric("🟡 Em andamento", em_andamento)
col3.metric("🟢 Concluídas", concluidas)

st.write(f"**Progresso geral da turma: {percentual}%**")
st.progress(percentual / 100)


# Painel de acompanhamento das equipes
st.subheader("📊 Acompanhamento da investigação")

nomes_etapas = {
    1: "Caso aberto",
    2: "Pista 1",
    3: "Missão fora da tela",
    4: "Pista 2",
    5: "Momento Professor",
    6: "Caso resolvido"
}

for equipe in equipes_salvas:
    codigo = equipe["codigo"]

    conn = conectar_banco()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT etapa, concluido
        FROM progresso
        WHERE equipe_codigo = ?
        """,
        (codigo,)
    )

    progresso = cursor.fetchone()
    conn.close()

    if not progresso:
        status = "⚪ Não iniciou"
    elif progresso["concluido"]:
        status = "🟢 Caso resolvido"
    else:
        etapa = progresso["etapa"]
        status = f"🟡 Etapa {etapa}/6 — {nomes_etapas.get(etapa, 'Em andamento')}"

    st.write(f"**{equipe['nome']}** — {status}")

for equipe in equipes_salvas:
    st.info(f"🔎 {equipe['nome']} • Código: {equipe['codigo']}")
# =========================================================
# EQUIPE
# =========================================================

else:

    st.header("Entrar na investigação")

    if not st.session_state.jogando:

        st.write(
            "Você não precisa criar conta. "
            "Use o código fornecido pelo professor."
        )

        codigo = st.text_input(
            "Código da equipe",
            placeholder="Ex.: MC01"
        ).strip().upper()

    if st.button("ENTRAR NO CASO", type="primary"):

        conn = conectar_banco()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT equipes.id, equipes.nome, equipes.codigo,
                turmas.escola, turmas.serie, turmas.turma,
                turmas.turno, turmas.caso
            FROM equipes
            JOIN turmas ON equipes.turma_id = turmas.id
            WHERE equipes.codigo = ?
        """, (codigo,))

        equipe = cursor.fetchone()
        conn.close()

        if equipe is None:
            st.error("❌ Código de equipe inválido.")
        else:
            st.session_state.codigo_equipe = codigo
            st.session_state.turma = {
                "escola": equipe["escola"],
                "serie": equipe["serie"],
                "turma": equipe["turma"],
                "turno": equipe["turno"],
                "caso": equipe["caso"],
            }
        # Recupera o progresso salvo da equipe
        conn = conectar_banco()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT etapa, concluido FROM progresso WHERE equipe_codigo = ?",
            (codigo,)
        )

        progresso = cursor.fetchone()
        conn.close()

        st.session_state.jogando = True

        if progresso and not progresso["concluido"]:
            st.session_state.etapa = progresso["etapa"]
        else:
            st.session_state.etapa = 1

        st.rerun()

    # =====================================================
    # JOGO
    # =====================================================

    if st.session_state.get("jogando", False):

        st.caption(
            f"Equipe {st.session_state.codigo_equipe} • "
            f"{st.session_state.turma['turma']}"
        )

        st.progress(st.session_state.etapa / 6)

        # ---------- ETAPA 1 ----------
        if st.session_state.etapa == 1:

            st.success("🚨 CASO ABERTO")
            st.header("🔐 NÃO CAI NESSA")

            st.write(
                "Uma mensagem começou a circular entre estudantes da escola."
            )

            st.markdown("""
<div style="
    background:#102331;
    border:1px solid #2DD4F7;
    border-radius:18px;
    padding:18px;
    margin:18px 0;
    box-shadow:0 8px 24px rgba(0,0,0,0.25);
">

<div style="
    font-size:12px;
    color:#9FB3C8;
    margin-bottom:10px;
">
📱 MENSAGEM RECEBIDA • 10:42
</div>

<div style="
    background:#173545;
    border-radius:16px;
    padding:16px;
    color:white;
    line-height:1.6;
">

🎁 <b>PARABÉNS!</b><br>
Você ganhou <b>R$ 500 em créditos.</b><br>
Resgate agora antes que expire.<br><br>

<span style="
    color:#43DDF8;
    text-decoration:underline;
">
premio-estudante-gratis.xyz
</span>

</div>

<div style="
    margin-top:12px;
    color:#FFD166;
    font-weight:700;
">
⚠️ NÃO CLIQUE. INVESTIGUE.
</div>

</div>
""", unsafe_allow_html=True)

            

            st.write(
                "**Missão:** descubram se a mensagem é confiável "
                "antes que alguém clique."
            )

        if st.session_state.etapa == 1 and st.button("ANALISAR A MENSAGEM →", type="primary"):
            st.session_state.etapa = 2
            salvar_progresso(st.session_state.codigo_equipe, 2)
            st.rerun()

        # ---------- ETAPA 2 ----------
        elif st.session_state.etapa == 2:

            st.header("🔎 PISTA 1 — Observe antes de clicar")

            resposta = st.radio(
                "Qual detalhe merece mais atenção?",
                [
                    "O emoji de presente",
                    "O endereço do link",
                    "O valor de R$ 500",
                    "A palavra PARABÉNS"
                ],
                index=None
            )

            if st.button("CONFIRMAR RESPOSTA"):

                if resposta == "O endereço do link":
                    st.success(
                        "✓ BOA INVESTIGAÇÃO! "
                        "O endereço estranho é um forte sinal de alerta."
                    )
                    st.session_state.etapa = 3
                    salvar_progresso(st.session_state.codigo_equipe, 3)
                    st.rerun()

                elif resposta:
                    st.error(
                        "✕ Ainda não. Observe a mensagem novamente. "
                        "Qual elemento pode indicar para onde você será levado?"
                    )

                else:
                    st.warning("Escolha uma resposta.")

        # ---------- ETAPA 3 ----------
        elif st.session_state.etapa == 3:

            st.header("📵 MISSÃO FORA DA TELA")

            st.write(
                "Agora o celular precisa sair do centro da atividade."
            )

            st.info(
                "Coloque o aparelho sobre a mesa.\n\n"
                "**Em equipe, discutam por 2 minutos:**\n\n"
                "Quais sinais vocês verificariam antes de abrir "
                "um link recebido por mensagem?"
            )

            st.write(
                "Quando todos tiverem apresentado pelo menos uma ideia, "
                "voltem ao aparelho."
            )

            if st.button("EQUIPE PRONTA →", type="primary"):
                st.session_state.etapa = 4
                salvar_progresso(st.session_state.codigo_equipe, 4)
                st.rerun()

        # ---------- ETAPA 4 ----------
        elif st.session_state.etapa == 4:

            st.header("🧩 PISTA 2 — Tome uma decisão")

            resposta = st.radio(
                "Qual é a atitude mais segura?",
                [
                    "Abrir rapidamente para conferir",
                    "Encaminhar para um colega testar",
                    "Não clicar e verificar a informação por um canal oficial",
                    "Responder à mensagem perguntando se é verdadeira"
                ],
                index=None
            )

            if st.button("DECIDIR"):

                if resposta == (
                    "Não clicar e verificar a informação por um canal oficial"
                ):
                    st.success("✓ DECISÃO SEGURA.")
                    st.session_state.etapa = 5
                    salvar_progresso(st.session_state.codigo_equipe, 5)
                    st.rerun()

                elif resposta:
                    st.error(
                        "✕ Essa escolha ainda pode colocar alguém em risco. "
                        "Tentem novamente."
                    )

                else:
                    st.warning("Escolha uma resposta.")

        # ---------- ETAPA 5 ----------
        elif st.session_state.etapa == 5:

            st.header("👩🏾‍🏫 MOMENTO PROFESSOR")

            st.info(
                "**Investigação pausada.**\n\n"
                "Professor, provoque a turma:\n\n"
                "**“Por que uma mensagem enviada por alguém conhecido "
                "também pode ser perigosa?”**"
            )

            st.write(
                "Conversem brevemente antes de liberar a etapa final."
            )

            if st.button("CONTINUAR INVESTIGAÇÃO →", type="primary"):
                st.session_state.etapa = 6
                salvar_progresso(st.session_state.codigo_equipe, 6)
                st.rerun()

        # ---------- ETAPA 6 ----------
        elif st.session_state.etapa == 6:

            st.success("✓ CASO RESOLVIDO")
            st.header("🛡️ NÃO CAIU NESSA!")

            st.write(
                "A equipe identificou os sinais de risco e evitou "
                "uma possível tentativa de phishing."
            )

            st.subheader("O que levamos deste caso?")

            st.write(
                "🔎 Observe o endereço antes de clicar.\n\n"
                "🛡️ Verifique informações em canais oficiais.\n\n"
                "🤝 Não encaminhe conteúdo suspeito para outras pessoas."
            )

            st.info(
                "🔑 **CHAVE DA EQUIPE DESBLOQUEADA:** SEGURA"
            )

if st.button("ENCERRAR CASO"):
    salvar_progresso(
        st.session_state.codigo_equipe,
        6,
        1
    )

    st.session_state.jogando = False
    st.session_state.etapa = 1
    st.rerun()
    
                