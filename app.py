from flask import Flask, jsonify
from quotes import funny_quotes
import random
from routes import init_api_routes
from routes import init_website_routes

app = Flask(__name__)

#init_api_routes(app)
init_website_routes(app)

#candidates = funny_quotes()
@app.template_filter('reports')
def funny_quotes(asd):
    reports = {}
    report_list = []
    #dir = os.chdir('./tam_api')
    file_obj = open('quotes.txt', 'r')
    text = file_obj.read()
    text = text.split('\n')
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
    #text = text.strip().strip().strip('\t')
    report_list = sorted(report_list, key=lambda k: k['author'])
    return report_list



def senior_candidate(candidates):
    result = []
    for candidate in candidates:
        for experience in candidate['experience']:
            if experience['years'] >= 5:
                result.append({
                    'first_name':candidate['first_name'],
                    'last_name':candidate['last_name'],
                    'years':experience['years'],
                    'domain':experience['domain']
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
def candidate_by_id(id):
	#candidate = DATA_PROVIDER.get_candidate(id);
	if id:
		return jsonify({id: "anda a la cancha bobo"})
	else:
		#return jsonify({id: "sos boludo y no tenes huevos"})
		#
		# In case we did not find the candidate by id
		# we send HTTP 404 - Not Found error to the client
		#
		abort(404)

@app.route("/api/TAM")
def serve_funny_quote():
    quotes = funny_quotes()
    nr_of_quotes = len(quotes)
    selected_quote = quotes[random.randint(0, nr_of_quotes - 1)]
    return jsonify(selected_quote)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
