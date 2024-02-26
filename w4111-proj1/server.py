"""
Columbia's COMS W4111.001 Introduction to Databases
Example Webserver
To run locally:
    python server.py
Go to http://localhost:8111 in your browser.
A debugger such as "pdb" may be helpful for debugging.
Read about it online.
"""
import os
  # accessible as a variable in index.html:
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response, url_for, session

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
#name means everything you need in Flask is in this directory
app = Flask(__name__, template_folder=tmpl_dir)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
#
# The following is a dummy URI that does not connect to a valid database. You will need to modify it to connect to your Part 2 database in order to use the data.
#
# XXX: The URI should be in the format of: 
#
#     postgresql://USER:PASSWORD@34.73.36.248/project1
#
# For example, if you had username zy2431 and password 123123, then the following line would be:
#
#     DATABASEURI = "postgresql://zy2431:123123@34.73.36.248/project1"
#
# Modify these with your own credentials you received from TA!
DATABASE_USERNAME = "ayl2148"
DATABASE_PASSWRD = "football"
DATABASE_HOST = "34.148.107.47" # change to 34.28.53.86 if you used database 2 for part 2
DATABASEURI = f"postgresql://{DATABASE_USERNAME}:{DATABASE_PASSWRD}@{DATABASE_HOST}/project1"

# This line creates a database engine that knows how to connect to the URI above.
#
engine = create_engine(DATABASEURI, future=True)

#
# Example of running queries in your database
# Note that this will probably not work if you already have a table named 'test' in your database, containing meaningful data. 
# This is only an example showing you how to run queries in your database using SQLAlchemy.
#
with engine.connect() as conn:
	create_table_command = """
	CREATE TABLE IF NOT EXISTS test (
		id serial,
		name text
	)
	"""
	res = conn.execute(text(create_table_command))
	insert_table_command = """INSERT INTO test(name) VALUES ('grace hopper'), ('alan turing'), ('ada lovelace')"""
	res = conn.execute(text(insert_table_command))
	# you need to commit for create, insert, update queries to reflect
	conn.commit()

#python decorator, decorate/add functionality to function below it
@app.before_request
def before_request():
	"""
	This function is run at the beginning of every web request 
	(every time you enter an address in the web browser).
	We use it to setup a database connection that can be used throughout the request.

	The variable g is globally accessible.
	"""
	try:
		g.conn = engine.connect()
	except:
		print("uh oh, problem connecting to database")
		import traceback; traceback.print_exc()
		g.conn = None

@app.teardown_request
def teardown_request(exception):
	"""
	At the end of the web request, this makes sure to close the database connection.
	If you don't, the database could run out of memory!
	"""
	try:
		g.conn.close()
	except Exception as e:
		pass


#
# @app.route is a decorator around index() that means:
#   run index() whenever the user tries to access the "/" path using a GET request
#
# If you wanted the user to go to, for example, localhost:8111/foobar/ with POST or GET then you could use:
#
#       @app.route("/foobar/", methods=["POST", "GET"])
#
# PROTIP: (the trailing / in the path is important)
# 
# see for routing: https://flask.palletsprojects.com/en/1.1.x/quickstart/#routing
# see for decorators: http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/
#
@app.route('/')
def index():
	"""
	request is a special object that Flask provides to access web request information:

	request.method:   "GET" or "POST"
	request.form:     if the browser submitted a form, this contains the data in the form
	request.args:     dictionary of URL arguments, e.g., {a:1, b:2} for http://localhost?a=1&b=2

	See its API: https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data
	"""

	# DEBUG: this is debugging code to see what request looks like
	print(request.args)


	#
	# example of a database query
	#
	
	select_query = "SELECT name from player WHERE passing_yds > 1000"
	cursor = g.conn.execute(text(select_query))
	names = []
	for result in cursor:
		names.append(result[0])
		#names.append(result[1])
	cursor.close()

	#
	# Flask uses Jinja templates, which is an extension to HTML where you can
	# pass data to a template and dynamically generate HTML based on the data
	# (you can think of it as simple PHP)
	# documentation: https://realpython.com/primer-on-jinja-templating/
	#
	# You can see an example template in templates/index.html
	#
	# context are the variables that are passed to the template.
	# for example, "data" key in the context variable defined below will be 
	# accessible as a variable in index.html:
	#
	#     # will print: [u'grace hopper', u'alan turing', u'ada lovelace']
	#     <div>{{data}}</div>
	#     
	#     # creates a <div> tag for each element in data
	#     # will print: 
	#     #
	#     #   <div>grace hopper</div>
	#     #   <div>alan turing</div>
	#     #   <div>ada lovelace</div>
	#     #
	#     {% for n in data %}
	#     <div>{{n}}</div>
	#     {% endfor %}
	#
	context = dict(data = names)

	# render_template looks in the templates/ folder for files.
	# for example, the below file reads template/index.html
	#
	return render_template("index.html", **context)

