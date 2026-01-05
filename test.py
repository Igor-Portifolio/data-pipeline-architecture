'''
dados = {
        "nome_completo": [
            "   JOÃO DA SILVA sauçe   ",
            "maria eduarda dos santos",
            "CARLOS ALBERTO DE SOUZA",
            "ana beatriz di paulo",
            "FERNANDA E MARIA COM Ninguém",
            "josé roberto du arte",
            "   LUIZ INÁCIO lula da silva  ",
            "cláudia raia e jarbas homem de mello",
            "pedro álvares cabral",
            "maria-do-carmo ferreira"
        ]
    }

df = pd.DataFrame(dados)

# Instancia a classe
trat = Standard_text(df, coluna="nome_completo")

trat.normalize_text(name=True)

pass'''