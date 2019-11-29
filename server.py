from flask import Flask, render_template, request, jsonify, make_response
from packages import main, getNames, getPackage

packageList = main()
nameList = getNames(packageList)

app = Flask(__name__)

@app.route("/")
def server(data=nameList):
    return render_template('home.html', names=data)


@app.route("/<section>")
def package(section):
    data = getPackage(packageList, section)
    return render_template('package.html', package=data)


@app.route("/return-package", methods=["POST"])
def returnPackage():
    req = request.get_json()
    packageName = req['name']
    packageDict = getPackage(packageList, packageName)
    return jsonify({'package' : packageDict})


if __name__ == '__main__':
    app.run(debug=True)
