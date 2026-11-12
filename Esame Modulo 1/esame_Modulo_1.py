import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#Parte 1 – Importazione Dataset, conversione dati e ordinazione cronologica 
df = pd.read_csv("vendite.csv")
df["Data"] = pd.to_datetime(df["Data"])
df["Quantità"] = df["Quantità"].astype(int)
df["Prezzo_unitario"] = df["Prezzo_unitario"].astype(float).round(2)
df = df.sort_values(by="Data", ascending=True).reset_index(drop=True)

#Parte 2 – Importazione con Pandas

#Stampare le prime 5 righe (head())
print("Prime 5 righe:\n", df.head())
#Il numero di righe e colonne (shape)
print("Shape: ",df.shape)
#Le informazioni generali (info())
print(df.info())

#Parte 3 – Elaborazioni con Pandas

#Aggiungere una colonna Incasso calcolata come Quantità * Prezzo_unitario.
df["Incasso"] = (df["Quantità"] * df["Prezzo_unitario"]).round(2)
#Calcolare l’incasso totale di tutta la catena
incasso_totale = round(df["Incasso"].sum(), 2)
print(f"Incasso totale: {incasso_totale}")
#Calcolare l’incasso medio per negozio
incasso_medio_negozio = df.groupby("Negozio")["Incasso"].mean().round(2)
print(f"Incasso medio per negozio:\n{incasso_medio_negozio}")
#Calcola i 3 prodotti più venduti (in termini di quantità totale)
prodotti_venduti = df.groupby("Prodotto")["Quantità"].sum()
print(f"I tre prodotti più venduti sono:\n",prodotti_venduti.sort_values(ascending=False).head(3))
#Raggruppare i dati per Negozio e Prodotto e mostrare l’incasso medio.
incasso_medio = df.groupby(["Negozio", "Prodotto"])["Incasso"].mean().round(2)
print(f"Incasso medio per Negozio e Prodotto:\n",incasso_medio)

#Parte 4 – Uso di NumPy

#Estrarre la colonna Quantità come array NumPy e calcolare:
quantita_np = df["Quantità"].to_numpy()
print(quantita_np)
#media, minimo, massimo e deviazione standard
print(f"Media: {quantita_np.mean().round(2)}")
print(f"Minimo: {quantita_np.min()}")
print(f"Massimo: {quantita_np.max()}")
print(f"Deviazione standard: {quantita_np.std().round(2)}")
#Calcolare percentuale di vendite sopra la media
filtro = quantita_np>quantita_np.mean().round(2)
vendite_sopra_media = len(quantita_np[filtro])
print(f"La percentuale di vendite sopra la medie è: {(vendite_sopra_media*100/len(quantita_np)).__round__(2)}%")

#Parte 5 – Visualizzazioni con Matplotlib

#Grafico a barre: incasso totale per ogni negozio.
q = df.groupby("Negozio")["Incasso"].sum().to_dict()
plt.figure(figsize=(10, 5))
plt.bar(q.keys(), q.values(), color="Blue")
plt.title("Incasso X Negozio", color="Red")
plt.xlabel("Negozio", color="Green")
plt.ylabel("Incasso in €", color="Green")
plt.show()

#Grafico a torta: percentuale di incassi per ciascun prodotto.
p = df.groupby("Prodotto")["Incasso"].sum().to_dict()
plt.figure(figsize=(10, 5))
plt.pie(p.values(), labels=p.keys(), autopct="%1.1f%%")
plt.title("Incasso X Prodotto", color="Red")
plt.show()

#Grafico a linee: andamento giornaliero degli incassi totali della catena.
g = df.groupby("Data")["Incasso"].sum().to_dict()
plt.figure(figsize=(12, 5))
plt.plot(g.keys(), g.values(), linestyle="-", color="Blue", marker="o")
plt.title("Andamento giornaliero", color="Red")
plt.xlabel("Data", color="Green")
plt.ylabel("Incasso in €", color="Green")
plt.grid(alpha=0.6)
plt.show()

