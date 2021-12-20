import json

data = json.load(open('input.json', 'r'))
current_state = set(data['current_state'])
goal_state = set(data['goal_state'])
stack = []
action_queue = []


class Stack:
    @staticmethod
    def push(x):
        stack.append(x)

    @staticmethod
    def pop():
        return stack.pop()

    @staticmethod
    def top():
        return stack[-1]


def achieve_on_xy(stat):
    tokens = stat.split()
    action = "__STACK__ {} {}".format(tokens[1], tokens[2])
    Stack.push(action)


def achieve_armempty():
    for stat in current_state:
        tokens = stat.split()
        if "HOLDING" in stat:
            action = "__PUTDOWN__ {}".format(tokens[1])
            Stack.push(action)
            break


def achieve_clear_x(stat):
    tokens = stat.split()
    x = tokens[1]
    for stat in current_state:
        tokens = stat.split()
        if 'HOLDING' in tokens and tokens[1] == x:
            action = "__PUTDOWN__ {}".format(x)
            Stack.push(action)
            return
        if 'ON' in tokens and tokens[2] == x:
            x = tokens[1]
            y = tokens[2]
            action = "__UNSTACK__ {} {}".format(x, y)
            Stack.push(action)
            return


def achieve_holding_x(stat):
    tokens = stat.split()
    x = tokens[1]
    for stat in current_state:
        tokens = stat.split()
        if 'TABLE' in tokens and tokens[1] == x:
            action = "__PICKUP__ {}".format(x)
            Stack.push(action)
            return
        if 'ON' in tokens and tokens[1] == x:
            y = tokens[2]
            action = "__UNSTACK__ {} {}".format(x, y)
            Stack.push(action)
            return


def try_putdown_x(stat):
    tokens = stat.split()
    x = tokens[1]
    possible = True

    conditions = [
        "HOLDING {}".format(x)
    ]
    for condition in conditions:
        if condition not in current_state:
            Stack.push(condition)
            possible = False

    if possible:
        for condition in conditions:
            current_state.remove(condition)

        actions = [
            "TABLE {}".format(x),
            "CLEAR {}".format(x),
            "ARMEMPTY"
        ]
        for action in actions:
            current_state.add(action)

        Stack.pop()
        action_queue.append(stat)


def try_pickup_x(stat):
    tokens = stat.split()
    x = tokens[1]
    possible = True

    conditions = [
        "ARMEMPTY",
        "TABLE {}".format(x),
        "CLEAR {}".format(x),
    ]
    for condition in conditions:
        if condition not in current_state:
            Stack.push(condition)
            possible = False

    if possible:
        for condition in conditions:
            current_state.remove(condition)

        actions = [
            "HOLDING {}".format(x)
        ]
        for action in actions:
            current_state.add(action)

        Stack.pop()
        action_queue.append(stat)


def try_unstack_xy(stat):
    tokens = stat.split()
    x = tokens[1]
    y = tokens[2]
    possible = True

    conditions = [
        "ARMEMPTY",
        "ON {} {}".format(x, y),
        "CLEAR {}".format(x),
    ]
    for condition in conditions:
        if condition not in current_state:
            Stack.push(condition)
            possible = False

    if possible:
        for condition in conditions:
            current_state.remove(condition)

        actions = [
            "HOLDING {}".format(x),
            "CLEAR {}".format(y)
        ]
        for action in actions:
            current_state.add(action)

        Stack.pop()
        action_queue.append(stat)


def try_stack_xy(stat):
    tokens = stat.split()
    x = tokens[1]
    y = tokens[2]
    possible = True

    conditions = [
        "HOLDING {}".format(x),
        "CLEAR {}".format(y),
    ]
    for condition in conditions:
        if condition not in current_state:
            Stack.push(condition)
            possible = False

    if possible:
        for condition in conditions:
            current_state.remove(condition)

        actions = [
            "ARMEMPTY",
            "ON {} {}".format(x, y),
            "CLEAR {}".format(x)
        ]
        for action in actions:
            current_state.add(action)

        Stack.pop()
        action_queue.append(stat)


if __name__ == '__main__':
    while goal_state != current_state:
        stack = [stat for stat in goal_state if stat not in current_state]
        while stack:
            print('actions:', action_queue)
            print('current state:', current_state)
            print('stack:', stack)
            print()

            stat = Stack.pop()

            if "ON" in stat:
                if stat in current_state:
                    pass
                else:
                    achieve_on_xy(stat)

            if "CLEAR" in stat:
                if stat in current_state:
                    pass
                else:
                    achieve_clear_x(stat)

            if "ARMEMPTY" in stat:
                if stat in current_state:
                    pass
                else:
                    achieve_armempty()

            if "HOLDING" in stat:
                if stat in current_state:
                    pass
                else:
                    achieve_holding_x(stat)

            if "__UNSTACK__" in stat:
                Stack.push(stat)
                try_unstack_xy(stat)

            if "__STACK__" in stat:
                Stack.push(stat)
                try_stack_xy(stat)

            if "__PICKUP__" in stat:
                Stack.push(stat)
                try_pickup_x(stat)

            if "__PUTDOWN__" in stat:
                Stack.push(stat)
                try_putdown_x(stat)

    print('actions:', action_queue)
    print('current state:', current_state)
    print('stack:', stack)

    json.dump(action_queue, open('output.json', 'w'), indent=2)