from flask import Flask, render_template, request, redirect, session
import random
app = Flask(__name__)
app.secret_key = 'keep it secret, keep it safe'

@app.route('/')
def start_game():
    session['target_num'] = random.randint(1, 100)
    print(session['target_num'])
    # Reset attempts from prior games
    session['attempts'] = 0
    return render_template('index.html', target_num=session['target_num'])

@app.route('/guessnumber', methods=['POST'])
def guess_number():
    # Record user's guess
    session['guess'] = request.form['guess']
    # Increment attempts
    session['attempts'] += 1
    return redirect('/game')

@app.route('/game')
def display_result():
    result = ''
    session['game_over'] = False
    # # Game over if game not won within 5 attempts. Otherwise, proceed with game.
    # if 'attempts' in session and session['attempts'] > 5:
    #     session['game_over'] = True
        # Calculate result
    if int(session['guess']) > session['target_num']:
        result = 'Too high!'
    elif int(session['guess']) < session['target_num']:
        result = 'Too low!'
    else:
        result = (f'{session['target_num']} was the number!')
    # Game over if user guesses wrong on the 5th attempt
    if session['attempts'] == 5 and (result == 'Too high!' or result == 'Too low!'):
            session['game_over'] = True
    print(session['attempts'])
    return render_template('game.html', result=result, attempts=session['attempts'], game_over=session['game_over'])

@app.route('/leaderboard', methods=['POST'])
def add_to_leaderboard():
    session['winner_name'] = request.form['winner_name']
    if 'winner_list' not in session:
        session['winner_list'] = []
    else:
        session['winner_list'].append({'name': session['winner_name'], 'num_attempts': session['attempts']})
    print(session['winner_list'])
    return render_template('leaderboard.html', winner_list=session['winner_list'])


if __name__ == '__main__':
    app.run(debug=True)