#Parte 6 – Analisi Avanzata

#Creare una nuova colonna Categoria che raggruppi i prodotti in grandi famiglie (es. Smartphone e Laptop → Informatica, TV → Elettrodomestici).
categorie = {
    "Smartphone": "Informatica",
    "Laptop": "Informatica",
    "Tablet": "Informatica",
    "TV": "Elettrodomestici",
    "Cuffie": "Accessori",
    "Smartwatch": "Accessori"
}
df["Categoria"] = df["Prodotto"].map(categorie)
print(df.head())
#Calcolare per ogni categoria L'incasso totale
incasso_tot_categoria = df.groupby("Categoria")["Incasso"].sum()
print(f"Incasso totale per categoria:\n", incasso_tot_categoria)
#Calcolare per ogni categoria la quantità media venduta
quantita_media_categoria = df.groupby("Categoria")["Quantità"].mean()
print(f"Quantità media venduta per ogni categoria:\n", quantita_media_categoria.round(2))
#Salvare il DataFrame aggiornato con le nuove colonne in un nuovo file vendite_analizzate.csv.
df.to_csv("vendite_analizzate.csv", index=False)

#Parte 7 – Estensioni

#Creare un grafico combinato (versione 1), : incasso medio per categoria (grafico a barre) + linea della quantità media venduta.
incasso_medio_categoria = df.groupby("Categoria")["Incasso"].mean()
quantita_media_categoria = df.groupby("Categoria")["Quantità"].mean()
fig, ax1 = plt.subplots(figsize=(10, 6))
ax1.bar(incasso_medio_categoria.index, incasso_medio_categoria.values, color="Blue", label="Incasso medio")
ax1.set_xlabel("Categoria", color="Green")
ax1.set_ylabel("Incasso medio €", color="Green")
ax1.set_title("Incasso medio e quantità media per categoria", color="Red")

ax2 = ax1.twinx()
ax2.plot(quantita_media_categoria.index, quantita_media_categoria.values, color="red", marker="o", label="Quantità media")
ax2.set_ylabel("Quantità media venduta", color="Green")
ax1.legend(loc="upper left")
ax2.legend(loc="upper right")
plt.tight_layout()
plt.show()

#Creare un grafico combinato (versione 2), : incasso medio per categoria (grafico a barre) + linea della quantità media venduta.
incasso_medio_categoria = df.groupby("Categoria")["Incasso"].mean()
quantita_media_categoria = df.groupby("Categoria")["Quantità"].mean()
fig, ax = plt.subplots(1, 2, figsize=(14, 5))
ax[0].bar(incasso_medio_categoria.index, incasso_medio_categoria.values, color="Blue")
ax[0].set_title("Incasso medio per categoria", color="Red")
ax[0].set_xlabel("Categoria", color="Green")
ax[0].set_ylabel("Incasso medio €", color="Green")
ax[0].tick_params(axis="x", rotation=45)

ax[1].plot(quantita_media_categoria.index, quantita_media_categoria.values, color="red", marker="o")
ax[1].set_title("Quantità media per categoria", color="Red")
ax[1].set_xlabel("Categoria", color="Green")
ax[1].set_ylabel("Quantità media venduta", color="Green")
ax[1].tick_params(axis="x", rotation=45)

plt.tight_layout()
plt.show()

#Creare una funzione top_n_prodotti(n) che restituisca i n prodotti più venduti in termini di incasso totale.
def top_n_prodotti(n):
    if not isinstance(n, int) or n <= 0:
        raise ValueError("Inserisci un numero intero positivo!!")
    prodotti = df.groupby("Prodotto")["Incasso"].sum()
    return f"I {n} prodotti più venduti in termini di incasso totale sono:\n{prodotti.sort_values(ascending=False).head(n)}"

print(top_n_prodotti(2))
