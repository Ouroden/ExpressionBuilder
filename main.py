from ExpressionBuilder import ExpressionBuilder


def main():
    builder = ExpressionBuilder()

    commands = [
        "dodaj dwadziescia jeden i tysiac piecset siedemnascie",
        "dodaj tysiac jeden do milion",
        "do jedenascie dodaj zero",
        "dwa plus minus trzy",
        "odejmij siedem od sto",
        "piec odjac dwa",
        "od piec odejmij jeden",
        "pomnoz sto siedemdziesiat i minus dziewiec",
        "pomnoz cztery przez zero",
        "siedem razy osiem",
        "podziel dwa i cztery",
        "podziel jeden przez piec",
        "osiem dzielone przez trzy",
        "pierwiastek z siedemnascie",
        "dwa do kwadratu",
        "osiemdziesiat trzy do potegi minus jeden",
        "kwadrat ze sto",
        "sto czterdziesci trzy tryliony dwiescie dwadziescia bilionow milion dwa tysiace czterdziesci dwa do potegi minus sto jedenascie"
    ]

    for command in commands:
        print("\ncommand:    ", command)
        print("expression: ", builder.getExpressionFromPlanText(command))


if __name__ == '__main__':
    main()
