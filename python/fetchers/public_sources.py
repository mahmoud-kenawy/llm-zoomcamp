from typing import List, Dict, Any

CHESS_OPENINGS = [
    {"name": "Italian Game", "moves": "1.e4 e5 2.Nf3 Nc6 3.Bc4", "eco": "C50-C54",
     "description": "Classical opening developing the bishop to its most active square, aiming at f7. Leads to open, tactical play with quick development and central control."},
    {"name": "Ruy Lopez", "moves": "1.e4 e5 2.Nf3 Nc6 3.Bb5", "eco": "C60-C99",
     "description": "The Spanish Game. White pressures the knight defending e5, building long-term central pressure. One of the oldest and most respected openings."},
    {"name": "Sicilian Defense", "moves": "1.e4 c5", "eco": "B20-B99",
     "description": "Black's most popular response to 1.e4. Creates an unbalanced position with chances for both sides. Major variations: Najdorf, Dragon, Classical, Sveshnikov."},
    {"name": "Sicilian Najdorf", "moves": "1.e4 c5 2.Nf3 d6 3.d4 cxd4 4.Nxd4 Nf6 5.Nc3 a6", "eco": "B90-B99",
     "description": "The most popular Sicilian variation at top level. Flexible and complex, favored by Fischer and Kasparov."},
    {"name": "Sicilian Dragon", "moves": "1.e4 c5 2.Nf3 d6 3.d4 cxd4 4.Nxd4 Nf6 5.Nc3 g6", "eco": "B70-B79",
     "description": "Sharp counterattacking variation with kingside fianchetto. The Yugoslav Attack (Be3, f3, Qd2) leads to opposite-side castling races."},
    {"name": "French Defense", "moves": "1.e4 e6", "eco": "C00-C19",
     "description": "Solid but slightly passive. Black builds a strong pawn chain (d5-e6) and counterattacks with ...c5. Main lines: Winawer, Classical, Tarrasch, Advance."},
    {"name": "Caro-Kann", "moves": "1.e4 c6", "eco": "B10-B19",
     "description": "Solid defense preparing ...d5. More solid than the French with better bishop development. Favored by Karpov and Carlsen."},
    {"name": "Queen's Gambit", "moves": "1.d4 d5 2.c4", "eco": "D06-D69",
     "description": "White offers a pawn for central control. Black can accept (QGA), decline (QGD), or play the Slav. Fundamental 1.d4 opening."},
    {"name": "Queen's Gambit Declined", "moves": "1.d4 d5 2.c4 e6", "eco": "D30-D69",
     "description": "Classical solid response. Black keeps the center closed and develops solidly. Rich strategic play around the c-file and minority attack."},
    {"name": "Slav Defense", "moves": "1.d4 d5 2.c4 c6", "eco": "D10-D19",
     "description": "Solid defense keeping the light-squared bishop open. Extremely popular at all levels for its reliability."},
    {"name": "King's Indian Defense", "moves": "1.d4 Nf6 2.c4 g6 3.Nc3 Bg7", "eco": "E60-E99",
     "description": "Hypermodern defense allowing White the center, then counterattacking with ...e5 or ...c5. Sharp and double-edged, favored by Fischer and Kasparov."},
    {"name": "Nimzo-Indian Defense", "moves": "1.d4 Nf6 2.c4 e6 3.Nc3 Bb4", "eco": "E20-E59",
     "description": "Black pins the knight, aiming to double White's pawns or control e4. Highly flexible and popular at top level."},
    {"name": "Queen's Indian Defense", "moves": "1.d4 Nf6 2.c4 e6 3.Nf3 b6", "eco": "E12-E19",
     "description": "Solid defense fianchettoing the queenside bishop. Less sharp than the Nimzo, focusing on control of e4."},
    {"name": "Grunfeld Defense", "moves": "1.d4 Nf6 2.c4 g6 3.Nc3 d5", "eco": "D80-D99",
     "description": "Hypermodern defense challenging White's center immediately. Leads to dynamic, concrete play."},
    {"name": "English Opening", "moves": "1.c4", "eco": "A10-A39",
     "description": "Flank opening controlling d5. Flexible transpositional possibilities. Favored by Carlsen and Kramnik."},
    {"name": "Reti Opening", "moves": "1.Nf3 d5 2.c4", "eco": "A04-A09",
     "description": "Hypermodern flank opening. White fianchettoes and attacks the center from the wings."},
    {"name": "London System", "moves": "1.d4 d5 2.Bf4", "eco": "D02, A46",
     "description": "Solid system with early bishop development. Very popular at club level for its simplicity and reliability."},
    {"name": "Scotch Game", "moves": "1.e4 e5 2.Nf3 Nc6 3.d4", "eco": "C44-C45",
     "description": "White opens the center immediately. Leads to open tactical play. Popularized by Kasparov and hơn."},
    {"name": "Petrov's Defense", "moves": "1.e4 e5 2.Nf3 Nf6", "eco": "C42-C43",
     "description": "Symmetrical solid defense. Black mirrors White's knight development. Very drawish but solid."},
    {"name": "Scandinavian Defense", "moves": "1.e4 d5", "eco": "B01",
     "description": "Black strikes the center immediately with the queen pawn. Leads to imbalanced play with queen development."},
    {"name": "Alekhine's Defense", "moves": "1.e4 Nf6", "eco": "B02-B05",
     "description": "Provocative defense inviting White's pawns forward to attack them later. Hypermodern concept."},
    {"name": "Pirc Defense", "moves": "1.e4 d6 2.d4 Nf6 3.Nc3 g6", "eco": "B07-B09",
     "description": "Flexible hypermodern defense allowing White the center initially."},
    {"name": "Modern Defense", "moves": "1.e4 g6", "eco": "B06",
     "description": "Hypermodern fianchetto defense. Flexible and transpositional."},
    {"name": "Dutch Defense", "moves": "1.d4 f5", "eco": "A80-A99",
     "description": "Aggressive flank defense fighting for e4. Main lines: Leningrad, Classical, Stonewall."},
    {"name": "Benoni Defense", "moves": "1.d4 Nf6 2.c4 c5 3.d5 e6", "eco": "A56-A79",
     "description": "Sharp counterattacking defense. Black accepts a queenside majority vs White's central majority."},
    {"name": "Catalan Opening", "moves": "1.d4 Nf6 2.c4 e6 3.g3", "eco": "E01-E09",
     "description": "Positional opening combining Queen's Gambit with kingside fianchetto. Long-term pressure on the queenside."},
    {"name": "Evans Gambit", "moves": "1.e4 e5 2.Nf3 Nc6 3.Bc4 Bc5 4.b4", "eco": "C51-C52",
     "description": "Romantic gambit sacrificing a pawn for rapid development and central control."},
    {"name": "King's Gambit", "moves": "1.e4 e5 2.f4", "eco": "C30-C39",
     "description": "Classic romantic gambit. White sacrifices the f-pawn for rapid development and attack. Rarely seen at top level today."},
    {"name": "Vienna Game", "moves": "1.e4 e5 2.Nc3", "eco": "C25-C29",
     "description": "Flexible developing move avoiding early theory. Can transpose to King's Gambit or lead to independent play."},
    {"name": "Four Knights Game", "moves": "1.e4 e5 2.Nf3 Nc6 3.Nc3 Nf6", "eco": "C48-C49",
     "description": "Classical symmetrical development. Solid and traditional, popular at club level."},
    {"name": "Philidor Defense", "moves": "1.e4 e5 2.Nf3 d6", "eco": "C41",
     "description": "Solid but passive defense. Black defends e5 directly but blocks the bishop."},
    {"name": "Ponziani Opening", "moves": "1.e4 e5 2.Nf3 Nc6 3.c3", "eco": "C44",
     "description": "Old opening preparing d4. Rare at top level but tricky."},
    {"name": "Bird's Opening", "moves": "1.f4", "eco": "A02-A03",
     "description": "Flank opening similar to Dutch with colors reversed. Uncommon but playable."},
    {"name": "Sokolsky Opening", "moves": "1.b4", "eco": "A00",
     "description": "The Orangutan. Rare flank opening attacking from the queenside."},
]

