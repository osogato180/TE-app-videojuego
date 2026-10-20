import io
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

st.set_page_config(page_title="Game Analytics & Predicciones", page_icon="🎮", layout="wide")

CAT = ["Genero", "Plataforma", "Editorial", "Multijugador"]
NUM = ["Anio", "Puntuacion", "Presupuesto", "Horas"]
TARGET = "Ventas"
REQ = ["Nombre"] + CAT + NUM + [TARGET]

# ---------------------------------------------------------- datos base (SINTETICOS)
@st.cache_data
def base_data(n=700, seed=42):
    r = np.random.default_rng(seed)
    gen = ["Accion", "RPG", "Deportes", "Shooter", "Aventura", "Estrategia", "Carreras", "Indie"]
    plat = ["PC", "PS5", "Xbox", "Switch", "Mobile"]
    pub = ["Nintendo", "Sony", "Microsoft", "Ubisoft", "EA", "Capcom", "Bandai Namco", "Indie"]
    d = pd.DataFrame({
        "Nombre": [f"Juego {i:03d}" for i in range(n)],
        "Genero": r.choice(gen, n), "Plataforma": r.choice(plat, n), "Editorial": r.choice(pub, n),
        "Multijugador": r.choice(["Si", "No"], n, p=[.45, .55]),
        "Anio": r.integers(2010, 2026, n), "Puntuacion": np.clip(r.normal(74, 11, n), 30, 99).round(0),
        "Presupuesto": np.clip(r.lognormal(3, 1.1, n), 0.2, 400).round(1),
        "Horas": np.clip(r.normal(25, 15, n), 2, 120).round(0)})
    gb = {"Accion": 1.2, "RPG": 1.1, "Deportes": 1.0, "Shooter": 1.3, "Aventura": .9, "Estrategia": .6, "Carreras": .7, "Indie": .4}
    pb = {"PC": 1, "PS5": 1.3, "Xbox": 1.0, "Switch": 1.2, "Mobile": .8}
    s = (np.exp((d.Puntuacion - 70) / 18) * (d.Presupuesto ** .45) * d.Genero.map(gb) * d.Plataforma.map(pb)
         * np.where(d.Multijugador == "Si", 1.25, 1) * (1 + (d.Anio - 2010) * .015) * r.lognormal(0, .3, n) * .8)
    d[TARGET] = s.round(2)
    return d

if "df" not in st.session_state:
    st.session_state.df = base_data()
df = st.session_state.df

tab_home, tab_an, tab_data = st.tabs(["🏠 Inicio", "📊 Analítica", "🗂️ Datos"])

# ---------------------------------------------------------- INICIO
with tab_home:
    st.title("🎮 Analítica y predicciones de videojuegos")
    st.write("Explora el mercado, entrena modelos para **predecir ventas** y proyecta tendencias. "
             "Puedes ampliar la base subiendo tus propios datos en la pestaña **Datos**.")
    k = st.columns(5)
    k[0].metric("Juegos", len(df)); k[1].metric("Ventas totales (M)", f"{df[TARGET].sum():,.0f}")
    k[2].metric("Puntuación media", f"{df.Puntuacion.mean():.1f}")
    k[3].metric("Presupuesto medio (M$)", f"{df.Presupuesto.mean():.1f}")
    k[4].metric("Rango de años", f"{int(df.Anio.min())}-{int(df.Anio.max())}")
    c1, c2 = st.columns(2)
    y = df.groupby("Anio")[TARGET].sum().reset_index()
    c1.plotly_chart(px.area(y, x="Anio", y=TARGET, title="Ventas por año"), use_container_width=True)
    g = df.groupby("Genero")[TARGET].sum().reset_index()
    c2.plotly_chart(px.pie(g, names="Genero", values=TARGET, hole=.45, title="Cuota por género"), use_container_width=True)
    st.info("Los datos iniciales son **sintéticos** (de demostración). Sube un CSV real para análisis reales.")

