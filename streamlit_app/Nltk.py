import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from collections import Counter
import networkx as nx
import plotly.graph_objects as go
import plotly.express as px
from wordcloud import WordCloud, STOPWORDS
import re


# Load Movie data
data = pd.read_csv("streamlit_app/scraped_table2(in).csv")

# Clean the data
data = data[~data.isin(['-']).any(axis=1)]  # Remove rows with '-'
data['1998 Rank'] = pd.to_numeric(data['1998 Rank'], errors='coerce') # convert rank columns to numeric
data['2007 Rank'] = pd.to_numeric(data['2007 Rank'], errors='coerce')
data['Rank Change'] = data['1998 Rank'] - data['2007 Rank']  # Positive means it improved

# Streamlit app
st.title("TOP MOVIES 1998 RANK VS 2007 RANK") #title of page
st.write("This app displays visualizations comparing movie ranks and release year distributions.") # description for app
st.write(data) # display table of data

# Create tabs using st.tabs()
tab1, tab2, tab3, tab4, tab5, tab6, tab7,tab8,tab9,tab10,tab11, tab12, tab13, tab14, tab15, tab16, tab17, tab18,tab19,tab20,tab21,tab22,tab23,tab24= st.tabs(["Rank Comparison: 1998 vs 2007","Distribution of Film Release Years", "Top 10 Most Frequent Directors","Top 10 Production Companies","Distribution of Rank Change (1998 - 2007)",
                                                                                                    "Top 10 Films with the Biggest Rank Changes (1998 → 2007)",
                                                                                                    "Average Rank Change by Director",
                                                                                                     "Network of Directors and Their Films",
                                                                                                      "Director → Studio → Film",
                                                                                                                          "Trend of Average Film Rank by Release Year",
                                                                                                                          "Rank Distribution by Decade (2007 List)",
                                                                                                                        "Distribution of Movie Ranks in 1998",
                                                                                                                        "Distribution of Movie Ranks in 2007",
                                                                                                                        "Distribution of Movie Ranks: 1998 vs 2007",
                                                                                                                        "Cumulative Distribution of Ranks",
                                                                                                                        "Treemap: Directors by Number of Movies",
                                                                                                                        "Movies per Year with Highlighted Peaks",
                                                                                                                        "Cumulative Films Over Time (Decades)",
                                                                                                                        "Stacked Bar Plot: Film Count by Decade",
                                                                                                                        "Correlation Matrix","Top 10 Directors: Share of Films",
                                                                                                                        "Most Common Words in Film Titles","Production Companies Word Cloud"
                                                                                                                        ,"Film Titles Before and After 1950 Word Clouds"])


with tab1:
    st.title("Rank Comparison: 1998 vs 2007")
    st.write("This visualization compares ranks from 1998 and 2007, highlighting the changes.")

    # Create the scatter plot
    fig, ax = plt.subplots() # generates figure object(the container for your entire plot or visualization), axes (represent the area where data is plotted (like subplots within a figure))
    sns.scatterplot(data=data,x='1998 Rank',y='2007 Rank',hue='Rank Change',palette='coolwarm',size=abs(data['Rank Change']),legend=False,ax=ax)
    #Using ax ensures your plot is explicitly tied to the specific figure you're working on, avoiding any confusion or conflicts when creating multiple graphs across different tabs.
    ax.plot([1, 100], [1, 100], color='gray', linestyle='--')  # Diagonal line
    ax.set_title('Rank Comparison: 1998 vs 2007')
    ax.set_xlabel('1998 Rank')
    ax.set_ylabel('2007 Rank')
    # used to display your Matplotlib figure
    st.pyplot(fig)

with tab2:
    st.title("Distribution of Film Release Years")
    st.write("This visualization shows the distribution of film release years with a KDE overlay.")

    # Create the histogram
    fig2, ax = plt.subplots()
    sns.histplot(data['Release year'], bins=15, kde=True, ax=ax)
    ax.set_title('Distribution of Film Release Years')
    ax.set_xlabel('Release Year')
    ax.set_ylabel('Number of Films')

    # Display the plot
    st.pyplot(fig2)


