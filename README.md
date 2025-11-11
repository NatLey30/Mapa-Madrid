# Madrid Road Network Visualization

## Project Overview
This project builds and visualizes a **graph-based map of Madrid** using data extracted from two CSV files — one containing **road intersections (nodes)** and another containing **street connections (edges)**.  
The final graph representation is rendered as an image, showing the road network structure of the city.

## Data Sources
- **`cruces.csv`** – Contains the coordinates or identifiers of all intersections in Madrid. Each row represents a node in the graph.  
- **`direcciones.csv`** – Describes the road connections between intersections. Each row defines an edge between two nodes, possibly including additional information like distance or road type.

## How It Works
1. **Data Loading:**  
   The project reads the two CSV files using a data analysis library..

2. **Graph Construction:**  
   The intersections and connections are used to build a **graph structure**, where:
   - Nodes = intersections  
   - Edges = roads connecting them  

3. **Visualization:**  
   The graph is plotted and saved, visually representing Madrid’s road network.

## Output
The resulting file, **`grafp.jpg`**, displays the reconstructed **road network of Madrid**, with nodes representing crossings and edges representing road connections.

![Madrid Graph](grafp.jpg)
