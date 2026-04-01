import urllib.request
import urllib.parse

def generate_mermaid_image(mermaid_text, filename):
    # Quickchart has a mermaid endpoint but its graphviz endpoint is more stable for this format
    # A graphviz format is better
    pass

def generate_graphviz_image(dot_text, filename):
    url = "https://quickchart.io/graphviz"
    import json
    data = json.dumps({"graph": dot_text}).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req) as response:
        with open(filename, 'wb') as f:
            f.write(response.read())

dot_a = """
digraph G {
  rankdir=LR;
  node [shape=box, style=filled, fillcolor="#ececff", color="#9370db", penwidth=2];
  
  InF [shape=circle, label="f", fillcolor="#e0ffd4", color="#32cd32"];
  InG [shape=circle, label="g", fillcolor="#e0ffd4", color="#32cd32"];
  OutX [shape=circle, label="x", fillcolor="#e0ffd4", color="#32cd32"];
  OutY [shape=circle, label="y", fillcolor="#e0ffd4", color="#32cd32"];
  
  SumX [shape=circle, label="Σ", fillcolor="#ffebcd", color="#ff8c00"];
  SumY [shape=circle, label="Σ", fillcolor="#ffebcd", color="#ff8c00"];
  
  IntX1 [label="∫"];
  IntX2 [label="∫"];
  IntY [label="∫"];
  
  Gain5 [label="Gain: 5"];
  Gain2x [label="Gain: 2"];
  Gain2y [label="Gain: 2"];
  
  InF -> SumX [label="+"];
  InG -> Gain5;
  Gain5 -> SumY [label="+"];
  
  SumX -> IntX1 [label="x_ddot"];
  IntX1 -> IntX2 [label="x_dot"];
  IntX2 -> OutX [label="x"];
  
  SumY -> IntY [label="y_dot"];
  IntY -> OutY [label="y"];
  
  IntX1 -> Gain2x;
  Gain2x -> SumX [label="-"];
  IntX2 -> SumX [label="-"];
  
  SumY -> Gain2y;
  Gain2y -> SumX [label="+"];
  
  IntY -> SumY [label="-"];
  IntX2 -> SumY [label="+"];
}
"""

dot_b1 = """
digraph G {
  rankdir=LR;
  node [shape=box, style=filled, fillcolor="#ececff", color="#9370db", penwidth=2];
  
  InX [shape=circle, label="x", fillcolor="#e0ffd4", color="#32cd32"];
  OutZ [shape=circle, label="z", fillcolor="#e0ffd4", color="#32cd32"];
  SumZ [shape=circle, label="Σ", fillcolor="#ffebcd", color="#ff8c00"];
  IntB1 [label="∫"];
  
  InX -> SumZ [label="+"];
  InX -> IntB1;
  IntB1 -> SumZ [label="∫x dt"];
  SumZ -> OutZ [label="z"];
}
"""

dot_b2 = """
digraph G {
  rankdir=LR;
  node [shape=box, style=filled, fillcolor="#ececff", color="#9370db", penwidth=2];
  
  InZ [shape=circle, label="z", fillcolor="#e0ffd4", color="#32cd32"];
  OutX [shape=circle, label="x", fillcolor="#e0ffd4", color="#32cd32"];
  SumV [shape=circle, label="Σ", fillcolor="#ffebcd", color="#ff8c00"];
  IntB2 [label="∫"];
  
  InZ -> SumV [label="+"];
  SumV -> IntB2 [label="x"];
  IntB2 -> SumV [label="-", color="red", fontcolor="red"];
  SumV -> OutX [label="x"];
}
"""

generate_graphviz_image(dot_a, "diagram_a.png")
generate_graphviz_image(dot_b1, "diagram_b1.png")
generate_graphviz_image(dot_b2, "diagram_b2.png")
print("All images generated.")