with tab3:
    st.title("Top 10 Most Frequent Directors")
    st.write("This visualization shows the top 10 directors based on the number of films they directed.")

    # Create the barplot
    top_directors = data['Director'].value_counts().head(10)
    fig3, ax = plt.subplots()
    sns.barplot(x=top_directors.values, y=top_directors.index, palette="magma", ax=ax)
    ax.set_title('Top 10 Most Frequent Directors')
    ax.set_xlabel('Number of Films')
    ax.set_ylabel('Director')


    st.pyplot(fig3)

with tab4:
    st.title("Top 10 Production Companies")
    st.write("This visualization shows the top 10 production companies based on the number of films they produced.")
    # Split companies if there are multiple in a cell
    company_list = data['Production companies'].dropna().apply(lambda x: [i.strip() for i in x.split(',')])
    flat_companies = [company for sublist in company_list for company in sublist]
    company_counts = pd.Series(Counter(flat_companies)).sort_values(ascending=False).head(10)

    # Create the barplot
    fig4, ax = plt.subplots()
    sns.barplot(x=company_counts.values, y=company_counts.index, palette="cubehelix", ax=ax)
    ax.set_title('Top 10 Production Companies')
    ax.set_xlabel('Number of Films')
    ax.set_ylabel('Production Company')
    st.pyplot(fig4)
with tab5:
    st.title("Distribution of Rank Change (1998 - 2007)")
    st.write("This visualization shows the distribution of rank changes between 1998 and 2007.")

    # Create the histogram
    fig5, ax = plt.subplots()
    sns.histplot(data['Rank Change'], bins=20, kde=True, ax=ax)
    ax.set_title('Distribution of Rank Change (1998 - 2007)')
    ax.set_xlabel('Rank Change')
    ax.set_ylabel('Number of Films')
    ax.axvline(0, color='black', linestyle='--')  # Vertical line at 0

    st.pyplot(fig5)
with tab6:
    st.title("Top 10 Films with the Biggest Rank Changes (1998 → 2007)")
    st.write("This visualization highlights the top 10 films with the most significant rank changes between 1998 and 2007.")

    top_movers = data[['Film', '1998 Rank', '2007 Rank']].copy()
    top_movers['Change'] = top_movers['1998 Rank'] - top_movers['2007 Rank']
    top_movers['abs_change'] = top_movers['Change'].abs()
    top_movers = top_movers.sort_values('abs_change', ascending=False).head(10)
    # Create the barplot
    fig6, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(
        x='Change', y='Film', data=top_movers,
        palette='RdYlGn', dodge=False, ax=ax
    )
    ax.axvline(0, color='black', linestyle='--')  # Vertical line at 0
    ax.set_title('Top 10 Films with the Biggest Rank Changes (1998 → 2007)')
    ax.set_xlabel('Change in Rank (Positive = Rank Improved)')
    ax.set_ylabel('Film')
    plt.tight_layout()

    st.pyplot(fig6)
with tab7:
    st.title("Average Rank Change by Director")
    st.write("This visualization shows the average rank change for each director between 1998 and 2007.")
    director_change = data.groupby('Director')['Rank Change'].mean().sort_values()
    # Create the barplot
    fig7, ax = plt.subplots(figsize=(12, 10))
    sns.barplot(x=director_change, y=director_change.index, palette='coolwarm', ax=ax)
    ax.axvline(0, color='black', linestyle='--')  # Vertical line at 0
    ax.set_title('Average Rank Change by Director')
    ax.set_xlabel('Avg Rank Change (1998 - 2007)')
    ax.set_ylabel('Director')
    st.pyplot(fig7)
