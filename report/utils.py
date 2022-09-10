import matplotlib.pyplot as plt
import base64
from io import BytesIO

def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph

def get_pie(x, labels, title):
    plt.switch_backend('AGG')
    plt.figure(figsize=(10, 5))
    plt.pie(x, labels=labels, counterclock=False, autopct=lambda y: f'{y:.1f}%\n({(y/100)*sum(x):.0f} HS)')
    plt.legend(loc="right", bbox_to_anchor=(1.8,0), title=title)
    plt.tight_layout()
    graph = get_graph()
    return graph

def get_pie2(x, labels, title):
    plt.switch_backend('AGG')
    plt.figure(figsize=(10, 5))
    plt.pie(x, labels=labels, counterclock=False, autopct=lambda y: f'{y:.1f}%\n({(y/100)*sum(x):.0f} HS)')
    plt.legend(loc="right", bbox_to_anchor=(1.5,0), title=title)
    plt.tight_layout()
    graph = get_graph()
    return graph



