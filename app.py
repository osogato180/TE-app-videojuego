import random
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="Digimon Story: Time Stranger – Analytics", page_icon="🌀", layout="wide")

# ------------------------------------------------------------------ DATA
# NOTA: los stats son valores de EJEMPLO para analitica; ajustalos con datos reales del juego.
DIGIMON = pd.DataFrame([
    # nombre, nivel, atributo, elemento, HP, ATK, DEF, INT, SPD
    ("Agumon", "Rookie", "Vacuna", "Fuego", 70, 62, 48, 40, 55),
    ("Gabumon", "Rookie", "Datos", "Hielo", 72, 58, 52, 45, 50),
    ("Patamon", "Rookie", "Vacuna", "Viento", 60, 50, 45, 60, 58),
    ("Gomamon", "Rookie", "Vacuna", "Agua", 68, 52, 50, 48, 54),
    ("Impmon", "Rookie", "Virus", "Oscuridad", 58, 60, 40, 55, 66),
    ("Greymon", "Champion", "Vacuna", "Fuego", 120, 105, 80, 60, 70),
    ("Garurumon", "Champion", "Datos", "Hielo", 110, 98, 78, 66, 95),
    ("Angemon", "Champion", "Vacuna", "Luz", 105, 95, 70, 85, 80),
    ("Devimon", "Champion", "Virus", "Oscuridad", 115, 100, 75, 80, 65),
    ("Metalgreymon", "Ultimate", "Vacuna", "Acero", 170, 150, 140, 90, 85),
    ("Seraphimon", "Mega", "Vacuna", "Luz", 220, 190, 175, 200, 150),
    ("Beelzemon", "Mega", "Virus", "Oscuridad", 215, 215, 150, 170, 190),
    ("Omnimon", "Mega", "Vacuna", "Neutro", 260, 250, 220, 190, 185),
    ("Lucemon", "Mega", "Virus", "Oscuridad", 240, 230, 190, 200, 170),
    ("Susanoomon", "Mega", "Datos", "Luz", 280, 260, 230, 210, 200),
], columns=["Digimon", "Nivel", "Atributo", "Elemento", "HP", "ATK", "DEF", "INT", "SPD"])
DIGIMON["Poder total"] = DIGIMON[["HP", "ATK", "DEF", "INT", "SPD"]].sum(axis=1)

COLORS = {"Vacuna": "#3b82f6", "Datos": "#22c55e", "Virus": "#a855f7", "Libre": "#f59e0b", "Variable": "#ec4899", "Desconocido": "#94a3b8"}

ATTRIBUTES = {
    "Vacuna": ("🛡️", "Fuerte contra Virus, debil contra Datos. Suelen ser Digimon de orden y proteccion."),
    "Datos": ("💾", "Fuerte contra Vacuna, debil contra Virus. Equilibrados y adaptables."),
    "Virus": ("☣️", "Fuerte contra Datos, debil contra Vacuna. Agresivos e impredecibles."),
    "Libre": ("🕊️", "Sin ventaja ni desventaja fija en el triangulo. Muy versatiles."),
    "Variable": ("🔀", "Atributo que cambia o se adapta; casos especiales de evolucion."),
    "Desconocido": ("❓", "Sin clasificar o de naturaleza misteriosa."),
}

CRESTS = pd.DataFrame([
    ("Valor", "Agumon", "🔥"), ("Amistad", "Gabumon", "🤝"), ("Amor", "Biyomon", "❤️"),
    ("Sinceridad", "Palmon", "🌿"), ("Conocimiento", "Tentomon", "📚"),
    ("Fiabilidad", "Gomamon", "⚓"), ("Esperanza", "Patamon", "🌟"), ("Luz", "Gatomon", "✨"),
], columns=["Emblema", "Digimon asociado", "Icono"])

ROYAL_KNIGHTS = ["Omnimon", "Gallantmon (Dukemon)", "Alphamon", "Craniamon", "Dynasmon", "Examon", "Gankoomon",
                 "Jesmon", "Magnamon", "Sleipmon", "UlforceVeedramon", "Duftmon", "Leopardmon"]