#
# This is an example of a different path.  You can see it at:
# 
#     localhost:8111/another
#
# Notice that the function name is another() rather than index()
# The functions for each app.route need to have different names
#

@app.route('/city_stadium', methods=['POST'])
def stadium_search():
	city= request.form['city_name']
	params = {}
	params["city"] = city

	query=(text('SELECT s.name, s.city, s.sponsor, p.team_name FROM stadium s, plays_in p WHERE s.city = :city AND p.stadium_name=s.name ')
	)
	cursor = g.conn.execute(query, params)
	result= cursor 
	rows= [dict(name=row[0], city=row[1], sponsor=row[2], team_name=row[3]) for row in result]
	cursor.close()
	print(rows)
	      # Check if there are any results
	if len(rows) == 0:
		# If there are no results, render the "no results" template
		return render_template('no_results.html')
	else:
		# If there are results, render the template that displays the results
		return render_template('city_stadium.html', rows=rows)

@app.route('/mascot_search', methods=['POST'])
def mascot_search():
	team= request.form['team_name']
	params = {}
	params["team"] = team

	query=(text('SELECT m.team_name, r.mascot_name, m.description FROM mascot m, represents r WHERE m.team_name= :team AND r.team_name= :team'))
	cursor = g.conn.execute(query, params)
	result= cursor 
	rows= [dict(team_name=row[0], mascot_name=row[1], mascot_description=row[2]) for row in result]
	cursor.close()
	print(rows)
	      # Check if there are any results
	if len(rows) == 0:
		# If there are no results, render the "no results" template
		return render_template('no_results.html')
	else:
		# If there are results, render the template that displays the results
		return render_template('mascot.html', rows=rows)

@app.route('/player_contract', methods=['POST'])
def player_contract():  
    person_id = request.form['person_id']
    params = {'person_id': person_id}

    query = (text('SELECT p.person_id, p.name, pf.name as team, c.amount, c.start_year, c.term \
			FROM player p, plays_for pf, player_contract c, signs s \
			WHERE p.person_id = pf.person_id \
			AND p.person_id = c.person_id \
			AND s.person_id = pf.person_id \
			AND p.person_id like :person_id '))			
    cursor = g.conn.execute(query, params)
    rows= [{'person_id': row[0], 'name': row[1], 'team': row[2], 
            'amount': row[3], 'start_year': row[4], 'term': row[5]} for row in cursor]
    cursor.close()
    return render_template('contract_search.html', rows=rows)

@app.route('/team_search', methods=['POST'])
def team_search():  
    team_name = request.form['team_name']
    params = {'team_name': team_name}
    query=(text('SELECT t.name, t.record, t.city, t.sb_wins, c.name, c.role, c.record FROM team t, coach c, coaches f WHERE f.person_id=c.person_id AND f.name=t.name AND t.name= :team_name'))
    cursor = g.conn.execute(query, params)
    rows= [{'team_name': row[0], 'team_record': row[1], 'team_city': row[2], 'team_sb': row[3], 'coach_name': row[4], 'coach_role': row[5], 'coach_record': row[6]} for row in cursor]
    cursor.close()
    return render_template('team_search.html', rows=rows)

@app.route('/game_search', methods=['POST'])
def game_search():
	team= request.form['team_name']
	params = {}
	params["team"] = team

	query=(text('SELECT g.winning_team, g.losing_team, g.score, g.date_time FROM game g WHERE g.winning_team = :team OR g.losing_team = :team'))
	cursor = g.conn.execute(query, params)
	result= cursor 
	rows= [dict(win_team=row[0], losing_team=row[1], score=row[2], date=row[3]) for row in result]
	cursor.close()
	print(rows)
	      # Check if there are any results
	if len(rows) == 0:
		# If there are no results, render the "no results" template
		return render_template('no_results.html')
	else:
		# If there are results, render the template that displays the results
		return render_template('game.html', rows=rows)

