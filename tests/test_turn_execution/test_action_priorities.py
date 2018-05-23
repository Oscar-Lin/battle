from enum import Enum, auto


class ActionPriority(Enum):
    STAY = auto()
    GO = auto()
    ATTACK = auto()
    """
    write a bunch of priorities. the first step is brainstorming.
        - write descriptive ideas for what a bunch of priorities
        - ex:
            - go until first attack opportunity, always reserve pts for an attack, no matter what
            - go until first attack opportunity, make sure can get to minimum safe distance after attack.

    Write a SECOND list that is just an edited version of first list. cut out the ones you don't want
    for each element in second list, write several attempts at a short descriptive
    
    
    go until find a player                FIND HUNT
    go until someone hits                 ALARM ALERT NOTIFIED
    go until out of mvpts                 ALL_GO ONLY_GO
    go until sees player then turn back   SEEK SCOUT
    run to base                           RETREAT RETURN
    run to nearest teammate               BACKUP GET_HELP
    chase down running player             CHASE
    go towards danger                     EDGY RISKY BRAVE
    go towards opportunity                LUCKY PLAY_SAFE
    wait until enemy spotted              CAMP STILL WATCH
    wait until target in perimeter        STALK TRAP RADAR
    wait until max_hp                     REGEN HEAL GET_FULL
    wait until team arrives               HOLD WAIT GET_READY
    attack when teammates                 GANG GROUP COOPERATE
    attack when enemy spotted             OFFEND TRIGGER
    attack if they attack                 COPYCAT COPY
    drive by attack                       DRIVE_BY PASS_BY
    attack if max_hp                      FULL_ATTACK HP_ATTACK

    
    
    """