DEVAS = ["Vikaralamon", "Mihiramon", "Pajiramon", "Kumbhiramon", "Majiramon", "Indramon",
         "Sandiramon", "Antylamon", "Caturamon", "Vajramon", "Makuramon", "Pagumon/otro (varia segun fuente)"]
ANGELS = ["Seraphimon", "Ophanimon", "Cherubimon"]
DEMONS = ["Lucemon", "Leviamon", "Lilithmon", "Barbamon", "Beelzemon", "Belphemon", "Daemon"]
TITANS = ["Titamon", "Atlas (referencia mitologica)", "Olympos XII (Apollomon, Dianamon, Marsmon, Junomon...)"]
SOVEREIGNS = ["Azulongmon (Este)", "Zhuqiaomon (Sur)", "Baihumon (Oeste)", "Ebonwumon (Norte)"]

COMPUTERS = {
    "Homeos": ("🧠", "Primera computadora central; nucleo de control del equilibrio."),
    "Yggdrasil": ("🌳", "Supercomputadora que administra el Mundo Digital y su evolucion."),
    "Kunlun": ("🏔️", "Tercera computadora central, asociada al orden de la red."),
}

TYPE_MATCHUP = {"Vacuna": "Virus", "Virus": "Datos", "Datos": "Vacuna"}

# ------------------------------------------------------------------ SIDEBAR
st.sidebar.title("🌀 Digimon Story\nTime Stranger")
page = st.sidebar.radio("Menu", [
    "🏠 Inicio", "⚔️ Atributos", "📊 Analitica", "🥚 Digitama / Tamagotchi",
    "🖥️ Computadoras centrales", "👑 Caballeros, Devas y Soberanos",
    "😇😈 Angeles, Demonios y Titanes", "💎 Emblemas", "🌌 Susanoomon"])
st.sidebar.caption("Datos de stats = ejemplo. Lore basado en el canon de la franquicia.")

# ------------------------------------------------------------------ PAGES
if page == "🏠 Inicio":
    st.title("🌀 Digimon Story: Time Stranger — Panel de Analitica")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Digimon cargados", len(DIGIMON))
    c2.metric("Atributos", DIGIMON["Atributo"].nunique())
    c3.metric("Poder promedio", int(DIGIMON["Poder total"].mean()))
    c4.metric("Mas fuerte", DIGIMON.loc[DIGIMON["Poder total"].idxmax(), "Digimon"])
    st.write("Usa el menu lateral para explorar atributos, estadisticas, el Tamagotchi, las computadoras "
             "centrales y las grandes jerarquias del Mundo Digital.")
    fig = px.sunburst(DIGIMON, path=["Atributo", "Nivel", "Digimon"], values="Poder total",
                      color="Atributo", color_discrete_map=COLORS)
    st.plotly_chart(fig, use_container_width=True)

elif page == "⚔️ Atributos":
    st.title("⚔️ Tipos / Atributos")
    tabs = st.tabs([f"{ATTRIBUTES[a][0]} {a}" for a in ATTRIBUTES])
    for tab, (name, (icon, desc)) in zip(tabs, ATTRIBUTES.items()):
        with tab:
            st.subheader(f"{icon} {name}")
            st.write(desc)
            sub = DIGIMON[DIGIMON["Atributo"] == name]
            if sub.empty:
                st.info("Sin Digimon de ejemplo cargados para este atributo.")
            else:
                st.dataframe(sub, use_container_width=True, hide_index=True)
    st.markdown("**Triangulo:** Vacuna ➜ Virus ➜ Datos ➜ Vacuna (cada uno vence al siguiente).")

