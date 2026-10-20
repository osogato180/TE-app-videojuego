import random, zlib
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="Digimon Story: Time Stranger", page_icon="🌀", layout="wide")

# ============================== DATOS ==============================
# Formato: Nombre|Nivel|Atributo|Elemento  (referencial: corrige lo que difiera del juego)
RAW = """
Botamon|Baby|Sin datos|Oscuridad;Punimon|Baby|Sin datos|Neutro;Poyomon|Baby|Sin datos|Luz;Nyaromon|Baby|Sin datos|Luz;Kuramon|Baby|Desconocido|Oscuridad;Pagumon|Baby|Virus|Oscuridad;Yuramon|Baby|Sin datos|Planta;Pichimon|Baby|Sin datos|Agua
Agumon|Rookie|Vacuna|Fuego;Gabumon|Rookie|Datos|Hielo;Biyomon|Rookie|Vacuna|Viento;Palmon|Rookie|Datos|Planta;Tentomon|Rookie|Vacuna|Electrico;Gomamon|Rookie|Datos|Agua;Patamon|Rookie|Datos|Viento;Salamon|Rookie|Vacuna|Neutro;Guilmon|Rookie|Virus|Fuego;Terriermon|Rookie|Vacuna|Viento;Renamon|Rookie|Datos|Neutro;Veemon|Rookie|Libre|Neutro;Hawkmon|Rookie|Vacuna|Viento;Armadillomon|Rookie|Datos|Tierra;Impmon|Rookie|Virus|Oscuridad;Betamon|Rookie|Virus|Agua;Elecmon|Rookie|Datos|Electrico;Gazimon|Rookie|Virus|Tierra;Hagurumon|Rookie|Virus|Acero;DemiDevimon|Rookie|Virus|Oscuridad;Goburimon|Rookie|Virus|Tierra;Kunemon|Rookie|Virus|Planta;Shoutmon|Rookie|Variable|Fuego;Hudiemon|Rookie|Desconocido|Viento;Dorumon|Rookie|Datos|Fuego;Lucemon|Rookie|Libre|Luz
Greymon|Champion|Vacuna|Fuego;Garurumon|Champion|Vacuna|Hielo;Birdramon|Champion|Libre|Fuego;Togemon|Champion|Datos|Planta;Kabuterimon|Champion|Vacuna|Electrico;Ikkakumon|Champion|Datos|Agua;Angemon|Champion|Vacuna|Luz;Devimon|Champion|Virus|Oscuridad;Gatomon|Champion|Vacuna|Luz;Airdramon|Champion|Datos|Viento;Leomon|Champion|Vacuna|Fuego;Meramon|Champion|Datos|Fuego;Seadramon|Champion|Datos|Agua;Numemon|Champion|Virus|Tierra;Ogremon|Champion|Virus|Tierra;Growlmon|Champion|Virus|Fuego;Kyubimon|Champion|Datos|Fuego;Wizardmon|Champion|Datos|Oscuridad;Flamedramon|Champion|Libre|Fuego;Ankylomon|Champion|Vacuna|Tierra;Mojyamon|Champion|Datos|Hielo;Frigimon|Champion|Vacuna|Hielo;Monochromon|Champion|Datos|Fuego;Tyrannomon|Champion|Datos|Fuego;Shellmon|Champion|Datos|Agua;Andromon|Champion|Vacuna|Acero;Gargomon|Champion|Vacuna|Viento;Exveemon|Champion|Vacuna|Viento;Stingmon|Champion|Virus|Viento;Dobermon|Champion|Virus|Oscuridad;Sorcerymon|Champion|Datos|Oscuridad
MetalGreymon|Ultimate|Virus|Acero;WereGarurumon|Ultimate|Vacuna|Hielo;Garudamon|Ultimate|Vacuna|Fuego;Lillymon|Ultimate|Datos|Planta;MegaKabuterimon|Ultimate|Vacuna|Electrico;Zudomon|Ultimate|Datos|Agua;Angewomon|Ultimate|Vacuna|Luz;SkullGreymon|Ultimate|Virus|Oscuridad;MetalMamemon|Ultimate|Datos|Acero;Myotismon|Ultimate|Virus|Oscuridad;Cherrymon|Ultimate|Virus|Planta;Etemon|Ultimate|Virus|Oscuridad;Rapidmon|Ultimate|Vacuna|Acero;Taomon|Ultimate|Datos|Neutro;MarineAngemon|Ultimate|Vacuna|Agua;WarGrowlmon|Ultimate|Vacuna|Fuego;MegaSeadramon|Ultimate|Datos|Agua;Silphymon|Ultimate|Vacuna|Viento;Cyberdramon|Ultimate|Virus|Acero;Knightmon|Ultimate|Datos|Acero;Shakkoumon|Ultimate|Vacuna|Acero;Okuwamon|Ultimate|Virus|Planta;Rosemon|Ultimate|Datos|Planta;Phantomon|Ultimate|Virus|Oscuridad;Mamemon|Ultimate|Datos|Neutro;Vikaralamon|Ultimate|Datos|Tierra;Mihiramon|Ultimate|Datos|Tierra;Sandiramon|Ultimate|Datos|Tierra
Omnimon|Mega|Vacuna|Neutro;WarGreymon|Mega|Vacuna|Fuego;MetalGarurumon|Mega|Datos|Hielo;Seraphimon|Mega|Vacuna|Luz;Ophanimon|Mega|Vacuna|Luz;Cherubimon|Mega|Vacuna|Luz;Lucemon Satan|Mega|Virus|Oscuridad;Leviamon|Mega|Virus|Agua;Lilithmon|Mega|Virus|Oscuridad;Barbamon|Mega|Datos|Oscuridad;Beelzemon|Mega|Virus|Oscuridad;Belphemon|Mega|Virus|Oscuridad;Daemon|Mega|Virus|Oscuridad;Gallantmon|Mega|Vacuna|Fuego;Alphamon|Mega|Virus|Oscuridad;Craniamon|Mega|Datos|Tierra;Dynasmon|Mega|Datos|Viento;Examon|Mega|Vacuna|Fuego;Gankoomon|Mega|Datos|Neutro;Jesmon|Mega|Vacuna|Luz;Magnamon|Mega|Vacuna|Acero;Sleipmon|Mega|Datos|Viento;UlforceVeedramon|Mega|Vacuna|Luz;Duftmon|Mega|Vacuna|Luz;Susanoomon|Mega|Libre|Luz;Apocalymon|Mega|Virus|Oscuridad;Millenniummon|Mega|Virus|Oscuridad;Imperialdramon|Mega|Vacuna|Neutro;MegaGargomon|Mega|Vacuna|Acero;Machinedramon|Mega|Virus|Acero;Piedmon|Mega|Virus|Oscuridad;Puppetmon|Mega|Virus|Planta;AncientGreymon|Mega|Libre|Fuego;Ouryumon|Mega|Variable|Fuego;Chaosmon|Mega|Variable|Oscuridad;Azulongmon|Mega|Libre|Viento;Zhuqiaomon|Mega|Libre|Fuego;Baihumon|Mega|Libre|Electrico;Ebonwumon|Mega|Libre|Tierra;Armageddemon|Mega|Desconocido|Oscuridad;Dagomon|Mega|Sin datos|Agua
"""
rows = [r.split("|") for r in RAW.replace("\n", ";").split(";") if r.strip()]
df = pd.DataFrame(rows, columns=["Digimon", "Nivel", "Atributo", "Elemento"])
LEVELS = ["Baby", "Rookie", "Champion", "Ultimate", "Mega"]
ATTRS = ["Vacuna", "Datos", "Virus", "Libre", "Variable", "Desconocido", "Sin datos"]
COLORS = {"Vacuna": "#3b82f6", "Datos": "#22c55e", "Virus": "#a855f7", "Libre": "#f59e0b",
          "Variable": "#ec4899", "Desconocido": "#94a3b8", "Sin datos": "#475569"}
