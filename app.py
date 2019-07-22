from flask import Flask, jsonify, Response
import random
from routes import init_website_routes

app = Flask(__name__)

init_website_routes(app)


@app.template_filter('reports')
def funny_quotes(asd):
    report_list = []
    file_obj = open('data/quotes.txt', 'r')
    text = file_obj.read()
    text = text.split('\n')

    aux_dict = None
    for line in text:
        line = line.strip(',')
        if '{' in line or '}' in line:
            continue
        lines = line.split(':')
        if len(lines) > 1:
            d = {lines[0]: lines[1].strip('"')}
            if 'author' in line:
                aux_dict = d
            elif 'quote' in line:
                aux_dict.update(d)
                report_list.append(aux_dict)
    report_list = sorted(report_list, key=lambda k: k['author'])
    return report_list


@app.template_filter('veraz')
def debt_handler(asd):
    report_list = []
    file_obj = open('data/veraz.txt', 'r')
    text = file_obj.read()
    text = text.split('\n')

    aux_dict = None
    for line in text:
        line = line.strip(',')
        if '{' in line or '}' in line:
            continue
        lines = line.split(':')
        if len(lines) > 1:
            d = {lines[0]: lines[1].strip('"')}
            if 'debtor' in line:
                aux_dict = d
                report_list.append(aux_dict)
            elif 'amount' in line:
                aux_dict.update(d)
            elif 'reason' in line:
                aux_dict.update(d)
            elif 'date' in line:
                aux_dict.update(d)
    report_list = sorted(report_list, key=lambda k: k['debtor'])
    return report_list


def senior_candidate(candidates):
    result = []
    for candidate in candidates:
        for experience in candidate['experience']:
            if experience['years'] >= 5:
                result.append({
                    'first_name': candidate['first_name'],
                    'last_name': candidate['last_name'],
                    'years': experience['years'],
                    'domain': experience['domain']
                })
                break

    return result


@app.route("/api", methods=["GET"])
def list_routes():
    result = []
    for rt in app.url_map.iter_rules():
        result.append({
            "methods": list(rt.methods),
            "route": str(rt)
        })
    return jsonify({"routes": result, "total": len(result)})


@app.route("/api/candidate/<string:id>", methods=["GET"])
def candidate_by_id(response_id):
    if response_id:
        return jsonify({response_id: "anda a la cancha bobo"})
    else:
        pass


@app.route("/api/TAM")
def serve_funny_quote():
    quotes = funny_quotes(None)
    nr_of_quotes = len(quotes)
    selected_quote = quotes[random.randint(0, nr_of_quotes - 1)]
    return jsonify(selected_quote)


@app.route("/afrika")
def go_to_the_stadium():
    return Response('Andá a la cancha, bobo.\n', 401,
                    {'WWW-Authenticate': 'Basic realm="Login Required"'})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
