from flask import Flask, render_template
from packages import main, getNames, getPackage

packageList = main()
nameList = getNames(packageList)
#packageList = ['kakkara', 'makkara', 'jakkara']

app = Flask(__name__)

@app.route("/")
def server(data=nameList):
    return render_template('home.html', names=data)


@app.route("/<section>")
def package(section):
    data = getPackage(packageList, section)
    return render_template('package.html', package=data)


if __name__ == '__main__':
    app.run(debug=True)
