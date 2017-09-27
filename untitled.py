import datetime, pymysql
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#A conexão está aberta, lembre-se que não se pode fazer isso
#em produção (vida real), pois pode ocorrer falhas na segurança
#é recomendado sempre fechar com conexao.close()
conexao = pymysql.connect(
    host='localhost',
    user='root',
    passwd='alunoifro',
    db='beatriz'
)
conexao_cursor = conexao.cursor()


@app.route('/', methods=['GET', 'POST'])
def index():
    query_sql = """
        SELECT * FROM tb_produto
    """
    conexao_cursor.execute(query_sql)
    produtos = conexao_cursor.fetchall()

    return render_template('index.html', produtos=produtos)

@app.route('/criar_tabela')
def criar_tabela():
    query_sql = """
        CREATE TABLE tb_produto (
            id int(11) NOT NULL AUTO_INCREMENT,
            nome varchar(100) DEFAULT NULL,
            data_envio datetime DEFAULT NULL,
            PRIMARY KEY (id),
            UNIQUE KEY tb_produto_id_uindex (id)
        )
    """
    conexao_cursor.execute(query_sql)

    return '<h1> Tabela criada com sucesso! </h1>'

@app.route('/excluir_tabela')
def excluir_tabela():

    query_sql = """
        DROP TABLE lista_flask.tb_produto
    """
    conexao_cursor.execute(query_sql)
    return '<h1> Tabela excluída com sucesso!</h1>'

@app.route('/adicionar', methods=['GET', 'POST'])
def adicionar_produto():
    if request.method == 'POST':
        nome = request.form['nome']
        data_envio = datetime.datetime.now()
        query_sql = """
            INSERT INTO tb_produto (nome, data_envio)
            VALUES ('{}', '{}')
        """.format(nome,data_envio)

        conexao_cursor.execute(query_sql)
        conexao.commit()

        return redirect(url_for('index'))
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)