elif page == "📊 Analitica":
    st.title("📊 Analitica avanzada")
    f1, f2 = st.columns(2)
    attrs = f1.multiselect("Atributo", DIGIMON["Atributo"].unique(), default=list(DIGIMON["Atributo"].unique()))
    levels = f2.multiselect("Nivel", DIGIMON["Nivel"].unique(), default=list(DIGIMON["Nivel"].unique()))
    df = DIGIMON[DIGIMON["Atributo"].isin(attrs) & DIGIMON["Nivel"].isin(levels)]
    if df.empty:
        st.warning("Sin datos con esos filtros.")
        st.stop()

    t1, t2, t3, t4 = st.tabs(["Dispersion", "Radar", "Heatmap", "Simulador de batalla"])
    with t1:
        x, y = st.columns(2)
        xs = x.selectbox("Eje X", ["HP", "ATK", "DEF", "INT", "SPD"], index=1)
        ys = y.selectbox("Eje Y", ["HP", "ATK", "DEF", "INT", "SPD"], index=4)
        st.plotly_chart(px.scatter(df, x=xs, y=ys, size="Poder total", color="Atributo", text="Digimon",
                                   color_discrete_map=COLORS, hover_data=["Nivel", "Elemento"]),
                        use_container_width=True)
    with t2:
        picks = st.multiselect("Compara Digimon", df["Digimon"], default=list(df["Digimon"][:3]))
        cats = ["HP", "ATK", "DEF", "INT", "SPD"]
        fig = go.Figure()
        for n in picks:
            r = df[df["Digimon"] == n].iloc[0]
            fig.add_trace(go.Scatterpolar(r=[r[c] for c in cats] + [r[cats[0]]], theta=cats + [cats[0]],
                                          fill="toself", name=n))
        st.plotly_chart(fig, use_container_width=True)
    with t3:
        piv = df.groupby(["Atributo", "Nivel"])["Poder total"].mean().unstack().fillna(0)
        st.plotly_chart(px.imshow(piv, text_auto=".0f", color_continuous_scale="Viridis", aspect="auto"),
                        use_container_width=True)
    with t4:
        a, b = st.columns(2)
        d1 = a.selectbox("Digimon A", DIGIMON["Digimon"], index=0)
        d2 = b.selectbox("Digimon B", DIGIMON["Digimon"], index=11)
        if st.button("⚔️ Simular 1000 combates"):
            A = DIGIMON[DIGIMON["Digimon"] == d1].iloc[0]
            B = DIGIMON[DIGIMON["Digimon"] == d2].iloc[0]
            def mult(x, y):
                return 1.25 if TYPE_MATCHUP.get(x) == y else 0.8 if TYPE_MATCHUP.get(y) == x else 1.0
            pa = A["Poder total"] * mult(A["Atributo"], B["Atributo"])
            pb = B["Poder total"] * mult(B["Atributo"], A["Atributo"])
            wins = sum(random.gauss(pa, 40) > random.gauss(pb, 40) for _ in range(1000))
            st.metric(f"Victorias de {d1}", f"{wins/10:.1f}%")
            st.metric(f"Victorias de {d2}", f"{(1000-wins)/10:.1f}%")
            st.caption("Modelo simple: poder total x ventaja de atributo + ruido aleatorio.")