@app.route('/Search_a_Player', methods=['POST'])
def player_search():
	passing_upper= request.form['passing_upper']
	passing_lower= request.form['passing_lower']
	rushing_upper= request.form['rushing_upper']
	rushing_lower= request.form['rushing_lower']
	receiving_upper= request.form['receiving_upper']
	receiving_lower= request.form['receiving_lower']
	tds_upper= request.form['tds_upper']
	tds_lower=request.form['tds_lower']

	params = {}
	params["upper_p"] = passing_upper
	params["lower_p"] = passing_lower
	params["upper_r"] = rushing_upper
	params["lower_r"] = rushing_lower
	params["upper_v"] = receiving_upper
	params["lower_v"] = receiving_lower
	params["upper_t"] = tds_upper
	params["lower_t"] = tds_lower

	query=(text('SELECT name, passing_yds, rushing_yds, receiving_yds, total_tds FROM player WHERE \
	passing_yds <= :upper_p AND passing_yds >= :lower_p AND \
	rushing_yds <= :upper_r AND rushing_yds >= :lower_r AND \
	receiving_yds <= :upper_v AND receiving_yds >= :lower_v AND \
	total_tds <= :upper_t AND total_tds >= :lower_t')
	)
	cursor = g.conn.execute(query, params)
	result= cursor 
	rows= [dict(name=row[0], passing_yds=row[1], rushing_yds=row[2], receiving_yds= row[3], total_tds=row[4]) for row in result]
	cursor.close()
	print(rows)
	      # Check if there are any results
	if len(rows) == 0:
		# If there are no results, render the "no results" template
		return render_template('no_results.html')
	else:
		# If there are results, render the template that displays the results
		return render_template('player_search.html', rows=rows)

@app.route('/admin')
def admin():
	return f"Hello Admin!"
	#return redirect(url_for("user", name="Admin!"))
    
@app.route('/view_fantasy_team', methods=['POST'])
def view_fantasy_team():
    team_name = request.form['team_name']
    password = request.form['password']
    
    params = {'team_name': team_name, 'password': password}
    
    # Check team_name is valid and password are valid
    check_team_command = (text('SELECT * FROM fantasy_team WHERE name like :team_name'))
    cursor = g.conn.execute(check_team_command, params)
    team_row = [{'team_name': row[0], 'password': row[1]} for row in cursor]
    cursor.close()
    
    if not team_row:
        return render_template('invalid_team_name.html')
    
    if team_row[0]['password'] != password:
        return render_template('invalid_team_password.html')
    
    query = (text('SELECT p.name, p.position, pf.name as team \
                    FROM player p, plays_for pf, on_fantasy_team oft \
                    WHERE oft.name like :team_name \
                    AND oft.person_id = p.person_id \
                    AND pf.person_id = oft.person_id'))
    
    cursor = g.conn.execute(query, params)
    team_rows= [{'name': row[0], 'position': row[1], 'team': row[2]} for row in cursor]
    cursor.close()
    
    session['team_name'] = team_name
    
    return render_template('view_fantasy_team.html', team_rows=team_rows)
    
    
@app.route('/get_person_id', methods=['POST'])
def get_person_id():
    player_name = request.form['player_name']
    
    # Get team_rows
    team_name = session.get('team_name', None)
    params = {'team_name': team_name}
    query = (text('SELECT p.name, p.position, pf.name as team \
                    FROM player p, plays_for pf, on_fantasy_team oft \
                    WHERE oft.name like :team_name \
                    AND oft.person_id = p.person_id \
                    AND pf.person_id = oft.person_id'))
    
    cursor = g.conn.execute(query, params)
    team_rows= [{'name': row[0], 'position': row[1], 'team': row[2]} for row in cursor]
    cursor.close()

    # Get person_id_rows
    params = {'player_name': player_name}
    query = (text('SELECT p.person_id, p.name, p.position, pf.name as team \
                    FROM player p, plays_for pf \
                    WHERE p.name like :player_name\
                    AND p.person_id = pf.person_id'))
    
    cursor = g.conn.execute(query, params)
    person_id_rows= [{'person_id': row[0], 'name': row[1], 'position': row[2], 'team': row[3]} for row in cursor]
    cursor.close()
    
    return render_template('view_fantasy_team.html', team_rows=team_rows, person_id_rows=person_id_rows)