CHESS_CONCEPTS = [
    {"name": "Fork", "category": "tactics",
     "description": "A tactic where one piece attacks two or more enemy pieces simultaneously. Knights are especially good at forking due to their unusual movement."},
    {"name": "Pin", "category": "tactics",
     "description": "A tactic where a piece cannot move without exposing a more valuable piece behind it. Absolute pins (king behind) are strongest."},
    {"name": "Skewer", "category": "tactics",
     "description": "The reverse of a pin: a valuable piece is attacked and must move, exposing a less valuable piece behind it."},
    {"name": "Discovered Attack", "category": "tactics",
     "description": "Moving one piece reveals an attack by another piece. Discovered check is especially powerful as the opponent must address the check."},
    {"name": "Double Check", "category": "tactics",
     "description": "Two pieces give check simultaneously. The king must move as neither check can be blocked or captured in one move."},
    {"name": "Zwischenzug", "category": "tactics",
     "description": "An in-between move that changes the outcome of a sequence. Often a check or threat played before the 'expected' recapture."},
    {"name": "Deflection", "category": "tactics",
     "description": "Forcing an enemy piece away from an important square or duty by sacrifice or threat."},
    {"name": "Decoy", "category": "tactics",
     "description": "Luring an enemy piece to a bad square, often by sacrifice."},
    {"name": "X-ray", "category": "tactics",
     "description": "A piece attacks through an enemy piece to a square beyond, or defends through its own piece."},
    {"name": "Windmill", "category": "tactics",
     "description": "A series of alternating checks and captures, typically with rook and bishop working together."},
    {"name": "Outpost", "category": "strategy",
     "description": "A square in enemy territory that cannot be attacked by enemy pawns, ideal for a knight. Supported by own pawns."},
    {"name": "Weak Squares", "category": "strategy",
     "description": "Squares that cannot be defended by pawns. Controlling weak squares near the enemy king is a key attacking plan."},
    {"name": "Pawn Structure", "category": "strategy",
     "description": "The arrangement of pawns determines long-term plans. Isolated, doubled, backward, and passed pawns each have strategic implications."},
    {"name": "Minority Attack", "category": "strategy",
     "description": "Advancing fewer pawns against more to create weaknesses. Classic plan in Queen's Gambit structures."},
    {"name": "Open File", "category": "strategy",
     "description": "A file with no pawns. Rooks belong on open files. Controlling the only open file is a major advantage."},
    {"name": "Bishop Pair", "category": "strategy",
     "description": "Having both bishops is a long-term advantage in open positions, worth roughly half a pawn."},
    {"name": "Bad Bishop", "category": "strategy",
     "description": "A bishop blocked by its own pawns on the same color. A key concept in French Defense structures."},
    {"name": "Prophylaxis", "category": "strategy",
     "description": "Preventive moves that stop the opponent's plans before they start. Associated with Petrosian and Karpov."},
    {"name": "Opposition", "category": "endgame",
     "description": "Kings facing each other with one square between. The player NOT to move has the opposition, a key drawing/winning technique in pawn endgames."},
    {"name": "Triangulation", "category": "endgame",
     "description": "King maneuver losing a tempo to put the opponent in zugzwang. Essential technique in king and pawn endgames."},
    {"name": "Lucena Position", "category": "endgame",
     "description": "Winning technique with rook pawn and rook vs rook. The 'bridge-building' method secures promotion."},
    {"name": "Philidor Position", "category": "endgame",
     "description": "Drawing technique with rook vs rook and pawn. The defender keeps the rook on the third rank."},
    {"name": "Zugzwang", "category": "endgame",
     "description": "A position where any move worsens the position. Common in pawn endgames and a decisive winning method."},
    {"name": "Corresponding Squares", "category": "endgame",
     "description": "In pawn endgames, certain king positions correspond. Understanding them determines win vs draw."},
    {"name": "Square Rule", "category": "endgame",
     "description": "Method to determine if a king can catch a passed pawn: draw a square from the pawn to promotion, if the king is inside it can catch."},
    {"name": "Castling", "category": "rules",
     "description": "Special move with king and rook. Kingside (O-O) is most common. Cannot castle through check, out of check, or after moving either piece."},
    {"name": "En Passant", "category": "rules",
     "description": "Pawn capture of an enemy pawn that moved two squares as if it moved one. Only possible immediately after the two-square move."},
    {"name": "Pawn Promotion", "category": "rules",
     "description": "A pawn reaching the last rank promotes to queen, rook, bishop, or knight. Underpromotion to knight can be a brilliant tactic."},
    {"name": "Stalemate", "category": "rules",
     "description": "When the player to move has no legal moves and is not in check. Results in a draw. Important defensive resource."},
    {"name": "Draw by Repetition", "category": "rules",
     "description": "If the same position occurs three times, either player can claim a draw. Fivefold repetition is automatic draw."},
    {"name": "Fifty-Move Rule", "category": "rules",
     "description": "If 50 moves pass without pawn move or capture, the game is drawn. Important in endgames."},
]