with tab8:
    st.title("Network of Directors and Their Films")
    st.write("This visualization shows the relationships between directors and their films.")

    # Create the NetworkX graph
    G = nx.Graph()

    for _, row in data.iterrows():
        director = row['Director']
        film = row['Film']
        G.add_node(director, type='director')
        G.add_node(film, type='film')
        G.add_edge(director, film)

    # Generate the layout and plot the graph
    pos = nx.spring_layout(G, k=0.5)
    fig8, ax = plt.subplots(figsize=(12, 12))
    nx.draw(G, pos, with_labels=False, node_size=50, alpha=0.7, ax=ax)

    # Label top directors
    top_directors = data['Director'].value_counts().head(5).index
    for node in G.nodes:
        if node in top_directors:
            x, y = pos[node]
            ax.text(x, y, node, fontsize=10)

    ax.set_title("Network of Directors and Their Films")
    st.pyplot(fig8)
with tab9:
    st.title("Director → Studio → Film")
    st.write("This Sankey diagram visualizes the flow from directors to studios to films.")

    # Extract simplified Sankey structure (director -> studio -> film)
    sankey_df = data[['Director', 'Production companies', 'Film']].dropna().head(20)

    labels = list(set(sankey_df['Director']) | set(sankey_df['Production companies']) | set(sankey_df['Film']))
    label_indices = {label: i for i, label in enumerate(labels)}

    sources = sankey_df['Director'].map(label_indices)
    targets = sankey_df['Production companies'].map(label_indices)
    values = [1] * len(sankey_df)

    sources2 = sankey_df['Production companies'].map(label_indices)
    targets2 = sankey_df['Film'].map(label_indices)

    fig = go.Figure(data=[go.Sankey(
        node=dict(label=labels),
        link=dict(
            source=list(sources) + list(sources2),
            target=list(targets) + list(targets2),
            value=[1] * (len(sources) + len(sources2))
        )
    )])
    fig.update_layout(title_text="Director → Studio → Film", font_size=10)
    st.plotly_chart(fig, use_container_width=True)
with tab10:
    st.title("Trend of Average Film Rank by Release Year")
    st.write("This visualization shows the trend of average film ranks over the years.")
    # Calculate the average rank
    data['Avg Rank'] = data[['1998 Rank', '2007 Rank']].mean(axis=1)
    # Create the regression plot
    fig10, ax = plt.subplots()
    sns.regplot(data=data,
        x='Release year',
        y='Avg Rank',
        scatter_kws={'alpha': 0.5},
        line_kws={'color': 'red'},
        ax=ax)
    ax.set_title('Trend of Average Film Rank by Release Year')
    ax.set_xlabel('Release Year')
    ax.set_ylabel('Average Rank')
    # Display the plot in Streamlit
    st.pyplot(fig10)
