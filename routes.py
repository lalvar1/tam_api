from flask import jsonify
from flask import render_template


def init_api_routes(app):
    if app:
        app.add_url_rule('/api/candidate/<string:id>', 'candidate_by_id', candidate_by_id, methods=['GET'])
        app.add_url_rule('/api', 'list_routes', list_routes, methods=['GET'], defaults={'app': app})


def page_about():
    return render_template('about.html', selected_menu_item="about")


def page_index():
    return render_template('index.html', selected_menu_item="index")


def page_reports():
    return render_template('reports.html', selected_menu_item="reports")


def page_crew():
    return render_template('crew.html', selected_menu_item="crew")


def page_veraz():
    return render_template('veraz.html', selected_menu_item="veraz")


def init_website_routes(app):
    if app:
        app.add_url_rule('/about', 'page_about', page_about, methods=['GET'])
        app.add_url_rule('/', 'page_index', page_index, methods=['GET'])
        app.add_url_rule('/reports', 'page_reports', page_reports, methods=['GET'])
        app.add_url_rule('/crew', 'page_crew', page_crew, methods=['GET'])
        app.add_url_rule('/veraz', 'page_veraz', page_veraz, methods=['GET'])


def list_routes(app):
    result = []
    for rt in app.url_map.iter_rules():
        result.append({
            'methods': list(rt.methods),
            'route': str(rt)
        })
    return jsonify({'routes': result, 'total': len(result)})
