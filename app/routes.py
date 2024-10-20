from crypt import methods
from pprint import pprint

from flask import Flask, render_template, request, jsonify, redirect
from app import app
from constant import player_number
from skyjo import Game
import constant
import pprint

# 8 gamer max

game = Game(constant.player_number)
game.restart_points()

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/restart", methods=['GET'])
def restart():
    game.restart()
    return jsonify({
        'message': "ok"
    })

@app.route("/newGame", methods=['GET'])
def new_game():
    game.restart_points()
    game.restart()
    return jsonify({
        'message': "ok"
    })


@app.route("/update_board", methods=['POST'])
def update_board():
    done, players_cards, discard_cards_left, turn, turn_number, points ,end_of_game,end_of_axe= game.run()
    showed_card = game.get_showed_card()
    staging_card = game.get_staging_card()
    has_the_player_passed_staging_card = game.get_has_the_player_passed_staging_card()
    display_no_card = False
    if not showed_card:
        display_no_card = True
    if showed_card:
        showed_card = game.get_html_for_card(showed_card[0], showed_card[1], turn_number > 0 and not staging_card, turn,
                                             -2, 'discardedCard')
    if staging_card:
        staging_card = game.get_html_for_card(staging_card[0], staging_card[1], True, turn, -1, 'stagingCard')
    plateau_cards = ""

    for idx, player_card_columns in enumerate(players_cards):
        column_number = 1
        # start player card
        player_cards = f"<div class='cardDeck  ' id='player{idx}' data-id='{idx}' >"

        player_cards += f"<span class='count'>{game.count_showed_card_value(idx)} points</span>"
        if idx == turn:
            player_cards += f"<span class='turn'>Your turn</span>"

        card_number = 1
        for column in player_card_columns:

            # start column
            cards_column = "<div class='columnCard'>"
            for card in column:
                cards_column += game.get_html_for_card(card[0], card[1], (
                            idx == turn and not staging_card and turn_number == 0) or staging_card or has_the_player_passed_staging_card,
                                                       idx, (column_number * card_number), '')
                card_number += 1
            # close the column
            cards_column += "</div>"

            # add column to card plateau
            player_cards += cards_column

        # end player card
        player_cards += "</div>"
        # senf player card to plateau
        plateau_cards += player_cards
        column_number += 1

    return jsonify({
        'done': done,
        'cards': plateau_cards,
        'player_number': constant.player_number,
        'discard_cards_left': discard_cards_left,
        'showed_card': showed_card,
        'staging_card': staging_card,
        'current_turn': turn,
        'no_card': display_no_card,
        'turn_number': turn_number,
        "axes": {
            "points": points,
            "end_of_game": end_of_game,
            "end_of_axe": end_of_axe,
        },
        'has_the_player_passed_staging_card': has_the_player_passed_staging_card,
    })


@app.route('/return/card', methods=['POST'])
def return_card():
    data = request.get_json()
    card_number = int(data.get('card_number'))
    player_number = int(data.get('player_number'))

    state, message = game.discard_own_card(card_number, player_number)

    if not state:
        return jsonify({
            'error': message
        })

    return jsonify({
        'message': "ok"
    })


@app.route('/exchange', methods=['POST'])
def exchange():
    data = request.get_json()
    card_number = int(data.get('card_to_change'))
    player = int(data.get('player_index'))
    game.exchange(card_number, player)

    return jsonify({
        'message': "ok"
    })


@app.route('/discard', methods=['POST'])
def discard():
    game.discard()

    return jsonify({
        'message': "ok"
    })


@app.route('/get/showed/card', methods=['GET'])
def get_showed_card():
    game.replace_showed_card_staging_card()

    return (jsonify({
        'message': "ok"
    }))


@app.route('/pass/staging/card', methods=['GET'])
def replace_staging_card_to_showed_card():
    game.replace_staging_card_showed_card()

    return jsonify({
        'message': "ok"
    })


@app.route('/play_turn', methods=['POST'])
def play_turn():
    # Logique pour faire jouer un tour
    done, players_cards, remaining_cards, current_turn, turn_number = game.run()

    return jsonify({
        'done': done,
        'players_cards': players_cards,
        'remaining_cards': remaining_cards,
        'current_turn': current_turn,
        'turn_number': turn_number
    })
