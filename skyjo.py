from random import random

from constant import CARDS
import random
import pprint

#count de la pioche
#quand la pioche est vide
#quand on pass la carte, en retourner une
# les rangé

class Game:
    def __init__(self, players_number):
        self.cards=[]

        self.players_number = players_number
        if players_number > 4:
            self.players_number = 4

        self.little_card_class = ""
        if self.players_number >= 3:
            self.little_card_class = "littleCard"

        self.players_points = []
        self.players_cards = []
        self.game_discard = []
        self.distribute_cards()
        self.showed_card = None
        self.last_showed_card = None
        self.staging_card = None
        self.play_turn = 0
        self.play_turn_number = 0
        self.has_the_player_passed_staging_card = False

    def shuffle_card(self):

        print('shuffle')
        self.cards = CARDS.copy()
        random.shuffle(self.cards)

    def get_showed_card(self):
        print('get showed card')
        print(self.showed_card)
        return self.showed_card

    def get_staging_card(self):
        print('get staging card')
        print(self.staging_card)
        return self.staging_card

    def get_current_player(self):
        print('get current player')
        print(self.players_number)
        return self.players_number
    def get_has_the_player_passed_staging_card(self):

        return self.has_the_player_passed_staging_card

    def get_html_for_card(self, number, showed, touchable, player_number, card_id, addedClasses):
        option = ""
        if not showed:
            option = "<div class='behindCard'><span>SKYJO</span></div>"

        color = ""
        if number < 0:
            color = "darkBlue"
        if number == 0:
            color = "blue"
        if number >= 1:
            color = "green"
        if number >= 5:
            color = "yellow"
        if number >= 9:
            color = "red"

        html = f"<div class=' card {addedClasses} {"untouchable" if player_number != self.play_turn or not touchable else ""} {"" if addedClasses =="discardedCard" or addedClasses== "stagingCard"  else self.little_card_class} {color} ' id='{card_id}'> \
                                    <span class='topNumber'>{number}</span> \
                                    <span class='number'>{number}</span> \
                                    <span class='bottomNumber'>{number}</span> \
                                    {option}\
                                 </div>"

        return html

    def start(self):

        print('start')
        # shuffle cards
        self.shuffle_card()

        # reset turn
        self.play_turn = 0
        self.play_turn_number = 0
        self.players_points = []
        self.players_cards = []
        self.game_discard = []
        self.showed_card = None
        self.staging_card = None

        # distribute
        self.players_cards = []
        self.distribute_cards()

        # return first card
        self.showed_card = (self.cards[0], True)
        del self.cards[0]

    def distribute_cards(self):

        print('distribute')
        for player in range(self.players_number):
            # get 12 cards
            cards_of_one_player = [(card, False) for card in self.cards[0:12]]
            del self.cards[0:12]

            cards_of_one_player = [cards_of_one_player[i:i + 3] for i in range(0, len(cards_of_one_player), 3)]

            self.players_cards.append(cards_of_one_player)

        # add card to showed_card

        return

    def has_finish(self, cards_columns):

        print('has_finished')
        for column in cards_columns:
            for card in column:
                if card[1] == False:
                    return False
        return True

    def someone_has_finished(self):

        print('someone_has_finished')
        for player_card_columns in self.players_cards:
            if self.has_finish(player_card_columns):
                return True
        return False

    def count_showed_card(self, player):

        player_cards = self.players_cards[player]
        cards_showed = 0
        for column in player_cards:
            for card in column:
                if card[1] is True:
                    cards_showed += 1

        print('count_showed_card : ', cards_showed)
        return cards_showed
    def count_showed_card_value(self, player):

        player_cards = self.players_cards[player]
        count = 0
        for column in player_cards:
            for card in column:
                if card[1] is True:
                    count += card[0]

        return count



    def discard(self):
        print('discard for staging card')
        self.staging_card = (self.cards[0], True)
        print(self.staging_card)
        del self.cards[0]
        return

    def replace_showed_card_staging_card(self):
        self.staging_card = self.showed_card
        self.last_showed_card = self.showed_card
        if len( self.game_discard) >= 1  :
            self.showed_card = (self.game_discard[-1],True)
            del self.game_discard[-1]
        else :
            self.showed_card = None
        return
    def replace_staging_card_showed_card(self):
        if self.showed_card :
            self.game_discard.append(self.showed_card[0])
        if self.showed_card != self.last_showed_card :
            self.has_the_player_passed_staging_card = True
        self.showed_card = self.staging_card
        self.staging_card = None
        return
    def exchange(self, card_number_index, player):
        colonne_index = (card_number_index - 1) // 3  # Colonne (de 0 à 3 pour 4 colonnes)
        card_index = (card_number_index - 1) % 3
        print(card_number_index,player)
        print('before : ')
        print(self.players_cards[player][colonne_index][card_index])
        print(self.staging_card)
        print(self.showed_card)
        card = self.players_cards[player][colonne_index][card_index]

        if self.showed_card :
            self.game_discard.append(self.showed_card[0])
        self.showed_card = (card[0],True)
        self.players_cards[player][colonne_index][card_index] = self.staging_card
        self.staging_card = None
        print('after : ')
        print(self.players_cards[player][colonne_index][card_index])
        print(self.staging_card)
        print(self.showed_card)
        self.change_player()
        return True

    def change_player(self):
        self.play_turn += 1
        if self.play_turn == self.players_number:
            self.play_turn = 0
            self.play_turn_number += 1

    def discard_own_card(self, index, player):

        print('discard own car :', player, " player turn :", self.play_turn)
        if player != self.play_turn:
            return False, "Not your turn"
        colonne_index = (index - 1) // 3  # Colonne (de 0 à 3 pour 4 colonnes)
        card_index = (index - 1) % 3
        card = self.players_cards[player][colonne_index][card_index]
        self.players_cards[player][colonne_index][card_index] = (card[0], True)

        if self.count_showed_card(player) == 2 and self.play_turn_number == 0:
            self.change_player()
        if self.has_the_player_passed_staging_card :
            self.has_the_player_passed_staging_card = False
            self.change_player()
        print('END : discard own car :', player, " player turn :", self.play_turn)
        return True, ""

    def run(self):
        print('run', self.play_turn, self.play_turn_number)
        # first initialisation
        if len(self.players_cards) == 0:
            self.start()

        if self.someone_has_finished():
            self.start()

        return False, self.players_cards, len(self.cards), self.play_turn, self.play_turn_number
