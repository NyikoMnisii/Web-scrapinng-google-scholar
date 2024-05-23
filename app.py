from flask import Flask, render_template, request
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.express as px
import networkx as nx
import plotly.graph_objects as go

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def scrape_google_scholar(search_query, num_pages):
    base_url = 'https://scholar.google.com/scholar?hl=en&as_sdt=0%2C5&q={}&btnG=&oq={}'
    feedArr = []

    for page in range(num_pages):
        url = base_url.format(search_query, search_query) + '&start=' + str(page * 10)
        res = requests.get(url, timeout=5)
        content = BeautifulSoup(res.content, "html.parser")

        for data in content.find_all("div", attrs={"class": "gs_r gs_or gs_scl"}):
            AuthorInfo = data.find("div", attrs={"class": "gs_a"}).text
            heading = data.find("h3", attrs={"class": "gs_rt"}).text

            splitted = AuthorInfo.split("-")
            author = splitted[0]
            date = splitted[1]
            webAddress = splitted[2]

            if (date.isdigit() == False):
                splitDate = date.split()
                for x in splitDate:
                    if (x.isdigit()):
                        date = x

            Obj = {
                "Heading": heading,
                "Author": author,
                "Date": date,
                "WebAddress": webAddress
            }

            feedArr.append(Obj)

    return feedArr

def clean_data(data):
    # Convert 'Date' column to datetime format
    data['Date'] = pd.to_datetime(data['Date'], errors='coerce')

    # Remove rows with missing or invalid dates
    data.dropna(subset=['Date'], inplace=True)

    # Extract publication year from the 'Date' column
    data['Year'] = data['Date'].dt.year

    return data

def visualize_trends(data):
    # Group data by publication year and count the number of papers
    yearly_counts = data.groupby('Year').size().reset_index(name='Count')

    # Create an interactive line chart
    fig = px.line(yearly_counts, x='Year', y='Count', title='Number of Papers Published Over Time')
    fig.update_xaxes(title_text='Year')
    fig.update_yaxes(title_text='Number of Papers')
    return fig.to_html(full_html=False)

def visualize_co_authorship(data):
    G = nx.Graph()

    # Extract co-authorship information from the data
    for authors in data['Author']:
        author_list = authors.split(',')
        author_list = [author.strip() for author in author_list]
        if len(author_list) > 1:
            for i in range(len(author_list)):
                for j in range(i+1, len(author_list)):
                    if G.has_edge(author_list[i], author_list[j]):
                        G[author_list[i]][author_list[j]]['weight'] += 1
                    else:
                        G.add_edge(author_list[i], author_list[j], weight=1)

    pos = nx.spring_layout(G)
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')

    node_x = []
    node_y = []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        marker=dict(
            showscale=True,
            colorscale='YlGnBu',
            reversescale=True,
            color=[],
            size=10,
            colorbar=dict(
                thickness=15,
                title='Node Connections',
                xanchor='left',
                titleside='right'
            ),
            line_width=2))

    node_adjacencies = []
    node_text = []
    for node, adjacencies in enumerate(G.adjacency()):
        node_adjacencies.append(len(adjacencies[1]))
        node_text.append(f'{adjacencies[0]}<br># of co-authors: {len(adjacencies[1])}')

    node_trace.marker.color = node_adjacencies
    node_trace.text = node_text

    fig = go.Figure(data=[edge_trace, node_trace],
                 layout=go.Layout(
                    title='Co-authorship Network Graph',
                    titlefont_size=16,
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=20, l=5, r=5, t=40),
                    annotations=[dict(
                        text="",
                        showarrow=False,
                        xref="paper", yref="paper",
                        x=0.005, y=-0.002)],
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))

    return fig.to_html(full_html=False)

@app.route('/search', methods=['POST'])
def search():
    search_query = request.form.get('search_query')
    searchSplit = search_query.split()
    if len(searchSplit) > 1:
        search_query = '+'.join(searchSplit)

    num_pages = 5


    feedArr = scrape_google_scholar(search_query, num_pages)


    data = pd.DataFrame(feedArr)


    data = clean_data(data)


    trends_html = visualize_trends(data)
    co_authorship_html = visualize_co_authorship(data)

    return render_template('result.html', trends_html=trends_html, co_authorship_html=co_authorship_html)

if __name__ == '__main__':
    app.run(debug=True)


#after running this script on your IDE it will tell you which localhost port its running on and
#open that localhost on your browser