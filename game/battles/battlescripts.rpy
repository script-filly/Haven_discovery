define battle_narrator = Character(None, interact=False)
screen battle_screen:
    vbox:
        xalign 0.01 yalign 0.1
        spacing 5
        
        for each_party_member in party_list:
            frame:
                size_group "party"
                xminimum 250 xmaximum 250
                yminimum 75
                vbox:
                    $ party_member_name = each_party_member.name
                    text "[party_member_name]" size 22 xalign 0.5
                    null height 5
                    hbox:
                        bar:
                            xmaximum 130
                            value each_party_member.cur_hp
                            range each_party_member.max_hp
                            left_gutter 0
                            right_gutter 0
                            thumb None
                            thumb_shadow None
                            left_bar Frame("gui/barfull.png", 10, 0)
                            right_bar Frame("gui/barempy.png", 10, 0)
                        null width 5
                        if each_party_member.cur_hp <=0:
                         text "KO'd" size 16
                        else:
                         $ ally_cur_hp = each_party_member.cur_hp
                         $ ally_max_hp = each_party_member.max_hp
                         text "[ally_cur_hp] / [ally_max_hp]" size 16
        
        hbox:
            frame:
                size_group "party"
                yminimum 40
                text "Medipacks [potions_left]" yalign 0.0 xalign 0.5 size 22
            if players_turn and potions_left > 0:
                textbutton "<- Use" action Return("heal") yminimum 30
            else:
                textbutton "<- Use" action None yminimum 30
        
    vbox:
        xalign 0.90 yalign 0.1
        spacing 5
        
        if enemies_list != []:
            for i, each_enemy_member in enumerate(enemies_list):
                hbox:
                    if players_turn and each_enemy_member.cur_hp > 0:
                        textbutton "Attack ->" action Return(i) yminimum 75
                    else:
                        textbutton "Attack ->" action None yminimum 75
                    
                    frame:
                        size_group "enemies"
                        xminimum 250 xmaximum 250
                        yminimum 75
                        vbox:
                            $ enemy_name = each_enemy_member.name
                            text "[enemy_name]" size 22 xalign 0.5
                            null height 5   
                            hbox:
                                bar:
                                    xmaximum 130
                                    value each_enemy_member.cur_hp
                                    range each_enemy_member.max_hp
                                    left_gutter 0
                                    right_gutter 0
                                    thumb None
                                    thumb_shadow None
                                    left_bar Frame("gui/barfull.png", 10, 0)
                                    right_bar Frame("gui/barempy.png", 10, 0) 
                                null width 5
                                $ enemy_cur_hp = each_enemy_member.cur_hp
                                $ enemy_max_hp = each_enemy_member.max_hp
                                text "[enemy_cur_hp] / [enemy_max_hp]" size 16
 
init python:
    class Member:
        def __init__(self, name, max_hp, cur_hp, min_dmg, max_dmg):
            self.name = name
            self.max_hp = max_hp
            self.cur_hp = cur_hp
            self.min_dmg = min_dmg
            self.max_dmg = max_dmg

        def display(self, anim, xalign=0.05, yalign=0.8):
            pos = Position(xalign=xalign, yalign=yalign)
            trans = Dissolve(0.5)
            renpy.show(anim, at_list=[pos])
            renpy.with_statement(trans)

        def show_status(self, xalign, yalign=0.78, anim_name=''):
            if anim_name is '':
                anim_name = 'idle50' if self.cur_hp <= 50 else 'idle100'
            who = self.name.lower()
            anim = '%s %s' % (who, anim_name)
            self.display(anim, xalign, yalign)

        def fainted(self):
            result = False if self.cur_hp > 0 else True
            return result
            # result = False
            # if self.cur_hp > 0:
                # result = False
            # else:
                # result = True
            # return result


    def heal(member, potions, healthcount):
        member.cur_hp = min(member.cur_hp+10, member.max_hp)
        potions -= 1
        healthcount += 10

    # Checks for win or lose conditions
    def check(members):
        fainted = [""]
        # fainted = []
        # fainted.pop(0)
        # for member in members:
        for index in range(0, len(members)):
            member = members[index]
            if member.fainted():
                # fainted += member.name
                # fainted.append(str(member.name))
                fainted.append(member.name)
        fainted.pop(0)
        if (len(fainted) == len(members)):
            return True
        else:
            return False


label battle_game_2:
    hide screen inventory
    hide screen itemdisplay

    $ party_list = [Member("Eebee", 100, healthcount, 3, 5)]
    $ potions_left = 10
    $ players_turn = False
    $ enemies_list = [] # Enemies list will have the description for enemies.

    show screen battle_screen

   ##Load in eebee health graphics##
    if healthcount <=50:
        show eebee idle50 at Position (xalign = 0.05, yalign = 0.8) with dissolve
    elif healthcount >=51:
        show eebee idle100 at Position (xalign = 0.05, yalign = 0.8) with dissolve
 
   ##Load in oleka health graphics##
    if olekahealth <=50:
        show oleka idle50 at Position (xalign = -0.03, yalign = 0.78) with dissolve
    elif olekahealth >=51:
        show oleka idle100 at Position (xalign = -0.03, yalign = 0.78) with dissolve
    
    show snaike disabled  at Position (xalign = 0.93, yalign = 0.8) with dissolve