BASE = {"Baby": 20, "Rookie": 60, "Champion": 110, "Ultimate": 170, "Mega": 240}

# Stats ESTIMADOS (simulados y reproducibles por nombre), no son los del juego.
def mk_stats(r):
    g = random.Random(zlib.crc32(r.Digimon.encode())); b = BASE[r.Nivel]
    return pd.Series({s: int(b * g.uniform(0.7, 1.3) * m) for s, m in
                      zip(["HP", "ATK", "DEF", "INT", "SPD"], [1.2, 1, 0.9, 0.9, 0.9])})
df = pd.concat([df, df.apply(mk_stats, axis=1)], axis=1)
STATS = ["HP", "ATK", "DEF", "INT", "SPD"]
df["Poder"] = df[STATS].sum(axis=1)
df["Nivel"] = pd.Categorical(df["Nivel"], LEVELS, ordered=True)
TRI = {"Vacuna": "Virus", "Virus": "Datos", "Datos": "Vacuna"}

# ============================== MENU ==============================
st.sidebar.title("🌀 Digimon Story\nTime Stranger")
page = st.sidebar.radio("Menu", ["🏠 Inicio", "⚔️ Atributos", "📊 Analitica avanzada", "📜 Historia"])
st.sidebar.caption(f"{len(df)} Digimon cargados. Stats = estimados para analitica; atributo/elemento referenciales.")