@app.route('/add_player_to_fantasy_team', methods=['POST'])
def add_player_to_fantasy_team():
    person_id = request.form['person_id']
    team_name = session.get('team_name', None)
    
    params = {'person_id': person_id, 'team_name': team_name}
    insert_command = (text('INSERT INTO on_fantasy_team(person_id, name) \
                            VALUES (:person_id, :team_name)'))
    g.conn.execute(insert_command, params)
    g.conn.commit()
    
    # Get team_rows
    team_name = session.get('team_name', None)
    params = {'team_name': team_name}
    query = (text('SELECT p.name, p.position, pf.name as team \
                   FROM player p, plays_for pf, on_fantasy_team oft \
                   WHERE oft.name like :team_name \
                   AND oft.person_id = p.person_id \
                   AND pf.person_id = oft.person_id'))
    
    cursor = g.conn.execute(query, params)
    team_rows= [{'name': row[0], 'position': row[1], 'team': row[2]} for row in cursor]
    cursor.close()
    
    return render_template('view_fantasy_team.html', team_rows=team_rows)

    
@app.route('/remove_player_from_fantasy_team', methods=['POST'])
def remove_player_from_fantasy_team():
    person_id = request.form['person_id']
    team_name = session.get('team_name', None)
    
    params = {'person_id': person_id, 'team_name': team_name}
    delete_command = (text('DELETE FROM on_fantasy_team \
                            WHERE name like :team_name \
                            AND person_id like :person_id'))
    g.conn.execute(delete_command, params)
    g.conn.commit()
    
    # Get team_rows
    team_name = session.get('team_name', None)
    params = {'team_name': team_name}
    query = (text('SELECT p.name, p.position, pf.name as team \
                   FROM player p, plays_for pf, on_fantasy_team oft \
                   WHERE oft.name like :team_name \
                   AND oft.person_id = p.person_id \
                   AND pf.person_id = oft.person_id'))
    
    cursor = g.conn.execute(query, params)
    team_rows= [{'name': row[0], 'position': row[1], 'team': row[2]} for row in cursor]
    cursor.close()
    
    return render_template('view_fantasy_team.html', team_rows=team_rows)
    
    
@app.route('/goto_create_fantasy_team', methods=['POST'])
def goto_create_fantasy_team():
    return render_template('create_fantasy_team.html')   
    
@app.route('/create_fantasy_team', methods=['POST'])
def create_fantasy_team():
    team_name = request.form['team_name']
    password = request.form['password']
    
    params = {'team_name': team_name, 'password': password}
    
    # Check team_name does not already exist
    check_team_command = (text('SELECT * FROM fantasy_team'))
    cursor = g.conn.execute(check_team_command)
    existing_team_names = [row[0] for row in cursor]
    cursor.close()
    
    if not existing_team_names and team_name in existing_team_name:
        return render_template('team_name_already_exists.html')
    
    # Insert new row into fantasy_teams table
    insert_command = (text('INSERT INTO fantasy_team(name, password) VALUES(:team_name, :password);'))
    g.conn.execute(insert_command, params)
    g.conn.commit()
    
    # Check if team has been successfully created
    check_team_command = (text('SELECT :team_name FROM fantasy_team'))
    cursor = g.conn.execute(check_team_command, params)
    existing_team_names = [row[0] for row in cursor]
    cursor.close()
    
    if not existing_team_names and team_name not in existing_team_name:
        return render_template('error_creating_team.html')

    return render_template('team_successfully_created.html')       
    

if __name__ == "__main__":
	import click

	@click.command()
	@click.option('--debug', is_flag=True)
	@click.option('--threaded', is_flag=True)
	@click.argument('HOST', default='0.0.0.0')
	@click.argument('PORT', default=8111, type=int)
	def run(debug, threaded, host, port):
		"""
		This function handles command line parameters.
		Run the server using:

			python server.py

		Show the help text using:

			python server.py --help

		"""

		HOST, PORT = host, port
		print("running on %s:%d" % (HOST, PORT))
		app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)

run()