# ---------------------------------------------------------- ANALITICA
with tab_an:
    st.header("📊 Analítica")
    mode = st.radio("Módulo", ["Exploración", "Modelo predictivo", "Pronóstico temporal"], horizontal=True)
    f = st.columns(3)
    gs = f[0].multiselect("Género", sorted(df.Genero.unique()))
    ps = f[1].multiselect("Plataforma", sorted(df.Plataforma.unique()))
    yr = f[2].slider("Años", int(df.Anio.min()), int(df.Anio.max()), (int(df.Anio.min()), int(df.Anio.max())))
    d = df[df.Anio.between(*yr)]
    if gs: d = d[d.Genero.isin(gs)]
    if ps: d = d[d.Plataforma.isin(ps)]
    if len(d) < 30:
        st.warning("Pocos datos con esos filtros (mínimo 30)."); st.stop()

    if mode == "Exploración":
        a, b = st.columns(2)
        a.plotly_chart(px.scatter(d, x="Puntuacion", y=TARGET, color="Genero", size="Presupuesto", hover_name="Nombre",
                                  log_y=True, title="Puntuación vs ventas"), use_container_width=True)
        b.plotly_chart(px.box(d, x="Plataforma", y=TARGET, color="Plataforma", log_y=True, title="Ventas por plataforma"),
                       use_container_width=True)
        piv = d.pivot_table(index="Genero", columns="Plataforma", values=TARGET, aggfunc="mean")
        st.plotly_chart(px.imshow(piv, text_auto=".1f", aspect="auto", color_continuous_scale="Viridis",
                                  title="Ventas medias: género x plataforma"), use_container_width=True)
        st.plotly_chart(px.imshow(d[NUM + [TARGET]].corr(), text_auto=".2f", zmin=-1, zmax=1,
                                  color_continuous_scale="RdBu_r", title="Correlaciones"), use_container_width=True)

    elif mode == "Modelo predictivo":
        m1, m2 = st.columns(2)
        name = m1.selectbox("Modelo", ["Random Forest", "Gradient Boosting", "Ridge (lineal)"])
        test = m2.slider("% de prueba", 10, 40, 20) / 100
        models = {"Random Forest": RandomForestRegressor(300, random_state=0, n_jobs=-1),
                  "Gradient Boosting": GradientBoostingRegressor(random_state=0), "Ridge (lineal)": Ridge()}
        pre = ColumnTransformer([("c", OneHotEncoder(handle_unknown="ignore"), CAT), ("n", StandardScaler(), NUM)])
        X, yv = d[CAT + NUM], np.log1p(d[TARGET])
        Xtr, Xte, ytr, yte = train_test_split(X, yv, test_size=test, random_state=1)
        pipe = Pipeline([("p", pre), ("m", models[name])]).fit(Xtr, ytr)
        pred = pipe.predict(Xte)
        r2, mae = r2_score(yte, pred), mean_absolute_error(np.expm1(yte), np.expm1(pred))
        c = st.columns(3); c[0].metric("R² (prueba)", f"{r2:.3f}"); c[1].metric("Error medio (M)", f"{mae:.2f}")
        c[2].metric("Datos entrenamiento", len(Xtr))
        cmp = pd.DataFrame({"Real": np.expm1(yte), "Prediccion": np.expm1(pred)})
        fig = px.scatter(cmp, x="Real", y="Prediccion", log_x=True, log_y=True, title="Real vs predicho")
        mx = cmp.max().max(); fig.add_trace(go.Scatter(x=[.1, mx], y=[.1, mx], mode="lines", name="Ideal"))
        st.plotly_chart(fig, use_container_width=True)
        if name != "Ridge (lineal)":
            names = pipe.named_steps["p"].get_feature_names_out()
            imp = pd.Series(pipe.named_steps["m"].feature_importances_, index=names).nlargest(12).sort_values()
            st.plotly_chart(px.bar(imp, orientation="h", title="Variables más influyentes"), use_container_width=True)
        st.subheader("🔮 Predice las ventas de un juego nuevo")
        w = st.columns(4)
        new = pd.DataFrame([{
            "Genero": w[0].selectbox("Género", sorted(df.Genero.unique()), key="wg"),
            "Plataforma": w[1].selectbox("Plataforma", sorted(df.Plataforma.unique()), key="wp"),
            "Editorial": w[2].selectbox("Editorial", sorted(df.Editorial.unique()), key="we"),
            "Multijugador": w[3].selectbox("Multijugador", ["Si", "No"], key="wm"),
            "Anio": w[0].number_input("Año", 2010, 2040, 2026), "Puntuacion": w[1].slider("Puntuación esperada", 30, 99, 80),
            "Presupuesto": w[2].number_input("Presupuesto (M$)", 0.1, 1000.0, 50.0),
            "Horas": w[3].slider("Horas de juego", 2, 120, 25)}])
        p = float(np.expm1(pipe.predict(new[CAT + NUM])[0]))
        resid = np.expm1(ytr) - np.expm1(pipe.predict(Xtr))
        lo, hi = p + np.percentile(resid, 10), p + np.percentile(resid, 90)
        st.success(f"Ventas estimadas: **{p:,.2f} M** (rango 80%: {max(lo, 0):,.2f} – {hi:,.2f} M)")

    else:
        yd = d.groupby("Anio")[TARGET].sum().reset_index()
        c = st.columns(3)
        deg = c[0].selectbox("Tendencia", ["Lineal", "Cuadrática"])
        h = c[1].slider("Años a proyectar", 1, 10, 5)
        metric = c[2].selectbox("Métrica", [TARGET, "Presupuesto", "Puntuacion"])
        yd = d.groupby("Anio")[metric].sum() if metric != "Puntuacion" else d.groupby("Anio")[metric].mean()
        yd = yd.reset_index()
        if len(yd) < 4:
            st.warning("Se necesitan al menos 4 años de datos."); st.stop()
        co = np.polyfit(yd.Anio, yd[metric], 1 if deg == "Lineal" else 2)
        fut = np.arange(yd.Anio.max() + 1, yd.Anio.max() + 1 + h)
        res = yd[metric] - np.polyval(co, yd.Anio); sd = res.std()
        fc = np.polyval(co, fut)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=yd.Anio, y=yd[metric], name="Histórico", mode="lines+markers"))
        fig.add_trace(go.Scatter(x=fut, y=fc, name="Pronóstico", mode="lines+markers", line=dict(dash="dash")))
        fig.add_trace(go.Scatter(x=list(fut) + list(fut[::-1]), y=list(fc + 1.28 * sd) + list((fc - 1.28 * sd)[::-1]),
                                 fill="toself", opacity=.2, name="Banda ~80%", line=dict(width=0)))
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(pd.DataFrame({"Anio": fut, "Pronostico": fc.round(2)}), hide_index=True)
        st.caption("Ajuste polinómico simple sobre el agregado anual; sirve como referencia, no como garantía.")