FAMOUS_GAMES = [
    {"name": "The Immortal Game", "white": "Adolf Anderssen", "black": "Lionel Kieseritzky", "year": 1851,
     "description": "Anderssen sacrificed both rooks and the queen to deliver checkmate. Played in London, the epitome of romantic chess."},
    {"name": "The Evergreen Game", "white": "Adolf Anderssen", "black": "Jean Dufresne", "year": 1852,
     "description": "Famous for the stunning queen sacrifice 19.Rad1!! leading to a forced mate. A masterpiece of combination play."},
    {"name": "The Opera Game", "white": "Paul Morphy", "black": "Duke Karl and Count Isouard", "year": 1858,
     "description": "Morphy, playing against two consulters at the Paris Opera, demonstrated rapid development and sacrifice. A model of open-game principles."},
    {"name": "Kasparov vs Topalov, Wijk aan Zee 1999", "white": "Garry Kasparov", "black": "Veselin Topalov", "year": 1999,
     "description": "Kasparov's legendary rook sacrifice 24.Rxd4!! in a Pirc Defense. Voted one of the greatest games ever played."},
    {"name": "The Game of the Century", "white": "Donald Byrne", "black": "Bobby Fischer", "year": 1956,
     "description": "13-year-old Fischer's queen sacrifice 17...Be6!! stunned the chess world. Announced the arrival of a genius."},
    {"name": "Deep Blue vs Kasparov 1997 Game 6", "white": "Deep Blue", "black": "Garry Kasparov", "year": 1997,
     "description": "The computer's victory that changed history. Caro-Kann knight sacrifice led to Kasparov's resignation and match loss."},
    {"name": "Carlsen vs Anand, World Championship 2013 Game 5", "white": "Magnus Carlsen", "black": "Viswanathan Anand", "year": 2013,
     "description": "Carlsen's positional squeeze in the middlegame demonstrated his grinding style that won him the title."},
    {"name": "Fischer vs Spassky 1972 Game 6", "white": "Bobby Fischer", "black": "Boris Spassky", "year": 1972,
     "description": "Fischer's masterpiece in the Match of the Century. Spassky applauded. Perfect demonstration of the Tartakower QGD."},
]