elif page == "🥚 Digitama / Tamagotchi":
    st.title("🥚 Crianza digital (estilo Tamagotchi)")
    ss = st.session_state
    ss.setdefault("pet", {"Hambre": 50, "Felicidad": 50, "Energia": 50, "Disciplina": 50, "Edad": 0})
    ss.setdefault("log", [])
    pet = ss.pet
    stage = ["Digitama 🥚", "Baby 🐣", "Rookie 🦖", "Champion 🐉", "Ultimate 🔥", "Mega 👑"][min(pet["Edad"] // 3, 5)]
    st.subheader(f"Etapa: {stage}")
    cols = st.columns(4)
    for c, k in zip(cols, ["Hambre", "Felicidad", "Energia", "Disciplina"]):
        c.write(k)
        c.progress(max(0, min(100, pet[k])) / 100)
    actions = {"🍖 Alimentar": {"Hambre": -20, "Felicidad": 5}, "🎮 Jugar": {"Felicidad": 15, "Energia": -15, "Hambre": 10},
               "😴 Dormir": {"Energia": 25, "Hambre": 5}, "📚 Entrenar": {"Disciplina": 15, "Energia": -15, "Hambre": 10}}
    bc = st.columns(4)
    for col, (label, eff) in zip(bc, actions.items()):
        if col.button(label, use_container_width=True):
            for k, v in eff.items():
                pet[k] = max(0, min(100, pet[k] + v))
            pet["Edad"] += 1
            ss.log.append({"Turno": pet["Edad"], "Accion": label, **{k: pet[k] for k in ["Hambre", "Felicidad", "Energia", "Disciplina"]}})
            st.rerun()
    if st.button("🔄 Reiniciar"):
        del ss["pet"], ss["log"]
        st.rerun()
    if ss.log:
        st.plotly_chart(px.line(pd.DataFrame(ss.log), x="Turno", y=["Hambre", "Felicidad", "Energia", "Disciplina"]),
                        use_container_width=True)

elif page == "🖥️ Computadoras centrales":
    st.title("🖥️ Las 3 computadoras centrales")
    st.write("Segun tu planteamiento, estan dominadas por la red de **Homeostasis**, el sistema que mantiene el equilibrio del Mundo Digital.")
    for col, (n, (ic, d)) in zip(st.columns(3), COMPUTERS.items()):
        with col:
            st.markdown(f"### {ic} {n}")
            st.write(d)
    fig = go.Figure(go.Sankey(
        node=dict(label=["Homeostasis", "Homeos", "Yggdrasil", "Kunlun", "Mundo Digital"], pad=20),
        link=dict(source=[0, 0, 0, 1, 2, 3], target=[1, 2, 3, 4, 4, 4], value=[1, 1, 1, 1, 1, 1])))
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Los roles exactos dentro del juego conviene verificarlos; edita las descripciones en COMPUTERS.")

elif page == "👑 Caballeros, Devas y Soberanos":
    st.title("👑 Jerarquias del Mundo Digital")
    t1, t2, t3 = st.tabs(["Caballeros Reales", "12 Devas (Shinsho)", "Cuatro Soberanos"])
    t1.write(" • ".join(ROYAL_KNIGHTS)); t1.caption("La lista varia segun la fuente (son 13 o mas).")
    t2.write(" • ".join(DEVAS)); t2.caption("Lista orientativa; revisa la 12ª segun la fuente.")
    t3.write(" • ".join(SOVEREIGNS))

elif page == "😇😈 Angeles, Demonios y Titanes":
    st.title("Angeles, Demonios y Titanes")
    c1, c2, c3 = st.columns(3)
    c1.subheader("😇 3 Grandes Angeles"); c1.write("\n".join(f"- {x}" for x in ANGELS))
    c2.subheader("😈 7 Grandes Demonios"); c2.write("\n".join(f"- {x}" for x in DEMONS))
    c3.subheader("🗿 Titanes"); c3.write("\n".join(f"- {x}" for x in TITANS))
    st.plotly_chart(px.pie(names=["Angeles (3)", "Demonios (7)"], values=[3, 7],
                           color_discrete_sequence=["#fde047", "#7c3aed"]), use_container_width=True)

elif page == "💎 Emblemas":
    st.title("💎 Los 8 emblemas")
    st.dataframe(CRESTS, use_container_width=True, hide_index=True)
    st.plotly_chart(px.pie(CRESTS, names="Emblema", hole=0.5), use_container_width=True)

elif page == "🌌 Susanoomon":
    st.title("🌌 Susanoomon")
    st.write("Fusion legendaria de los 10 Guerreros Legendarios (Digimon Frontier), "
             "una de las existencias mas poderosas de la franquicia.")
    st.plotly_chart(px.bar(DIGIMON.sort_values("Poder total"), x="Poder total", y="Digimon", orientation="h",
                           color="Atributo", color_discrete_map=COLORS), use_container_width=True)