## We can add some allies to the party:##
    menu:
        "Malicious code dectected"
        "Help AI":
            $ party_list.append (Member("Oleka", 100, olekahealth, 5, 6))
            play music "audio/music/suspended-battle.ogg"

## Enemies party can be set manually or automatically like:##
            $ enemies_list.append ( {"name":"SnAIke", "max_hp":75, "current_hp":75, "min_damage":5, "max_damage":12} )          
    "Let the battle begin!"

## Main battle loop ##
    label battle_2_loop:

## At first let's check if player's party is ok.##
        if check_party(party_list) == "lost":
            jump battle_2_lose     
        elif check_party(enemies_list) == 'lost':
            jump battle_2_win

        python:
            # Check for lose
            fainted_party = []
            for ally in party_list:
                if ally.fainted():
                    fainted_party + ally.name
            if (fainted_party == len(party_list)):
                renpy.jump('battle_2_lose')

            for ally in party_list:
                if ally.cur_hp < 0:
                    continue # Skip turn
                else: # Process player input
                    players_turn = True
                    ally.show_status(0.3)

                    battle_narrator("%s, it\'s your turn now" % ally.name)

                    res = ui.interact()    # Get player input
                    players_turn = False   # Stop receiving inputs, and process the current action

                    if res == "heal":
                        ally.heal(potions_left, healthcount)
                        if ally.name == 'Eebee':
                            e("10hp restored")
                        elif ally.name == 'Oleka':
                            o("10hp restored")
                    else: # Attack
                        player_damage = renpy.random.randint( ally.min_dmg, ally.max_dmg )
                        enemies_list[res]["current_hp"] -= player_damage

                        if ally.cur_hp <= 0:
                            renpy.say(None, "Take this! (damage dealt - [%s]hp)" % player_damage)
                        else:
                            if ally.name == 'Eebee':
                                renpy.hide("Eebee") # Show character's turn is consumed
                                ally.display(0.05)
                            else:
                                renpy.hide("oleka")
                                ally.display(-0.03, 0.8)
                            renpy.show("snaike hurt")
                            renpy.call("expression", renpy.random.choice(["etaunt1", "etaunt2", "etaunt3"]))

                    ally.show_status() # Show status of party members
        ## Enemy Turn

        if check_party(enemies_list) == "lost": ## At first let's check if enemy's party is ok.##
            hide snaike fight
            jump battle_2_win

        ## All the party members will do their actions one after another.
        $ enemy_index = 0
        
        while enemy_index < len(enemies_list):
            $ current_enemy = enemies_list[enemy_index]
            
            ## Current enemy will act only if he is still alive.
            
            if current_enemy["current_hp"] > 0:
                
                ## Let's check if player's party is still ok.
                if check_party(party_list) == "lost":
                    jump battle_2_lose

                ## Enemy will attack the random player.
                $ party_member_to_attack = party_list[renpy.random.randint( 0, (len(party_list)-1) )]
                $ enemy_damage = renpy.random.randint( current_enemy["min_damage"], current_enemy["max_damage"] )
                $ party_member_to_attack["current_hp"] -= enemy_damage

                ##Eebees Hit##
                if party_member_to_attack["name"] == "Eebee":
                 if party_member_to_attack["current_hp"] <= 0:
                  show snaike fight
                  show eebee ko at Position (xalign = 0.0, yalign = 0.78) with dissolve
                  "([current_enemy[name]] continues to attack [party_member_to_attack[name]])!"
                  $ healthcount = 1
                 else:
                  show snaike fight
                  show eebee hurt at Position (xalign = 0.05, yalign = 0.78) with dissolve
                  "Rrrrr! ([current_enemy[name]] dealt [enemy_damage]hp damage to [party_member_to_attack[name]])"
                  $ healthcount -= enemy_damage
                ##Oleka Hit##
                elif party_member_to_attack["name"] == "Oleka":
                 if party_member_to_attack["current_hp"] <= 0:
                  show snaike fight
                  show oleka hurt at Position (xalign = -0.03, yalign = 0.8) with dissolve
                  "([current_enemy[name]] continues to attack [party_member_to_attack[name]])!"
                  $ olekahealth = 1
                 else:
                  show snaike fight
                  show oleka hurt at Position (xalign = -0.03, yalign = 0.8) with dissolve
                  $ olekahealth -= enemy_damage
                  "Rrrrr! ([current_enemy[name]] dealt [enemy_damage]hp damage to [party_member_to_attack[name]])"  

            ## And the turn goes to the next party member.
            $ enemy_index += 1
        ## Next round of the battle.
    if healthcount <=50:
        show eebee idle50 at Position (xalign = 0.3, yalign = 0.78) with dissolve
    elif healthcount >=51:
        show eebee idle100 at Position (xalign = 0.3, yalign = 0.78) with dissolve

    if olekahealth <=50:
        show oleka idle50 at Position (xalign = -0.03, yalign = 0.8) with dissolve
    elif olekahealth >=51:
        show oleka idle100 at Position (xalign = -0.03, yalign = 0.8) with dissolve
    jump battle_2_loop

## The results of the game.

label battle_2_win:
    show snaike death at Position (xpos=0.85, xanchor=0.5, ypos=0.9, yanchor=0.5) 
    "Well done!"
    hide snaike death
    $ cryptocount += 35
    "+35 Crypto's found"
    $ inv.append("cube")
    "+1 Artifact found"
    pause
    hide screen battle_screen
    return
    
label battle_2_lose:
    "X_X"
    hide screen battle_screen
    return
