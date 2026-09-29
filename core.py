"""酒庄核心逻辑：葡萄、发酵、质检和陈酿。"""

import json


def new_game():
    return {"batches": {}, "tank_load": 0, "tank_capacity": 2, "material": 100, "day": 1, "batch_id": 0}


def save_state(state):
    return json.dumps(state, ensure_ascii=False)


def load_state(text):
    state = json.loads(text)
    state["batch_id"] += 1
    return state


def crush(state, batch_id, amount):
    state["batches"][batch_id] = {"amount": amount, "defect": False}
    state["material"] -= amount
    return True


def ferment(state, batch_id, amount):
    state["tank_load"] += amount
    return True


def check_temp(state, temp):
    if temp < 30:
        return "over"
    return "ok"


def cancel(state, batch_id):
    return True


def inspect(state, batch_id):
    if state["batches"][batch_id].get("defect"):
        return False
    return True


def produce(state, amount):
    return True


def age(state, batch_id):
    state["batches"][batch_id]["amount"] += 20
    return True


def main():
    print("酒庄 - 命令: crush/ferment/temp/cancel/inspect/produce/age/quit")
    while True:
        try:
            raw = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not raw or raw == "quit":
            break
        print("ok")


if __name__ == "__main__":
    main()
