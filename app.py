import csv
import json
import shutil
from tempfile import NamedTemporaryFile
from flask import Flask, make_response, jsonify, request

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "Pokemon DB!"


def _get_next_id():
    with open('pokemon.csv', newline='') as csvfile:
        pokereader = csv.DictReader(csvfile)
        max = 0
        for row in pokereader:
            if(int(row["#"]) > max):
                max = int(row["#"])

        return max + 1


def get_pokemon(pokemon_id):
    with open('pokemon.csv', 'r+', newline='') as csvfile:
        pokereader = csv.DictReader(csvfile)
        for row in pokereader:
            # print(int(row["#"]),pokemon_id)
            if(row["#"] == pokemon_id):
                return row


@app.route("/api/pokemon/<pokemon_id>", methods=['GET'])
def read_pokemon(pokemon_id):
    out = jsonify(get_pokemon(pokemon_id))
    return out


@app.route("/api/pokemon", methods=['POST'])
def create_pokemon():
    if request.is_json:
        result_id=""
        with open('pokemon.csv', 'a+', newline='') as csvfile:
            fieldnames = ["#", "Attack", "Defense", "Generation", "HP", "Legendary", "Name", "Sp. Atk", "Sp. Def", "Total", "Type 1", "Type 2"]
            pokewriter = csv.DictWriter(csvfile, fieldnames)
            pokemon = request.get_json()
            result_id = _get_next_id()
            pokewriter.writerow({ '#': result_id,
                'Attack': pokemon["Attack"],
                'Defense': pokemon["Defense"],
                'Generation': pokemon["Generation"],
                'HP': pokemon["HP"],
                'Legendary': pokemon["Legendary"],
                'Name': pokemon["Name"],
                'Sp. Atk': pokemon["Sp. Atk"],
                'Sp. Def': pokemon["Sp. Def"],
                'Total': pokemon["Total"],
                'Type 1': pokemon["Type 1"],
                'Type 2': pokemon["Type 2"]
                })

    return jsonify({ "pokemon_id": result_id})


@app.route("/api/pokemon/<pokemon_id>", methods=['PUT'])
def update_pokemon(pokemon_id):
    if request.is_json:
        pokemon = request.get_json()
        fieldnames = ["#", "Attack", "Defense", "Generation", "HP", "Legendary", "Name", "Sp. Atk", "Sp. Def", "Speed", "Total", "Type 1", "Type 2"]
        tempfile = NamedTemporaryFile(mode='w', delete=False)
        with open('pokemon.csv', 'r+', newline='') as csvfile, tempfile:
            pokereader = csv.DictReader(csvfile, fieldnames)
            pokewriter = csv.DictWriter(tempfile, fieldnames)
            for row in pokereader:
                newrow = {
                        "#": row['#'],
                        'Attack': row["Attack"],
                        'Defense': row["Defense"],
                        'Generation': row["Generation"],
                        'HP': row["HP"],
                        'Legendary': row["Legendary"],
                        'Name': row["Name"],
                        'Sp. Atk': row["Sp. Atk"],
                        'Sp. Def': row["Sp. Def"],
                        'Speed': row["Speed"],
                        'Total': row["Total"],
                        'Type 1': row["Type 1"],
                        'Type 2': row["Type 2"]
                        } 

                if(row["#"] == pokemon_id):
                    newrow = {
                        "#": pokemon_id,
                        'Attack': pokemon["Attack"],
                        'Defense': pokemon["Defense"],
                        'Generation': pokemon["Generation"],
                        'HP': pokemon["HP"],
                        'Legendary': pokemon["Legendary"],
                        'Name': pokemon["Name"],
                        'Sp. Atk': pokemon["Sp. Atk"],
                        'Sp. Def': pokemon["Sp. Def"],
                        'Speed': pokemon["Speed"],
                        'Total': pokemon["Total"],
                        'Type 1': pokemon["Type 1"],
                        'Type 2': pokemon["Type 2"]
                        }

                pokewriter.writerow(newrow)

            shutil.move(tempfile.name, 'pokemon.csv')

        return "Pokemon updated"


@app.route("/api/pokemon/<pokemon_id>", methods=['DELETE'])
def delete_pokemon(pokemon_id):
    fieldnames = ["#", "Attack", "Defense", "Generation", "HP", "Legendary", "Name", "Sp. Atk", "Sp. Def", "Speed", "Total", "Type 1", "Type 2"]
    tempfile = NamedTemporaryFile(mode='w', delete=False)
    with open('pokemon.csv', 'r+', newline='') as csvfile, tempfile:
        pokereader = csv.DictReader(csvfile, fieldnames)
        pokewriter = csv.DictWriter(tempfile, fieldnames)
        for row in pokereader:
            if(row["#"] != pokemon_id):
                pokewriter.writerow({
                    "#": row['#'],
                    'Attack': row["Attack"],
                    'Defense': row["Defense"],
                    'Generation': row["Generation"],
                    'HP': row["HP"],
                    'Legendary': row["Legendary"],
                    'Name': row["Name"],
                    'Sp. Atk': row["Sp. Atk"],
                    'Sp. Def': row["Sp. Def"],
                    'Speed': row["Speed"],
                    'Total': row["Total"],
                    'Type 1': row["Type 1"],
                    'Type 2': row["Type 2"]
                    })

        shutil.move(tempfile.name, 'pokemon.csv')

    return "Pokemon deleted"


@app.route("/api/pokemon/list/<offset>/<limit>", methods=['GET'])
def paginate_pokemons(offset, limit):
    with open('pokemon.csv', newline='') as csvfile:
        pokereader = csv.DictReader(csvfile)
        counter = 1
        array = []
        max = int(offset) + int(limit)
        for row in pokereader:
            counter = counter + 1
            if int(offset) <= counter and counter < max:
                array.append(row)

    return jsonify(array)


@app.route("/api/pokemon/list/all", methods=['GET'])
def list_pokemons():
    with open('pokemon.csv', newline='') as csvfile:
        pokereader = csv.DictReader(csvfile)
        out = jsonify([ row for row in pokereader])

    return out
