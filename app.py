import streamlit as st
import pandas as pd
import numpy as np

# Définition de la structure de référence
expected_columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
dtypes_ref = {'Date': str, 'Open': float, 'High': float, 'Low': float, 'Close': float, 'Volume': float}

def calculate_metrics(df):
    df['Date'] = pd.to_datetime(df['Date'])
    df['Daily Change (%)'] = (df['Close'] - df['Open']) / df['Open'] * 100
    df['Range'] = df['High'] - df['Low']
    df['True Range'] = df[['High', 'Low', 'Close']].apply(lambda x: max(x[0] - x[1], abs(x[0] - x[2]), abs(x[1] - x[2])), axis=1)
    df['ATR'] = df['True Range'].rolling(window=14).mean()
    df['Closing Position'] = (df['Close'] - df['Low']) / (df['High'] - df['Low'])
    df['Volatility'] = df['Daily Change (%)'].rolling(window=14).std()
    df['Sharpe Ratio'] = df['Daily Change (%)'].mean() / df['Volatility'] if df['Volatility'].mean() != 0 else np.nan
    df['Max Drawdown'] = (df['Close'].cummax() - df['Close']) / df['Close'].cummax()
    
    return df

def interpret_metrics(df):
    last_row = df.iloc[-1]
    interpretations = []
    
    # Volatilité
    if last_row['ATR'] > df['ATR'].mean():
        interpretations.append("📈 La volatilité est élevée, les mouvements de prix sont importants.")
    else:
        interpretations.append("📉 La volatilité est faible, le marché est plus stable.")
    
    # Closing Position
    if last_row['Closing Position'] > 0.7:
        interpretations.append("✅ Clôture proche du plus haut, les acheteurs sont en contrôle.")
    elif last_row['Closing Position'] < 0.3:
        interpretations.append("❌ Clôture proche du plus bas, les vendeurs dominent.")
    else:
        interpretations.append("⚖️ Indécision du marché, clôture au milieu de la fourchette.")
    
    # Sharpe Ratio
    if last_row['Sharpe Ratio'] > 1:
        interpretations.append("📊 Bonne performance ajustée au risque (Sharpe Ratio > 1).")
    elif last_row['Sharpe Ratio'] < 0:
        interpretations.append("⚠️ Mauvaise performance ajustée au risque (Sharpe Ratio < 0).")
    else:
        interpretations.append("📉 Performance moyenne (Sharpe Ratio entre 0 et 1).")
    
    # Max Drawdown
    if last_row['Max Drawdown'] > 0.2:
        interpretations.append("❗ Drawdown élevé, risque de pertes importantes.")
    else:
        interpretations.append("✅ Drawdown faible, bonne gestion du risque.")
    
    return interpretations

st.title("📊 Analyse des Données Boursières")

# Upload du fichier par l'utilisateur
uploaded_file = st.file_uploader("Déposez votre fichier CSV", type=["csv"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        df.columns = df.columns.str.strip().str.lower()
        expected_columns_lower = [col.lower() for col in expected_columns]

        if list(df.columns) != expected_columns_lower:
            st.error("❌ Erreur : La structure du fichier ne correspond pas au modèle attendu.")
            st.write("Colonnes attendues :", expected_columns)
            st.write("Colonnes trouvées :", list(df.columns))
        else:
            df.columns = expected_columns  # Normalisation des noms de colonnes
            df = calculate_metrics(df)
            interpretations = interpret_metrics(df)
            
            st.success("✅ Succès : Le fichier est valide et respecte la structure requise !")
            st.subheader("📊 Résumé des Calculs :")
            st.write(df.tail(5))
            
            st.subheader("📢 Interprétations :")
            for interpretation in interpretations:
                st.write(interpretation)
    except Exception as e:
        st.error(f"❌ Erreur lors de la lecture du fichier : {e}")
