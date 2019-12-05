from flask import Flask, render_template, request, jsonify
from package_parser import main, get_names, get_package

PackageList = main()
NameList = get_names(PackageList)

app = Flask(__name__ , static_url_path='/static', static_folder='static')


@app.route("/")
def server(data=NameList):
    return render_template('home.html', names=data)


@app.route("/mobile")
def mobile(data=NameList):
    return render_template('mobile.html', names=data)


@app.route("/<section>")
def package(section):
    data = get_package(PackageList, section)
    return render_template('package.html', package=data)


@app.route("/return-package", methods=["POST"])
def return_package():
    req = request.get_json()
    package_name = (req['name']).strip(", ")
    package_dict = get_package(PackageList, package_name)
    return jsonify({'package': package_dict})


if __name__ == '__main__':
    # app.run()
    app.run(debug=True)