# ============================== INICIO ==============================
if page == "🏠 Inicio":
    st.title("🌀 Digimon Story: Time Stranger")
    st.caption("Panel de exploracion y analitica del Mundo Digital")
    k = st.columns(5)
    k[0].metric("Digimon", len(df)); k[1].metric("Atributos", df.Atributo.nunique())
    k[2].metric("Elementos", df.Elemento.nunique()); k[3].metric("Poder medio", int(df.Poder.mean()))
    k[4].metric("Mas poderoso", df.loc[df.Poder.idxmax(), "Digimon"])
    c1, c2 = st.columns([3, 2])
    with c1:
        st.plotly_chart(px.sunburst(df, path=["Atributo", "Nivel", "Digimon"], values="Poder", color="Atributo",
                                    color_discrete_map=COLORS, title="Jerarquia Atributo > Nivel > Digimon"),
                        use_container_width=True)
    with c2:
        cnt = df.Atributo.value_counts().reindex(ATTRS).reset_index()
        cnt.columns = ["Atributo", "Cantidad"]
        st.plotly_chart(px.bar(cnt, x="Atributo", y="Cantidad", color="Atributo", color_discrete_map=COLORS,
                               text="Cantidad", title="Digimon por atributo"), use_container_width=True)
    c3, c4 = st.columns(2)
    c3.plotly_chart(px.treemap(df, path=["Elemento", "Atributo"], color="Elemento", title="Elementos"),
                    use_container_width=True)
    top = df.nlargest(10, "Poder")[["Digimon", "Nivel", "Atributo", "Elemento", "Poder"]]
    c4.subheader("🏆 Top 10 por poder"); c4.dataframe(top, hide_index=True, use_container_width=True)
    st.subheader("🎲 Digimon al azar")
    if st.button("Sacar otro") or "spot" not in st.session_state:
        st.session_state.spot = df.sample(1).iloc[0]
    s = st.session_state.spot
    st.info(f"**{s.Digimon}** — {s.Nivel} · {s.Atributo} · {s.Elemento} · Poder estimado {s.Poder}")

# ============================== ATRIBUTOS ==============================
elif page == "⚔️ Atributos":
    st.title("⚔️ Explorador de Digimon")
    cols = st.columns(len(ATTRS))
    for c, a in zip(cols, ATTRS):
        c.metric(a, int((df.Atributo == a).sum()))
    f = st.columns(4)
    q = f[0].text_input("🔎 Nombre")
    fa = f[1].multiselect("Atributo", ATTRS)
    fe = f[2].multiselect("Elemento", sorted(df.Elemento.unique()))
    fn = f[3].multiselect("Nivel", LEVELS)
    v = df.copy()
    if q: v = v[v.Digimon.str.contains(q, case=False)]
    if fa: v = v[v.Atributo.isin(fa)]
    if fe: v = v[v.Elemento.isin(fe)]
    if fn: v = v[v.Nivel.isin(fn)]
    st.write(f"**{len(v)}** resultados")
    st.dataframe(v.sort_values(["Nivel", "Digimon"]), hide_index=True, use_container_width=True, height=480,
                 column_config={"Poder": st.column_config.ProgressColumn("Poder", min_value=0, max_value=int(df.Poder.max()))})
    st.download_button("⬇️ Descargar CSV", v.to_csv(index=False).encode(), "digimon.csv")
    st.markdown("**Triangulo:** Vacuna ➜ Virus ➜ Datos ➜ Vacuna. Libre, Variable, Desconocido y Sin datos quedan fuera del triangulo.")
    if len(v):
        st.plotly_chart(px.histogram(v, x="Nivel", color="Atributo", barmode="group", color_discrete_map=COLORS,
                                     category_orders={"Nivel": LEVELS}), use_container_width=True)