WORLD_CHAMPIONS = [
    {"name": "Wilhelm Steinitz", "years": "1886-1894", "country": "Austria/United States",
     "description": "First official world champion. Founder of positional chess theory."},
    {"name": "Emanuel Lasker", "years": "1894-1921", "country": "Germany",
     "description": "Longest reign (27 years). Mathematician and philosopher of chess. Master of psychology."},
    {"name": "Jose Raul Capablanca", "years": "1921-1927", "country": "Cuba",
     "description": "The Chess Machine. Lost only 35 games in his career. Famous for effortless endgame technique."},
    {"name": "Alexander Alekhine", "years": "1927-1935, 1937-1946", "country": "Russia/France",
     "description": "Fierce attacker and brilliant tactician. Only champion to die holding the title."},
    {"name": "Max Euwe", "years": "1935-1937", "country": "Netherlands",
     "description": "Mathematician who defeated Alekhine. Later FIDE president."},
    {"name": "Mikhail Botvinnik", "years": "1948-1957, 1958-1960, 1961-1963", "country": "Soviet Union",
     "description": "The Patriarch of Soviet chess. Scientist who built the Soviet chess school."},
    {"name": "Vasily Smyslov", "years": "1957-1958", "country": "Soviet Union",
     "description": "Harmonious positional player and endgame master. Also an opera singer."},
    {"name": "Mikhail Tal", "years": "1960-1961", "country": "Soviet Union (Latvia)",
     "description": "The Magician from Riga. Dazzling sacrificial attacker. Youngest champion at the time."},
    {"name": "Tigran Petrosian", "years": "1963-1969", "country": "Soviet Union (Armenia)",
     "description": "Iron Tigran. Master of prophylaxis and defense. Extremely hard to beat."},
    {"name": "Boris Spassky", "years": "1969-1972", "country": "Soviet Union",
     "description": "Universal player. Lost the Match of the Century to Fischer in 1972."},
    {"name": "Bobby Fischer", "years": "1972-1975", "country": "United States",
     "description": "The lone American genius. 20 consecutive wins in 1970-71. Forfeited title in 1975."},
    {"name": "Anatoly Karpov", "years": "1975-1985", "country": "Soviet Union (Russia)",
     "description": "Positional boa constrictor. Dominated the late 70s with prophylactic mastery."},
    {"name": "Garry Kasparov", "years": "1985-2000", "country": "Soviet Union/Russia",
     "description": "The Beast of Baku. Highest rated player for 20 years. Peak rating 2851."},
    {"name": "Vladimir Kramnik", "years": "2000-2007", "country": "Russia",
     "description": "Ended Kasparov's reign with the Berlin Wall. Deep strategic understanding."},
    {"name": "Viswanathan Anand", "years": "2007-2013", "country": "India",
     "description": "The Tiger from Madras. Lightning-fast calculator. Five-time champion."},
    {"name": "Magnus Carlsen", "years": "2013-2023", "country": "Norway",
     "description": "Highest rated player ever (2882). Dominant in all formats. Abandoned classical title in 2023."},
    {"name": "Ding Liren", "years": "2023-2024", "country": "China",
     "description": "First Chinese world champion. Won 2023 title against Nepomniachtchi."},
    {"name": "Gukesh Dommaraju", "years": "2024-present", "country": "India",
     "description": "Youngest world champion ever (18). Won 2024 title against Ding Liren."},
]