# ---------------------------------------------------------- DATOS
with tab_data:
    st.header("🗂️ Datos")
    st.write(f"Base actual: **{len(df)}** filas, **{df.shape[1]}** columnas.")
    st.dataframe(df, use_container_width=True, height=350, hide_index=True)
    c = st.columns(3)
    c[0].download_button("⬇️ Descargar base actual", df.to_csv(index=False).encode(), "videojuegos.csv")
    c[1].download_button("📄 Plantilla CSV", df.head(3).to_csv(index=False).encode(), "plantilla.csv")
    if c[2].button("♻️ Restaurar datos originales"):
        st.session_state.df = base_data(); st.rerun()
    st.subheader("➕ Añadir otro dataset")
    st.caption("Columnas requeridas: " + ", ".join(REQ))
    up = st.file_uploader("Sube un CSV o Excel", type=["csv", "xlsx"])
    if up:
        try:
            new = pd.read_csv(up) if up.name.endswith(".csv") else pd.read_excel(up)
        except Exception as e:
            st.error(f"No se pudo leer el archivo: {e}"); st.stop()
        miss = [x for x in REQ if x not in new.columns]
        if miss:
            st.error("Faltan columnas: " + ", ".join(miss))
        else:
            new = new[REQ].dropna()
            for col in NUM + [TARGET]:
                new[col] = pd.to_numeric(new[col], errors="coerce")
            new = new.dropna()
            st.write(f"Filas válidas: **{len(new)}**"); st.dataframe(new.head(10), hide_index=True)
            if st.button("✅ Añadir a la base"):
                st.session_state.df = pd.concat([df, new[df.columns]], ignore_index=True).drop_duplicates()
                st.success("Datos añadidos."); st.rerun()