# ============================== ANALITICA ==============================
elif page == "📊 Analitica avanzada":
    st.title("📊 Analitica avanzada")
    fa = st.multiselect("Filtrar atributos", ATTRS, default=ATTRS)
    d = df[df.Atributo.isin(fa)]
    if d.empty: st.warning("Sin datos."); st.stop()
    t = st.tabs(["Distribuciones", "Correlacion y PCA", "Clusters", "Comparador", "Rankings", "Simulador"])
    with t[0]:
        m = st.selectbox("Estadistica", STATS + ["Poder"], index=5)
        st.plotly_chart(px.box(d, x="Nivel", y=m, color="Atributo", color_discrete_map=COLORS,
                               category_orders={"Nivel": LEVELS}), use_container_width=True)
        st.plotly_chart(px.violin(d, x="Elemento", y=m, color="Elemento", box=True), use_container_width=True)
        piv = d.pivot_table(index="Elemento", columns="Atributo", values=m, aggfunc="mean")
        st.plotly_chart(px.imshow(piv, text_auto=".0f", aspect="auto", color_continuous_scale="Viridis",
                                  title=f"Media de {m}: Elemento x Atributo"), use_container_width=True)
    with t[1]:
        st.plotly_chart(px.imshow(d[STATS].corr(), text_auto=".2f", color_continuous_scale="RdBu_r",
                                  zmin=-1, zmax=1, title="Correlacion de stats"), use_container_width=True)
        X = (d[STATS] - d[STATS].mean()) / d[STATS].std()
        U, S, Vt = np.linalg.svd(X.values, full_matrices=False)
        p = pd.DataFrame(U[:, :2] * S[:2], columns=["PC1", "PC2"], index=d.index).join(d[["Digimon", "Atributo", "Nivel"]])
        st.plotly_chart(px.scatter(p, x="PC1", y="PC2", color="Atributo", symbol="Nivel", hover_name="Digimon",
                                   color_discrete_map=COLORS, title="PCA de stats"), use_container_width=True)
        st.caption(f"Varianza explicada PC1+PC2: {(S[:2]**2).sum()/(S**2).sum():.0%}")
    with t[2]:
        k = st.slider("Numero de clusters (K-Means)", 2, 8, 4)
        X = ((d[STATS] - d[STATS].mean()) / d[STATS].std()).values
        rng = np.random.default_rng(0); C = X[rng.choice(len(X), min(k, len(X)), replace=False)]
        for _ in range(50):
            lab = ((X[:, None] - C[None]) ** 2).sum(2).argmin(1)
            C = np.array([X[lab == i].mean(0) if (lab == i).any() else C[i] for i in range(len(C))])
        cl = d.assign(Cluster=lab.astype(str))
        st.plotly_chart(px.scatter(cl, x="ATK", y="SPD", size="Poder", color="Cluster", hover_name="Digimon"),
                        use_container_width=True)
        st.dataframe(cl.groupby("Cluster")[STATS + ["Poder"]].mean().round(0), use_container_width=True)
    with t[3]:
        pk = st.multiselect("Digimon a comparar", d.Digimon, default=list(d.nlargest(3, "Poder").Digimon))
        fig = go.Figure()
        for n in pk:
            r = d[d.Digimon == n].iloc[0]
            fig.add_trace(go.Scatterpolar(r=[r[s] for s in STATS] + [r[STATS[0]]], theta=STATS + [STATS[0]],
                                          fill="toself", name=n))
        st.plotly_chart(fig, use_container_width=True)
    with t[4]:
        r = st.selectbox("Ranking por", STATS + ["Poder"], index=5, key="rk")
        n = st.slider("Cuantos mostrar", 5, 30, 15)
        st.plotly_chart(px.bar(d.nlargest(n, r).sort_values(r), x=r, y="Digimon", orientation="h", color="Atributo",
                               color_discrete_map=COLORS, height=500), use_container_width=True)
        st.dataframe(d.groupby("Atributo")[STATS + ["Poder"]].mean().round(0), use_container_width=True)
    with t[5]:
        a, b = st.columns(2)
        d1 = a.selectbox("Digimon A", df.Digimon, index=int(df.index[df.Digimon == "Omnimon"][0]))
        d2 = b.selectbox("Digimon B", df.Digimon, index=int(df.index[df.Digimon == "Beelzemon"][0]))
        if st.button("⚔️ Simular 2000 combates"):
            A, B = (df[df.Digimon == x].iloc[0] for x in (d1, d2))
            mu = lambda x, y: 1.25 if TRI.get(x) == y else 0.8 if TRI.get(y) == x else 1.0
            pa, pb = A.Poder * mu(A.Atributo, B.Atributo), B.Poder * mu(B.Atributo, A.Atributo)
            w = np.mean(np.random.normal(pa, 40, 2000) > np.random.normal(pb, 40, 2000))
            st.metric(f"Victoria de {d1}", f"{w:.1%}"); st.metric(f"Victoria de {d2}", f"{1-w:.1%}")
            st.caption("Poder estimado x ventaja de triangulo (x1.25 / x0.8) + ruido.")