def get_chess_openings() -> List[Dict[str, Any]]:
    documents = []
    for opening in CHESS_OPENINGS:
        content = f"""
Chess Opening: {opening['name']}
Moves: {opening['moves']}
ECO Code: {opening['eco']}
Description: {opening['description']}
""".strip()
        documents.append({
            "type": "opening",
            "name": opening['name'],
            "content": content,
            "metadata": {
                "name": opening['name'],
                "eco": opening['eco'],
                "moves": opening['moves'],
                "source": "curated_openings"
            }
        })
    return documents


def get_chess_concepts() -> List[Dict[str, Any]]:
    documents = []
    for concept in CHESS_CONCEPTS:
        content = f"""
Chess Concept: {concept['name']}
Category: {concept['category'].title()}
Description: {concept['description']}
""".strip()
        documents.append({
            "type": "concept",
            "name": concept['name'],
            "content": content,
            "metadata": {
                "name": concept['name'],
                "category": concept['category'],
                "source": "curated_concepts"
            }
        })
    return documents


def get_famous_games() -> List[Dict[str, Any]]:
    documents = []
    for game in FAMOUS_GAMES:
        content = f"""
Famous Chess Game: {game['name']}
White: {game['white']}
Black: {game['black']}
Year: {game['year']}
Description: {game['description']}
""".strip()
        documents.append({
            "type": "famous_game",
            "name": game['name'],
            "content": content,
            "metadata": {
                "name": game['name'],
                "white": game['white'],
                "black": game['black'],
                "year": game['year'],
                "source": "curated_famous_games"
            }
        })
    return documents


def get_world_champions() -> List[Dict[str, Any]]:
    documents = []
    for champ in WORLD_CHAMPIONS:
        content = f"""
World Chess Champion: {champ['name']}
Reign: {champ['years']}
Country: {champ['country']}
Description: {champ['description']}
""".strip()
        documents.append({
            "type": "champion",
            "name": champ['name'],
            "content": content,
            "metadata": {
                "name": champ['name'],
                "years": champ['years'],
                "country": champ['country'],
                "source": "curated_champions"
            }
        })
    return documents
