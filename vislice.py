import bottle
import model

SKRIVNOST = "moja_prva_skrivnost"
DATOTEKA_S_STANJEM = "stanje.json"
DATOTEKE_Z_BESEDAMI = "besede.txt"

vislice = model.Vislice(DATOTEKA_S_STANJEM, DATOTEKE_Z_BESEDAMI)
vislice.nalozi_igre_iz_datoteke()

@bottle.get("/")
def index():
    return bottle.template("Vislice\\views\\index.tpl")

@bottle.post("/nova_igra")
def nova_igra():
    id_igre = vislice.nova_igra()
    bottle.request.set_cookie("idigre", "idigre{}".format(id_igre),secret=SKRIVNOST, path="/")
    bottle.redirect("/igra/")

@bottle.get("/igra/")
def pokazi_igro():
    id_igre=int(bottle.request.set_cookie("idigre",secret=SKRIVNOST). split("e")[1])
    igra, poskus = vislice.igre[id_igre]
    return bottle.template("Vislice\\views\\igra.tpl", igra=igra, poskus=poskus)

@bottle.post("/igra/")
def ugibaj():
    id_igre =int(bottle.request.set_cookie("idigre",secret=SKRIVNOST). split("e")[1])
    crka = bottle.request.forms.getunicode("crka")
    vislice.ugibaj(id_igre, crka)
    bottle.redirect("/igra/")

@bottle.get('/img/<picture>')
def serve_pictures(picture):
    return bottle.static_file (picture, root="Vislice\\img")


bottle.run(port=80, reloader=True, debug=True)

