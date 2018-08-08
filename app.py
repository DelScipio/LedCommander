from flask import Flask, render_template, redirect
from engine import Engine

leds = Engine()

app = Flask(__name__)
app.debug = True


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/on")
def on():
    leds.stop()
    leds.start()

    return redirect("/")

@app.route("/off")
def off():
    leds.stop()
    return redirect("/")

@app.route("/luminosity")
def luminosityselect():
    levels = []
    for i in range(11):
        levels.append(i*10)

    return render_template("luminosity.html", levels=levels)

@app.route("/luminosity/<int:lum>")
def luminosity(lum):
    leds.vars.luminosity = lum/100
    return redirect("/luminosity")

@app.route("/sequences")
def sequences():
    listix = []
    for i in range(1, leds.vars.PIXEL_COUNT):
        if leds.vars.PIXEL_COUNT%i == 0:
            listix.append(i)
    return render_template("sequences.html", listix=listix)

@app.route("/sequences/<int:seqs>")
def sequencesapply(seqs):
    leds.vars.sequences = seqs
    return redirect("/sequences")

@app.route("/color/")
def color():
    colorlist = ["red","blue","green","white","purple", "yellow", "cyan", "clear"]
    return render_template("color.html", colorlist = colorlist)

@app.route("/color/<string:color>")
def colors(color):
    leds.vars.color = color

    return redirect("/color")

@app.route("/maximize")
def maximize():
    if leds.vars.maximize == True:
        leds.vars.maximize = False
    else:
        leds.vars.maximize = True
    return redirect("/")

@app.route("/uniform/")
def uniform():
    leds.stop()
    leds.vars.effect = "static"
    leds.start()
    return redirect("/")

@app.route("/rainbow")
def rainbow():
    leds.stop()
    leds.vars.effect = "rainbow"
    leds.start()
    return redirect("/")

@app.route("/random")
def random():
    leds.stop()
    leds.vars.effect = "random"
    leds.start()
    return redirect("/")

@app.route("/blink")
def blink():
    leds.stop()
    leds.vars.effect = "blink"
    leds.start()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")