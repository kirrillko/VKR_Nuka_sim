from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def read_index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("head_about.html")

@app.route("/feedback")
def feedback():
    return render_template("head_feedback.html")

@app.route("/terms")
def terms():
    return render_template("head_terms.html")

@app.route("/sources")
def sources():
    return render_template("head_sources.html")

@app.route("/simulator")
def simulator():
    return render_template("simulator.html")

@app.route("/test_turbine")
def test_turbine():
    return render_template("test_turbine.html")

@app.route("/test_3d")
def test_3d():
    return render_template("test_3D.html")

if __name__ == "__main__":
    app.run(debug=True)