# ============================== HISTORIA ==============================
else:
    st.title("📜 Historia del Mundo Digital")
    st.caption("Descripciones basadas en el canon de la franquicia; su rol exacto en Time Stranger conviene verificarlo en el juego.")
    H = {
     "🖥️ Las 3 computadoras centrales": "Homeos, Yggdrasil y Kunlun son los tres nucleos que sostienen el Mundo Digital. **Yggdrasil** administra el orden y la evolucion de los Digimon; **Homeos** y **Kunlun** completan la red de control. Todo esto se mueve bajo **Homeostasis**, el sistema que busca mantener el equilibrio y corregir cualquier amenaza a la estabilidad del mundo.",
     "👑 Caballeros Reales (Royal Knights)": "Elite guardiana de Yggdrasil: Omnimon, Gallantmon, Alphamon, Craniamon, Dynasmon, Examon, Gankoomon, Jesmon, Magnamon, Sleipmon, UlforceVeedramon, Duftmon, Leopardmon y otros segun la fuente. Actuan como fuerza ejecutora que protege el orden digital.",
     "🐲 Los 12 Devas": "Doce generales divinos inspirados en los guardianes budistas y el zodiaco: Vikaralamon, Mihiramon, Pajiramon, Kumbhiramon, Majiramon, Indramon, Sandiramon, Antylamon, Caturamon, Vajramon, Makuramon y otro segun la fuente. Sirven a los Cuatro Soberanos como guardianes.",
     "🐉 Los 4 Soberanos": "Azulongmon (Este), Zhuqiaomon (Sur), Baihumon (Oeste) y Ebonwumon (Norte): bestias sagradas que vigilan cada region cardinal y mantienen el equilibrio del Mundo Digital desde su territorio.",
     "😇 Los 3 Grandes Angeles": "Seraphimon, Ophanimon y Cherubimon: Digimon de luz y justicia, considerados guardianes celestiales y simbolo del bien. Cherubimon tambien tiene una version corrupta en la franquicia.",
     "😈 Los 7 Grandes Demonios": "Lucemon (Orgullo), Leviamon (Envidia), Lilithmon (Lujuria), Barbamon (Avaricia), Beelzemon (Gula), Belphemon (Pereza) y Daemon (Ira): inspirados en los siete pecados capitales, representan el poder oscuro mas temido.",
     "🗿 Los Titanes": "Grupo de poder ancestral de origen mitologico. Su definicion exacta varia entre fuentes (por ejemplo Titamon o las Olympos XII), asi que ajusta esta descripcion a lo que muestre el juego.",
     "🌌 Susanoomon": "Fusion de los diez Guerreros Legendarios (Digimon Frontier) y una de las existencias mas poderosas de toda la franquicia, capaz de purificar la oscuridad.",
    }
    for title, text in H.items():
        with st.expander(title, expanded=title.startswith("🖥️")):
            st.write(text)
