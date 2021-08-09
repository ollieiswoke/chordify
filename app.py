import main
from flask import Flask, render_template, request, url_for, redirect, send_from_directory
app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def bio_data_form():
    if request.method == "POST": #if submit button is pressed, pass song_file_name to next function, and run show_bio (which is the statistics page)

        song_file_name = request.form['song_file_name']

        return redirect(url_for('showbio',
                                ))
    return render_template("home.html")


@app.route('/showbio', methods=['GET'])
def showbio():          #show statistics
    song_file_name = request.args.get('song_file_name')
    #statistics_report = request.args.get('statistics_report')
    #statistics_report = None           <<use this code if you want to demo the statistics page without the loading time
    statistics_report = main.chordbot(song_file_name,"real")

    download_link = "/output/{}_inspired_piece.mid".format(song_file_name)
    original_piece_path = '/midi/{}.mid'.format(song_file_name)
    return render_template("statistics.html",
                           download_link=download_link,
                           statistics_report=statistics_report,
                           original_piece_path=original_piece_path
                           )

##downloading things
@app.route('/output/<path:path>') ##if this url is reached (by user clicking "here"), download to computer
def send_js(path):
    return send_from_directory('output', path) #<<this is the folder where the file is stored <<<so right now output/....mid
@app.route('/midi/<path:path>')
def send_js_midi(path):
    return send_from_directory('midi', path) #<<midi folder <<<so right now midi/....mid


@app.route('/help', methods=['GET']) #when user reaches "help" url from navigation bar
def showhelp():
    return render_template("help.html")
if __name__ == "__main__":
    app.run(debug=True, port=8080)
