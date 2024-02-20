from flask import Flask, render_template
from conecta_db import DB
import pandas as pd

app = Flask(__name__)
carregamento = '433000'
carre = DB()
car = carre.car(carregamento)

df = pd.DataFrame(car)
#print(df[df['DESC_TECNICA'].str.endswith('EXP')]['NUM_ORDEM'].tolist())



def generate_tree(df, carregamento):
    tree_html = f'<div class="tree"><ul><li><a href="#">{carregamento}</a><ul>'
    for index, row in df.iterrows():
        if row["DESC_TECNICA"].endswith('EXP'):
            tree_html += f'<li><a href="#">{row["NUM_ORDEM"]}</a>'
            next_level_html = generate_next_level_tree(row["NUM_ORDEM"])
            if next_level_html:
                tree_html += '<ul>'
                tree_html += next_level_html
                tree_html += '</ul>'
            tree_html += '</li>'
    tree_html += '</ul></div>'
    return tree_html


def generate_next_level_tree(num_ordem):
    df_lv2 = pd.DataFrame(carre.filhos(carregamento, num_ordem))
    if df_lv2.empty:
        return ""
    next_level_html = "<ul>"
    for _, row in df_lv2.iterrows():
        next_level_html += f'<li><a href="#">{row["NUM_ORDEM"]}</a>'
        next_level_html += generate_next_level_tree(row["NUM_ORDEM"])
        next_level_html += "</li>"
    next_level_html += "</ul>"
    return next_level_html




@app.route('/')
def criar():
    tree_html = generate_tree(df, carregamento)
    return render_template('template.html', tree_html=tree_html)


if __name__ == '__main__':
    app.run(debug=True)