with tab11:
    st.title("Rank Distribution by Decade (2007 List)")
    st.write("This visualization shows the distribution of ranks by decade from the 2007 list.")
    # Create the boxplot
    data['decade'] = (data['Release year'] // 10) * 10
    fig11, ax = plt.subplots(figsize=(12, 6))
    sns.boxplot(data=data, x='decade', y='2007 Rank', palette="coolwarm", ax=ax)
    ax.set_title('Rank Distribution by Decade (2007 List)')
    ax.set_ylabel('Rank (lower is better)')
    ax.set_xlabel('Decade')
    plt.xticks(rotation=45)
    # Display the plot
    st.pyplot(fig11)
with tab12:
    st.title("Distribution of Movie Ranks in 1998")
    st.write("This visualization shows the distribution of movie ranks in 1998.")
    # Create the histogram
    fig12, ax = plt.subplots(figsize=(12, 6))
    sns.histplot(data['1998 Rank'], kde=True, bins=20, color='skyblue', edgecolor='black', ax=ax)
    ax.set_title("Distribution of Movie Ranks in 1998")
    ax.set_xlabel("Rank")
    ax.set_ylabel("Frequency")
    plt.tight_layout()
    # Display the plot
    st.pyplot(fig12)
with tab13:
    st.title("Distribution of Movie Ranks in 2007")
    st.write("This visualization shows the distribution of movie ranks in 2007.")
    # Create the histogram
    fig13, ax = plt.subplots(figsize=(12, 6))
    sns.histplot(data['2007 Rank'], kde=True, bins=20, color='salmon', edgecolor='black', ax=ax)
    ax.set_title("Distribution of Movie Ranks in 2007")
    ax.set_xlabel("Rank")
    ax.set_ylabel("Frequency")
    plt.tight_layout()
    st.pyplot(fig13)
with tab14:
    st.title("Distribution of Movie Ranks: 1998 vs 2007")
    st.write("This visualization compares the distribution of movie ranks in 1998 and 2007.")
    # Plot both distributions on the same axes
    fig14, ax = plt.subplots(figsize=(12, 6))
    sns.histplot(data['1998 Rank'], kde=True, bins=20, color='skyblue', label='1998 Rank', edgecolor='black', alpha=0.6, ax=ax)
    sns.histplot(data['2007 Rank'], kde=True, bins=20, color='salmon', label='2007 Rank', edgecolor='black', alpha=0.6, ax=ax)
    ax.set_title("Distribution of Movie Ranks: 1998 vs 2007")
    ax.set_xlabel("Rank")
    ax.set_ylabel("Frequency")
    ax.legend(title='Year')
    plt.tight_layout()

    st.pyplot(fig14)
with tab15:
    st.title("Cumulative Distribution of Ranks")
    st.write("This visualization shows the cumulative distribution of ranks for 1998 and 2007.")

    # Create the ECDF plot
    fig15, ax = plt.subplots(figsize=(10, 6))
    sns.ecdfplot(data=data['1998 Rank'], label='1998', color='skyblue', ax=ax)
    sns.ecdfplot(data=data['2007 Rank'], label='2007', color='salmon', ax=ax)
    ax.set_title('Cumulative Distribution of Ranks')
    ax.set_xlabel('Rank')
    ax.set_ylabel('Cumulative Proportion')
    ax.legend(title='Year')
    plt.tight_layout()

    st.pyplot(fig15)
with tab16:
    st.title("Treemap: Directors by Number of Movies")
    st.write("This treemap shows the number of movies directed by each director.")
    # Create the treemap
    top_directors = data['Director'].value_counts().reset_index()
    top_directors.columns = ['Director', 'Movie Count']
    fig16 = px.treemap(top_directors, path=['Director'], values='Movie Count', title="Treemap: Directors by Number of Movies")
    # Display the treemap
    st.plotly_chart(fig16, use_container_width=True)
with tab17:
    st.title("Movies per Year with Highlighted Peaks")
    st.write("This visualization shows the number of movies released per year, highlighting peak years.")
    # Count number of films per year
    year_counts = data['Release year'].value_counts().sort_index()
    # Create the line plot
    fig17, ax = plt.subplots(figsize=(12, 6))
    sns.lineplot(x=year_counts.index, y=year_counts.values, marker='o', ax=ax)
    # Highlight peaks
    avg_films = year_counts.mean()
    peaks = year_counts[year_counts > avg_films]
    ax.scatter(peaks.index, peaks.values, color='red', label="Peak Years", zorder=5)
    ax.set_title("Movies per Year with Highlighted Peaks")
    ax.set_xlabel("Year")
    ax.set_ylabel("Number of Movies")
    ax.legend()
    plt.tight_layout()
    st.pyplot(fig17)
with tab18:
    st.title("Cumulative Films Over Time (Decades)")
    st.write("This visualization shows the cumulative number of films released over time, grouped by decades.")
    # Group by decade and count films
    data['decade'] = (data['Release year'] // 10) * 10
    decade_counts = data['decade'].value_counts().sort_index().cumsum()
    # Create the line plot
    fig18, ax = plt.subplots(figsize=(12, 6))
    sns.lineplot(x=decade_counts.index, y=decade_counts.values, marker='o', color='purple', ax=ax)
    ax.set_title("Cumulative Films Over Time (Decades)")
    ax.set_xlabel("Decade")
    ax.set_ylabel("Cumulative Number of Films")
    plt.tight_layout()
    # Display the plot
    st.pyplot(fig18)
with tab19:
    st.title("Stacked Bar Plot: Film Count by Decade")
    director_decade_counts = data.groupby(['Director', 'decade']).size().unstack(fill_value=0)
    fig19, ax = plt.subplots(figsize=(15, 8))
    director_decade_counts.plot(kind='bar', stacked=True, cmap="viridis", ax=ax)
    ax.set_title("Directors by Film Count and Decade")
    ax.set_xlabel("Director")
    ax.set_ylabel("Film Count")
    st.pyplot(fig19.figure)

with tab20:
    st.title("Correlation Matrix")
    data.drop(columns=["Unnamed: 0"], inplace=True, errors='ignore')  # Remove unnecessary column
    numeric_columns = data.select_dtypes(include='number')  # Select numeric columns
    correlation_matrix = numeric_columns.corr()  # Calculate correlations
    fig20, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", linewidths=0.5, ax=ax)
    ax.set_title("Correlation Matrix")
    st.pyplot(fig20)
with tab21:
    st.title("Top 10 Directors: Share of Films")
    top_directors = data['Director'].value_counts().head(10)
    fig21, ax = plt.subplots(figsize=(8, 8))
    top_directors.plot.pie(autopct='%1.1f%%', startangle=90, cmap="plasma", ax=ax)
    ax.set_title("Top 10 Directors: Share of Films")
    ax.set_ylabel("")
    st.pyplot(fig21)
with tab22:
    st.title("Most Common Words in Film Titles")
    title_text = ' '.join(data['Film'].dropna().astype(str).tolist())
    wordcloud = WordCloud(width=1000, height=500, background_color='white',
                          stopwords=STOPWORDS, colormap='viridis').generate(title_text)
    fig22, ax = plt.subplots(figsize=(12, 6))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    ax.set_title("Most Common Words in Film Titles", fontsize=16)
    st.pyplot(fig22)
with tab23:
    st.title("Production Companies Word Cloud")
    company_text = ' '.join(data['Production companies'].dropna().astype(str).tolist())
    wordcloud = WordCloud(width=1000, height=500, background_color='white', colormap='cool').generate(company_text)
    fig23, ax = plt.subplots(figsize=(12, 6))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    ax.set_title("Production Companies Word Cloud", fontsize=16)
    st.pyplot(fig23)
with tab24:
    st.title("Film Titles Before and After 1950")
    before_1950 = data[data['Release year'] < 1950]
    after_1950 = data[data['Release year'] >= 1950]
    def get_clean_text(film_series):
        text = ' '.join(film_series.dropna().astype(str).tolist())
        words = re.findall(r'\b\w+\b', text.lower())
        stopwords = set(STOPWORDS)
        stopwords.update(['the', 'of', 'a', 'and'])  # Add custom stopwords if needed
        filtered = [w for w in words if w not in stopwords and len(w) > 2]
        return ' '.join(filtered)
    text_before = get_clean_text(before_1950['Film'])
    text_after = get_clean_text(after_1950['Film'])
    wordcloud_before = WordCloud(width=800, height=400, background_color='white', colormap='Blues').generate(text_before)
    wordcloud_after = WordCloud(width=800, height=400, background_color='white', colormap='Oranges').generate(text_after)
    fig24, axes = plt.subplots(1, 2, figsize=(16, 7))
    axes[0].imshow(wordcloud_before, interpolation='bilinear')
    axes[0].axis('off')
    axes[0].set_title('Film Titles Before 1950', fontsize=16)
    axes[1].imshow(wordcloud_after, interpolation='bilinear')
    axes[1].axis('off')
    axes[1].set_title('Film Titles After 1950', fontsize=16)
    plt.tight_layout()
    st.pyplot(fig24)






