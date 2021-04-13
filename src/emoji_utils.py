import random


def generate_emoji(num_emojis: int) -> str:
    """ Generates a psuedo-random list of emojis with pasta sprinkled in """
    emojis = ["🙄", "😙", "😐", "🤤", "😤", "😲",
              "😬", "😭", "🥵", "🥺", "🤠", "🤫", "😳", "😢"]
    output: str = ""
    for _ in range(num_emojis):
        output += random.choice(emojis) + "🍝"
    return output


def pastify_string(input_str):
    return "🍝 " + input_str + " 🍝"
