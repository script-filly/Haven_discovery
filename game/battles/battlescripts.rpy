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
                        if each_party_member.cur_hp <= 0:
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

        # Show status of party members
        def show_status(self, xalign, yalign=0.78, anim_name=''):
            if anim_name is '':
                anim_name = 'idle50' if self.cur_hp <= 50 else 'idle100'
            who = self.name.lower()
            anim = '%s %s' % (who, anim_name)
            self.display(anim, xalign, yalign)

        def fainted(self):
            return (False if self.cur_hp > 0 else True)

    def heal(member, potions, healthcount):
        member.cur_hp = min(member.cur_hp+10, member.max_hp)
        potions -= 1
        healthcount += 10

    def check(members): # Check for win or lose conditions
        fainted = []
        for index in range(0, len(members)):
            member = members[index]
            if member.fainted():
                fainted.append(member.name)
        return (True if len(fainted) == len(members) else False)

label battle_game_2:
    hide screen inventory
    hide screen itemdisplay
    scene bg cave5

    # Allies and Enemies can be added via party_list.append(Member(...))
    $ party_list = [Member("Eebee", 100, healthcount, 3, 5), Member("Oleka", 100, olekahealth, 5, 6)]
    $ potions_left = 10
    $ players_turn = False
    $ enemies_list = [Member("SnAIke", 75, 75, 5, 12),] # TODO: Enemies will have descriptions

    show screen battle_screen

    $ party_list[0].show_status(0.05, 0.8)                  # Eebee
    $ party_list[1].show_status(-0.03, 0.78)                # Oleka
    $ enemies_list[0].display("snaike disabled", 0.93, 0.8) # SnAIke

    menu:
        "Malicious code dectected"
        "Help AI":
            play music "audio/music/suspended-battle.ogg"
    "Let the battle begin!"

## Main battle loop ##
    label battle_2_loop:

        python:
            while (not check(party_list) and not check(enemies_list)):
                # Ally's Turn
                for index in range(0, len(party_list)):
                    ally = party_list[index]
                    print(ally.name)
                    if ally.cur_hp <= 0:
                        continue # Skip turn

                    players_turn = True # Process player input
                    ally.show_status(0.3)
                    battle_narrator("%s, it\'s your turn now" % ally.name)

                    res = ui.interact()    # Get player input
                    players_turn = False   # Stop receiving inputs, and process the current action

                    if res == "heal":
                        heal(ally, potions_left, healthcount)
                        if ally.name == 'Eebee':
                            e("10hp restored")
                        elif ally.name == 'Oleka':
                            o("10hp restored")
                    else: # Attack
                        player_damage = renpy.random.randint( ally.min_dmg, ally.max_dmg)
                        enemies_list[res].cur_hp -= player_damage

                        if ally.cur_hp <= 0:
                            battle_narrator("Take this! (damage dealt - [%s]hp)" % player_damage)
                        else:
                            if ally.name == 'Eebee':
                                renpy.hide("Eebee disabled") # Show character's turn is consumed
                                ally.display("eebee fight", 0.05, 0.78)
                            elif ally.name == 'Oleka':
                                renpy.hide("Oleka disabled")
                                ally.display("oleka fight", -0.03, 0.8)
                            renpy.show("snaike hurt")
                            # renpy.call(renpy.random.choice(["etaunt1", "etaunt2", "etaunt3"]), from_current=True)

                        # Update global health counters
                        if (ally.name == 'Eebee'):
                            healthcount = ally.cur_hp
                        elif (ally.name == 'Oleka'):
                            olekahealth = ally.cur_hp

                        if ally.name == 'Eebee':
                            ally.show_status(0.05, 0.78)
                        elif ally.name == 'Oleka':
                            ally.show_status(-0.03, yalign=0.8)
                        if check(enemies_list):
                            break

                # Enemy's Turn
                for index in range(0, len(enemies_list)):
                    enemy = enemies_list[index]
                    if enemy.cur_hp < 0:
                        continue # Skip turn

                    ally = party_list[renpy.random.randint(0, (len(party_list)-1))]
                    enemy_dmg = renpy.random.randint(enemy.min_dmg, enemy.max_dmg)
                    ally.cur_hp -= enemy_dmg

                    if ally.cur_hp <= 0:
                        renpy.show('snaike fight')
                        ally.show_status(0.0, 0.78, 'ko')
                        battle_narrator('(%s continues to attack %s)!' % (enemy.name, ally.name))
                    else:
                        renpy.show('snaike fight')
                        if (ally.name == 'Eebee'):
                            ally.show_status(0.05, 0.78, 'hurt')
                        elif (ally.name == 'Oleka'):
                            ally.show_status(-0.03, 0.8, 'hurt')
                        battle_narrator('Rrrrr! (%s dealt %s hp damage to %s)' % (enemy.name, enemy_dmg, ally.name))

                        # Update global health counters
                        if ally.name == 'Eebee':
                            healthcount = ally.cur_hp
                        elif ally.name == 'Oleka':
                            olekahealth = ally.cur_hp

                    if ally.name == 'Eebee':
                        ally.show_status(0.05, 0.78)
                    elif ally.name == 'Oleka':
                        ally.show_status(-0.03, yalign=0.8)
                    if check(party_list):
                        break

            # In case all enemies are already defeated
            if check(party_list):
                renpy.jump("battle_2_lose")
            elif check(enemies_list):
                renpy.jump("battle_2_win")

# The results of the game.
label battle_2_win:
    show snaike death at Position(xpos=0.85, xanchor=0.5, ypos=0.9, yanchor=0.5)
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
