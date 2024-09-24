from app.models import usuario
from app.models import produto
from app import db
from app.forms import LoginForm
from datetime import timedelta
from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
import secrets

def init_app(app):
        
    #@app.route("/")
    #def principal():        
        #return render_template("seu_job/index.html")

    @app.route("/", methods=["GET", "POST"])
    def index():
        form = LoginForm()

        if form.validate_on_submit():
        #if request.method == "POST":
            user = usuario.query.filter_by(email=form.email.data).first()

            if not user:
                flash("Email do usuário incorreto, por favor verifique!")
                return redirect(url_for("index"))
                #return render_template("user_inv.html")

            elif not check_password_hash(user.senha, form.senha.data):
                flash("Senha do usuário incorreto, por favor verifique!")
                return redirect(url_for("index"))
                #return render_template("user_inv.html")

            login_user(user, remember=form.remember.data, duration=timedelta(days=7))
            #login_user(user)
            return redirect(url_for("inicio"))
        
        return render_template("index.html", form=form)

    @app.route("/logout")
    def logout():
            logout_user()
            return redirect(url_for("index"))
    
    @app.route("/inicio")
    def inicio():        
        return render_template("/inicio.html", usuarios=db.session.execute(db.select(usuario).order_by(usuario.id)).scalars())

    @app.route("/excluir/<int:id>")
    def excluir_user(id):
        delete=usuario.query.filter_by(id=id).first()
        db.session.delete(delete)
        db.session.commit()
        return redirect(url_for("inicio"))
    
    @app.route("/cad_user", methods=["GET", "POST"])
    def cad_user():        
        if request.method == "POST":
            user = usuario()
            user.email = request.form["email"]
            user.nome = request.form["nome"]        
            user.senha = generate_password_hash(request.form["senha"])
            db.session.add(user)
            db.session.commit()
                            
            flash("Usuario criado com sucesso!")       
            return redirect(url_for("cad_user"))
        return render_template("cad_user.html")
    
    @app.route("/atualiza_user/<int:id>", methods=["GET", "POST"])
    def atualiza_user(id):
        usu01=usuario.query.filter_by(id=id).first()
        if request.method == "POST":
            email_usuario = request.form["email"]
            nome_usuario = request.form["nome"]
            
            flash("Dados do usuário alterados com sucesso!")     

            usu01.query.filter_by(id=id).update( {"email":email_usuario, "nome":nome_usuario})
            
            db.session.commit()
            return redirect(url_for("inicio"))
        return render_template("atualiza_user.html", usu01=usu01)
    
    @app.route("/prod")
    def prod():        
        return render_template("/produto.html", prod01=db.session.execute(db.select(produto).order_by(produto.id)).scalars())

    @app.route("/excluir_produto/<int:id>")
    def excluir_produto(id):
        delete=produto.query.filter_by(id=id).first()
        db.session.delete(delete)
        db.session.commit()
        return redirect(url_for("prod"))

    @app.route("/cad_produto", methods=["GET", "POST"])
    def cad_produto():        
        if request.method == "POST":
            prod = produto()
            prod.nome = request.form["nome"]        
            prod.codigo = request.form["codigo"]      
            prod.quantidade = request.form["quantidade"]      
            db.session.add(prod)
            db.session.commit()
                            
            flash("Produto criado com sucesso!")       
            return redirect(url_for("cad_produto"))
        return render_template("cad_produto.html")

    @app.route("/atualiza_produto/<int:id>", methods=["GET", "POST"])
    def atualiza_produto(id):
        prod01=produto.query.filter_by(id=id).first()
        if request.method == "POST":
            nome_produto = request.form["nome"]
            codigo_produto = request.form["codigo"]
            quantidade_produto = request.form["quantidade"]
            
            flash("Dados do produto alterados com sucesso!")     

            prod01.query.filter_by(id=id).update( {"nome":nome_produto, "codigo":codigo_produto, "quantidade":quantidade_produto})
            
            db.session.commit()
            return redirect(url_for("prod"))
        return render_template("atualiza_produto.html", prod01=prod01)
