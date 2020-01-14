from generation.GenUtils import *

class Training(Event):
    def interest_flags():
        return [I_ACTIVE]

    def roles():
        pass

    def start():
        pass

    def end():
        pass

class HuntingTrip(Event):
    def interest_flags():
        return [I_ACTIVE]

    def roles():
        roles_required = [Hunter]
        roles_optional = [Hunter for i in range(7)]
        return roles_required, roles_optional

    def start():
        pass

    def end():
        pass

    class Hunter(Role):
        def __init__(self, c):
            super().__init__()

        def can_assign(character):
            if character.age > 15:
                return True
            return False

        def name():
            return "Hunter"
