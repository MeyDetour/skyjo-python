from itertools import count
from operator import contains
from random import random

from constant import CARDS, player_number
import random
import pprint


# parite a 100points

class Game:
    def __init__(self, players_number):
        self.cards = []
        self.points = []
        self.points_sum = []
        self.end_of_game = False
        self.end_of_axe = False
        self.players_number = players_number
        if players_number > 4:
            self.players_number = 4
        if players_number <= 1:
            self.players_number = 2

        self.little_card_class = ""
        if self.players_number >= 3:
            self.little_card_class = "littleCard"



        # (player_id,turn won)
        self.winner_player = None
        self.players_cards = []
        self.game_discard = []
        self.distribute_cards()
        self.showed_card = None
        self.last_showed_card = None
        self.staging_card = None
        self.play_turn = 0
        self.play_turn_number = -1
        self.has_the_player_passed_staging_card = False

    def get_showed_card(self):
        print(self.showed_card)
        return self.showed_card

    def get_staging_card(self):
        print(self.staging_card)
        return self.staging_card

    def get_current_player(self):
        print(self.players_number)
        return self.players_number

    def get_has_the_player_passed_staging_card(self):

        return self.has_the_player_passed_staging_card

    def get_html_for_card(self, number, showed, touchable, player_number, card_id, addedClasses):
        option = ""
        if not showed:
            option = "<div class='behindCard'><div class='span1'><span>o</span><span>SKYJO</span></div><div class='span2'><span>o</span><span>SKYJO</span></div></div>"

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
        if self.little_card_class != "":
            if number < 0:
                second_color = " littleDarkBlue"
            if number == 0:
                second_color = " littleBlue"
            if number >= 1:
                second_color = " littleGreen"
            if number >= 5:
                second_color = " littleYellow"
            if number >= 9:
                second_color = " littleRed"

            color += second_color

        html = f"<div class=' card {addedClasses} {"behindCardBorder" if not showed else ""} {"untouchable" if player_number != self.play_turn or not touchable else ""} {"" if addedClasses == "discardedCard" or addedClasses == "stagingCard" else self.little_card_class} {color} ' id='{card_id}'> \
                                    <span class='number'>{number}</span> \
                                    {option}\
                                 </div>"

        return html


    def restart_points(self):
        self.points = []
        self.points_sum = []
        self.end_of_game = False
    def restart(self):

        # shuffle cards
        self.cards = CARDS.copy()
        random.shuffle(self.cards)

        # reset turn
        self.play_turn = 0
        self.play_turn_number = 0

        #reset cards
        self.players_cards = []
        self.game_discard = []
        self.showed_card = None
        self.staging_card = None
        self.last_showed_card = self.showed_card
        self.has_the_player_passed_staging_card = False

        self.winner_player = None
        self.end_of_axe = False
        self.end_of_game = False

        # distribute
        self.players_cards = []
        self.distribute_cards()

        # return first card
        self.showed_card = (self.cards[0], True)
        del self.cards[0]

    def distribute_cards(self):
        self.end_of_axe = False
        for player in range(0, self.players_number):
            # get 12 cards
            cards_of_one_player = [(card, False) for card in self.cards[0:12]]
            del self.cards[0:12]

            cards_of_one_player = [cards_of_one_player[i:i + 3] for i in range(0, len(cards_of_one_player), 3)]

            self.players_cards.append(cards_of_one_player)

        # add card to showed_card

        return

    def has_finish(self, cards_columns):

        for column in cards_columns:
            for card in column:
                if card[1] == False:
                    return False
        return True

    def someone_has_finished(self):
        print('someone_has_finished')
        pprint.pprint(self.players_cards)
        for player_card_columns in self.players_cards:
            if self.has_finish(player_card_columns):
                if not self.winner_player:
                    self.winner_player = (self.players_cards.index(player_card_columns), self.play_turn_number - 1)
                    print("winner player:", self.winner_player)
                return True

        pprint.pprint(self.players_cards)

        print('END :someone_has_finished')
        return False

    def count_showed_card(self, player):

        player_cards = self.players_cards[player]
        cards_showed = 0
        for column in player_cards:
            for card in column:
                if card[1] is True:
                    cards_showed += 1

        return cards_showed

    def update_score(self):
        points_player_winner = self.count_showed_card_value(self.winner_player[0])

        print(f"\n--- Mise à jour du score ---")
        print(f"Points du gagnant actuel : {points_player_winner}")

        #get points of this axex
        points_value = []
        for player in range(0, player_number):
            points = self.count_showed_card_value(player)
            points_value.append(points)
            print(f"Points du joueur {player} : {points}")

        #double points if someone has less
        max_points = min(points_value)
        print(f"Max des points : {max_points}")
        if points_player_winner > max_points:
            print(f"Doublage des points pour le joueur gagnant (Joueur {self.winner_player[0]})")
            points_value[self.winner_player[0]] *= 2

        print(f"Points après éventuel doublage : {points_value}")

        # if first turn ? create list : append to existing list
        if len(self.points) != self.players_number:
            for point in points_value:
                self.points.append([point])
            print(f"Premier tour - Points initiaux : {self.points}")
        else:
            for idx, player_points in enumerate(points_value):  # Correction de la boucle pour enumerate
                self.points[idx].append(player_points)
            print(f"Points actuels après ajout : {self.points}")

        # Calcul des totaux pour chaque joueur
        self.points_sum = []
        print("\n--- Calcul des totaux ---")
        for idx, player_points in enumerate(self.points):
            total = sum(player_points)
            self.points_sum.append(total)
            print(f"Total du joueur {idx} : {total}")
            if total >= 100:
                print(f"Le joueur {idx} atteint ou dépasse 100 points. Fin de partie.")
                self.end_of_game = True


        self.end_of_axe = True
        print("\n--- Fin de la mise à jour du score ---\n")
        return

    def count_showed_card_value(self, player):
        player_cards = self.players_cards[player]
        count = 0
        border = "=" * 40

        # Impression du titre
        print(f"\n{border}\n|    Comptage des cartes visibles   |\n{border}")
        print(f"Cartes du joueur {player} :")

        for column_index, column in enumerate(player_cards):
            print(f"\n--- Colonne {column_index + 1} ---")  # Numérotation des colonnes pour clarté

            for card_index, card in enumerate(column):
                # Vérifier que la carte est un tuple avec au moins deux éléments
                print("card etudié :", card)
                if isinstance(card, tuple) and len(card) == 2:
                    if card[1]:  # Vérifie si la carte est visible (True)
                        count += card[0]
                        print(f"✔️  Carte visible à l'index {card_index}: {card} -> Ajoutée, Valeur actuelle: {count}")
                    else:
                        print(f"❌  Carte cachée à l'index {card_index}: {card} -> Ignorée")
                else:
                    print(f"⚠️  Carte invalide à l'index {card_index} : {card}")

        # Impression du total
        print(f"\n{border}\n|  Valeur totale des cartes visibles du joueur {player} : {count}  |\n{border}\n")
        return count

    def update_columns(self, player):
        columns_results = []

        for idx, column in enumerate(self.players_cards[player]):
            card_reference = column[0][0]
            result = True

            for card in column:
                if card[0] != card_reference or card[1] is False:
                    result = False

            columns_results.append(result)
        try:
            column = columns_results.index(True)

            # Ajout des cartes montrées et défaussées
            if self.showed_card:
                self.game_discard.append(self.showed_card[0])

            self.game_discard.append(self.players_cards[player][column][0][0])
            self.game_discard.append(self.players_cards[player][column][1][0])

            # Mise à jour de la carte montrée
            self.showed_card = self.players_cards[player][column][2]
            self.last_showed_card = self.showed_card

            # Suppression de la colonne
            del self.players_cards[player][column]

        except ValueError:
            return

    # def update_columns(self, player):
    #     columns_results = []
    #     for column in self.players_cards[player]:
    #         print(column)
    #         card_reference = column[0][0]
    #         result = True
    #         for card in column:
    #             if card[0] != card_reference or card[1] is False:
    #                 result = False
    #         columns_results.append(result)
    #     try:
    #         column = columns_results.index(True)
    #         if self.showed_card:
    #             self.game_discard.append(self.showed_card[0])
    #         self.game_discard.append(self.players_cards[player][column][0][0])
    #         self.game_discard.append(self.players_cards[player][column][1][0])
    #         self.showed_card = self.players_cards[player][column][2]
    #         self.last_showed_card = self.showed_card
    #         del self.players_cards[player][column]
    #     except ValueError:
    #         return

    def discard(self):
        print('discard for staging card')
        self.staging_card = (self.cards[0], True)
        self.last_showed_card = None
        print(self.staging_card)
        del self.cards[0]
        return

    def replace_showed_card_staging_card(self):
        self.staging_card = self.showed_card
        self.last_showed_card = self.showed_card
        self.has_the_player_passed_staging_card = False
        if len(self.game_discard) >= 1:
            self.showed_card = (self.game_discard[-1], True)
            del self.game_discard[-1]
        else:
            self.showed_card = None
        return

    def replace_staging_card_showed_card(self):
        if self.showed_card:
            self.game_discard.append(self.showed_card[0])
        if self.staging_card == self.last_showed_card:
            self.has_the_player_passed_staging_card = False
        else:
            self.has_the_player_passed_staging_card = True
        self.showed_card = self.staging_card
        self.staging_card = None
        return

    def exchange(self, card_number_index, player):
        colonne_index = (card_number_index - 1) // 3  # Colonne (de 0 à 3 pour 4 colonnes)
        card_index = (card_number_index - 1) % 3

        # Debug avant modification
        print(f"Avant échange : colonne {colonne_index}, index carte {card_index}")
        print(f"Carte sélectionnée : {self.players_cards[player][colonne_index][card_index]}")
        print(f"Staging card : {self.staging_card}")
        print(f"Showed card avant : {self.showed_card}")
        print(f"Player cards avant : {self.players_cards[player]}")

        card = self.players_cards[player][colonne_index][card_index]

        if self.showed_card:
            print(f"  Ajout de la carte montrée {self.showed_card[0]} dans la pile de défausse")
            self.game_discard.append(self.showed_card[0])

        self.showed_card = (card[0], True)
        self.last_showed_card = self.showed_card
        print(f"  Nouvelle carte montrée : {self.showed_card}")

        self.players_cards[player][colonne_index][card_index] = self.staging_card
        self.staging_card = None
        print(
            f"  Nouvelle carte dans la colonne {colonne_index}, index {card_index} : {self.players_cards[player][colonne_index][card_index]}")

        self.change_player()
        self.update_columns(player)

        # Debug après modification
        print(f"Après échange : colonne {colonne_index}, index carte {card_index}")
        if colonne_index < len(self.players_cards[player]):

            print(f"Carte modifiée : {self.players_cards[player][colonne_index][card_index]}")
        else:
            print(f"Carte modifiée a été enlevé avec la colonne")

        print(f"Showed card après : {self.showed_card}")
        print(f"Player cards après : {self.players_cards[player]}")

        return True

    def change_player(self):
        self.play_turn += 1
        if self.play_turn == self.players_number:
            self.play_turn = 0
            self.play_turn_number += 1

    def discard_own_card(self, index, player):

        if player != self.play_turn:
            return False, "Not your turn"
        colonne_index = (index - 1) // 3  # Colonne (de 0 à 3 pour 4 colonnes)
        card_index = (index - 1) % 3
        card = self.players_cards[player][colonne_index][card_index]
        self.players_cards[player][colonne_index][card_index] = (card[0], True)

        if self.count_showed_card(player) == 2 and self.play_turn_number == 0:
            self.change_player()
        if self.has_the_player_passed_staging_card:
            self.has_the_player_passed_staging_card = False
            self.change_player()

        self.update_columns(player)
        return True, ""

    def run(self):
        print('run', self.play_turn, self.play_turn_number)
        # first initialisation
        if len(self.players_cards) == 0:
            self.start()

        # reload discard
        if len(self.cards) == 0:
            self.cards = self.game_discard
            self.game_discard = []
            random.shuffle(self.cards)

        # to select the starter player with the max count card
        if self.play_turn_number == 1 and self.play_turn == 0:
            points = []

            for player in range(player_number):
                points.append(self.count_showed_card_value(player))

            print(points)
            self.play_turn = points.index(max(points))

        pprint.pprint(self.players_cards)
        # to finish game
        if self.someone_has_finished():
            print('someone has finished')
            # last turn it will be detected and his turn his change with his action
            print(self.play_turn, self.winner_player)
            pprint.pprint(self.players_cards)
            print("player turn :", self.play_turn)
            print('is it the end ?:',self.play_turn == self.winner_player[0] and self.play_turn_number != self.winner_player[1])
            if self.play_turn == self.winner_player[0] and self.play_turn_number != self.winner_player[1]:
                self.play_turn = -1

                for player in range(len(self.players_cards)):
                    for column in range(len(self.players_cards[player])):
                        for card in range(len(self.players_cards[player][column])):
                            self.players_cards[player][column][card] = (
                                self.players_cards[player][column][card][0], True)
                    self.update_columns(player)

                self.update_score()
                return True, self.players_cards,  self.play_turn, self.play_turn_number, self.points,self.end_of_game,self.end_of_axe,self.points_sum


        pprint.pprint(self.players_cards)
        return False, self.players_cards, self.play_turn, self.play_turn_number, self.points,self.end_of_game,self.end_of_axe,self.points_sum
