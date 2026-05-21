import app
import math
from events.input import Buttons, BUTTON_TYPES

try:
    import imu
except ImportError:
    imu = None

try:
    from tildagonos import tildagonos
except ImportError:
    tildagonos = None


class EmfQuest(app.App):
    def __init__(self):
        self.button_states = Buttons(self)

        self.nodes = {

            # ── ARRIVAL ──────────────────────────────────────────────────
            0: (
                "You arrive at EMFCamp.\n"
                "Badges blink. Lasers sweep\n"
                "the sky. RGB everywhere.\n"
                "Doom floppy under your arm.\n"
                "Time to trade.",
                [("Head to the swap shop", 1),
                 ("Check the info tent first", 20)]
            ),

            # ── INFO TENT ────────────────────────────────────────────────
            20: (
                "The info tent volunteer\n"
                "squints at your floppy.\n"
                "'Rumour: radioactive cylinder\n"
                "in the swap shop.\n"
                "Could be interesting.'",
                [("Go to the swap shop", 1),
                 ("Ask about workshops", 21)]
            ),
            21: (
                "Workshop board lists:\n"
                "- Tesla Coil Tuning (Tent 7)\n"
                "- Lock-picking 101 (Tent 3)\n"
                "- Soldering: Mods (Tent 12)\n"
                "You file it away for later.",
                [("Go to the swap shop", 1),
                 ("Visit Tesla Coil workshop", 30)]
            ),

            # ── TESLA COIL WORKSHOP ──────────────────────────────────────
            30: (
                "Tent 7 smells of ozone.\n"
                "A tesla coil SCREAMS arcs\n"
                "of purple lightning.\n"
                "A volunteer hands you\n"
                "ear defenders.",
                [("Watch and learn", 31),
                 ("Nope. Swap shop.", 1)]
            ),
            31: (
                "You learn that strong EM\n"
                "fields can scramble\n"
                "radiation sensors.\n"
                "Useful, maybe.\n"
                "You pocket the fact.",
                [("Go to the swap shop", 1)]
            ),

            # ── SWAP SHOP ────────────────────────────────────────────────
            1: (
                "Inside the swap shop:\n"
                "A radioactive black cylinder\n"
                "sits on a velvet cushion.\n"
                "It hums faintly. It PULSES.\n"
                "What do you do?",
                [("Offer the floppy disk for it", 2),
                 ("Examine it closely first", 10),
                 ("Ask about it", 11)]
            ),
            10: (
                "Stamped: DO NOT OPEN\n"
                "MOD CLEARANCE REQUIRED.\n"
                "It vibrates. Shopkeeper\n"
                "watches you sweat.",
                [("Offer the floppy disk for it", 2),
                 ("Ask about it", 11),
                 ("Just a tiny peek inside...", 102),
                 ("Walk away", 0)]
            ),
            11: (
                "Shopkeeper: 'Found it in\n"
                "a skip outside Harwell.\n"
                "Seems fine. Well. Mostly.\n"
                "Eyes stopped watering\n"
                "after the first day.'",
                [("Offer the floppy disk for it", 2),
                 ("Hard pass. Leave.", 0)]
            ),
            2: (
                "Deal struck! You hand over\n"
                "Doom. The cylinder is YOURS.\n"
                "It hums. It pulses.\n"
                "Then - a shriek from\n"
                "the entrance.",
                [("Look toward the shriek", 3)]
            ),

            # ── THE FURRY STRIKES ────────────────────────────────────────
            3: (
                "A furry in a full fox suit\n"
                "SNATCHES the cylinder!\n"
                "'IT MUST BE MADE SAFE!'\n"
                "they howl, vanishing\n"
                "into the crowd.",
                [("Chase them immediately", 4),
                 ("Ask shopkeeper which way", 12),
                 ("Stand there stunned", 13)]
            ),
            12: (
                "Shopkeeper points toward\n"
                "Null sector.\n"
                "'Went that-a-way. Fast.\n"
                "Also, you're glowing.\n"
                "Might want to jog.'",
                [("Chase into Null sector", 5)]
            ),
            13: (
                "You stand there 45 seconds.\n"
                "The cylinder is long gone.\n"
                "Shopkeeper taps counter.\n"
                "'You still owe me\n"
                "a Doom disk.'",
                [("Chase toward Null sector", 5),
                 ("Go to info tent for help", 20)]
            ),
            4: (
                "You run through the crowd.\n"
                "Badges beep in alarm.\n"
                "Someone spills Club Mate\n"
                "on your shoes.\n"
                "Fox-tail vanishes left.",
                [("Follow left to Null sector", 5),
                 ("Cut right past workshops", 40)]
            ),

            # ── SHORTCUT VIA WORKSHOPS ───────────────────────────────────
            40: (
                "You barrel past Tent 7.\n"
                "The tesla coil SCREAMS.\n"
                "You remember the EM trick.\n"
                "Ahead: furry hits a gate.",
                [("Cut them off at the gate", 41),
                 ("Follow to Null sector", 5)]
            ),
            41: (
                "You block the gate!\n"
                "Furry skids to a halt.\n"
                "'I just want to make\n"
                "it safe!' they pant,\n"
                "clutching the cylinder.",
                [("Negotiate calmly", 42),
                 ("Grab it back by force", 43)]
            ),
            42: (
                "'Safe HOW?' you ask.\n"
                "The furry blinks.\n"
                "'...I hadn't actually\n"
                "planned that far ahead.'\n"
                "The cylinder hums.",
                [("Suggest info tent together", 44),
                 ("Just take it back", 43)]
            ),
            43: (
                "You grab. They pull.\n"
                "The cylinder pops open.\n"
                "A burst of green light.\n"
                "Everyone within 10m\n"
                "turns teal.",
                [("Slam it shut and run", 60),
                 ("Apologise to teal people", 45)]
            ),
            44: (
                "You both go to the info tent.\n"
                "Volunteer rings the MOD.\n"
                "Cylinder collected safely.\n"
                "Traded AND returned!\n"
                "GOOD END: Responsible Trader.",
                []
            ),
            45: (
                "The teal people are chill.\n"
                "One says: 'Honestly this\n"
                "matches my badge.'\n"
                "The furry legs it.\n"
                "Cylinder gone.",
                [("Chase to Null sector", 5)]
            ),

            # ── NULL SECTOR ──────────────────────────────────────────────
            5: (
                "NULL SECTOR.\n"
                "Bass throbs. RGB strobes\n"
                "dissolve the dark.\n"
                "Lasers carve green lines.\n"
                "Where is the furry?",
                [("Ask the DJ booth", 50),
                 ("Check the chill-out corner", 51),
                 ("Head to Robot Arms", 6)]
            ),
            50: (
                "DJ is World of Techno:\n"
                "a small wheeled robot\n"
                "covered in stickers,\n"
                "pumping out 140bpm.\n"
                "It spins toward you.",
                [("Ask if they saw the furry", 52),
                 ("Ask for a slower track", 53),
                 ("Back away slowly", 5)]
            ),
            52: (
                "World of Techno responds:\n"
                "*BWEE BOOP DWEE WAAAH*\n"
                "It extends a small\n"
                "sticky antenna toward\n"
                "the chill-out corner.",
                [("Go to the chill-out corner", 51)]
            ),
            53: (
                "World of Techno responds:\n"
                "*BWWWAAAP*\n"
                "It does not play\n"
                "a slower track.\n"
                "It plays 180bpm.",
                [("Retreat to chill-out corner", 51),
                 ("Dance anyway", 54)]
            ),
            54: (
                "You dance. You're good.\n"
                "A crowd forms.\n"
                "Someone hands you\n"
                "a Club Mate.\n"
                "A beautiful 20 minutes.",
                [("Snap out of it. Find furry.", 51)]
            ),
            51: (
                "In the corner, a fox-eared\n"
                "head pokes above a beanbag.\n"
                "The cylinder sits between\n"
                "their paws.\n"
                "They look sheepish.",
                [("Confront them", 55),
                 ("Sneak up and grab it", 56),
                 ("Sit down and talk first", 57)]
            ),
            55: (
                "'WHY did you take it?!'\n"
                "Furry: 'I thought it leaked!\n"
                "I panicked! I'm a\n"
                "materials science PhD!\n"
                "I KNOW things!'",
                [("That's fair. Talk.", 57),
                 ("Ask for it back anyway", 58)]
            ),
            56: (
                "You lunge. Furry yelps.\n"
                "Cylinder skitters across\n"
                "the floor, vanishes\n"
                "under the decks.\n"
                "World of Techno: *BWAAAP*",
                [("Crawl under the decks", 59),
                 ("Give up. Robot Arms.", 6)]
            ),
            57: (
                "They explain: possibly\n"
                "Cs-137. They have a\n"
                "Geiger counter in their bag.\n"
                "It's clicking. Quite a lot.",
                [("Ask them to help return it", 65),
                 ("Take it, run to info tent", 66),
                 ("Robot Arms for a think", 6)]
            ),
            58: (
                "Furry hands it over, ears\n"
                "flat. 'Please be careful.\n"
                "It's not a toy.'\n"
                "Slightly guilty.\n"
                "Slightly irradiated.",
                [("Go to Robot Arms to regroup", 6),
                 ("Head straight home", 80)]
            ),
            59: (
                "Under the decks: cables,\n"
                "dust, one lost boot,\n"
                "and the cylinder.\n"
                "World of Techno rolls over\n"
                "and peers down. *bwee?*",
                [("Grab the cylinder", 60),
                 ("Ask World of Techno", 61)]
            ),
            61: (
                "World of Techno reverses,\n"
                "hooks the cylinder with\n"
                "a tiny claw arm and\n"
                "nudges it to you.\n"
                "*BOOP*. Solemnly done.",
                [("Thank the robot and leave", 60)]
            ),
            60: (
                "Cylinder in hand.\n"
                "It's warm. Very warm.\n"
                "The Geiger counter clicks\n"
                "in your memory.",
                [("Go to Robot Arms", 6),
                 ("Go straight to info tent", 66),
                 ("Head for the exit", 80)]
            ),

            # ── FURRY + GEIGER ───────────────────────────────────────────
            65: (
                "Together you walk to\n"
                "the info tent.\n"
                "Volunteer goes pale.\n"
                "Makes a call. Then another.\n"
                "A van arrives in an hour.",
                [("Wait and cooperate", 90)]
            ),
            66: (
                "You jog to the info tent,\n"
                "cylinder under one arm.\n"
                "Three people scatter\n"
                "as you pass.\n"
                "Possibly the Geiger noise.",
                [("Report it to the volunteer", 90)]
            ),

            # ── INFO TENT (LATE GAME) ────────────────────────────────────
            90: (
                "Volunteer: 'Right.\n"
                "Don't move. Don't open it.\n"
                "Don't sneeze.'\n"
                "Foil blanket. Then:\n"
                "A MOD van at the gate.",
                [("Cooperate fully", 91),
                 ("Ask to keep the disk", 92)]
            ),
            91: (
                "MOD officers take it.\n"
                "Nod gravely. Clipboard.\n"
                "'Thank you for your\n"
                "cooperation.'\n"
                "GOOD END: Civic Duty.",
                []
            ),
            92: (
                "Officer stares. Long pause.\n"
                "'The floppy disk of...Doom.'\n"
                "They bag it. 'Evidence.'\n"
                "You get a receipt.\n"
                "GOOD END: At least safe.",
                []
            ),

            # ── ROBOT ARMS ───────────────────────────────────────────────
            6: (
                "ROBOT ARMS PUB.\n"
                "Warm light. Smell of chips.\n"
                "World of Techno is here,\n"
                "parked by the bar.",
                [("Talk to World of Techno", 70),
                 ("Talk to the bartender", 71),
                 ("Talk to the stranger", 72),
                 ("Leave and head home", 80)]
            ),
            70: (
                "World of Techno has a straw\n"
                "taped to its chassis,\n"
                "dipped in a Club Mate.\n"
                "It wheels to face you.\n"
                "*bwee bwee boop waaah bwee*",
                [("Nod sagely", 73),
                 ("Ask bartender to translate", 74)]
            ),
            73: (
                "World of Techno clicks.\n"
                "*boop*\n"
                "You feel understood.\n"
                "It spins to face the exit\n"
                "and rolls meaningfully.",
                [("Head to info tent", 66),
                 ("Head home with cylinder", 80),
                 ("Bribe it with stickers", 100)]
            ),
            74: (
                "Bartender: 'No idea.\n"
                "Been saying that all night.\n"
                "Whatever it means,\n"
                "loads of people nodded\n"
                "and left.'",
                [("Follow the crowd's example", 66),
                 ("Order a drink and think", 71)]
            ),
            71: (
                "Bartender slides Club Mate.\n"
                "'You look like you've had\n"
                "a day. That thing on the\n"
                "table makes my watch\n"
                "run backwards, FYI.'",
                [("Ask who to call", 75),
                 ("Finish drink. Head out.", 80)]
            ),
            75: (
                "'MOD have a site liaison.\n"
                "Laminated sheet by the door.\n"
                "Apparently this happens\n"
                "more than you'd think.'",
                [("Find the sheet and call", 66)]
            ),
            72: (
                "The stranger in the corner:\n"
                "wiry, MOD lanyard,\n"
                "Geiger counter on their belt.\n"
                "Watching you very carefully.",
                [("Approach them", 76),
                 ("Pretend not to notice", 77)]
            ),
            76: (
                "MOD liaison:\n"
                "'I've been looking for\n"
                "that cylinder since Tuesday.\n"
                "Do NOT open it.\n"
                "Walk with me.'",
                [("Go with them", 91)]
            ),
            77: (
                "They stand up anyway.\n"
                "'Yeah, we need to talk.\n"
                "That's a Cs-137 source.\n"
                "I've been on-site\n"
                "three days.'",
                [("Comply immediately", 91),
                 ("Bolt for exit with it", 80)]
            ),

            # ── HOME STRETCH ─────────────────────────────────────────────
            80: (
                "You make it to the car park.\n"
                "Cylinder hums in your bag.\n"
                "Phone battery: 3%.\n"
                "The motorway stretches ahead.",
                [("Drive home", 81),
                 ("Call MOD hotline first", 82)]
            ),
            81: (
                "You drive home.\n"
                "The cylinder on the\n"
                "passenger seat.\n"
                "The radio keeps cutting out.",
                [("Arrive home. Go to bed.", 83),
                 ("Stop at services. Ring MOD.", 82),
                 ("Stop at services. Greggs.", 101)]
            ),
            82: (
                "You ring the MOD hotline.\n"
                "Hold music: 4 minutes.\n"
                "Then: 'Is this about\n"
                "a cylinder? We've had\n"
                "fourteen calls today.'",
                [("Yes. Yes it is.", 84)]
            ),
            83: (
                "You go to bed.\n"
                "6am: knock at the door.\n"
                "Three MOD officers in\n"
                "hazmat suits. A van.\n"
                "The neighbours are filming.",
                [("Open the door", 84)]
            ),
            84: (
                "The MOD take the cylinder.\n"
                "Officer finds your Doom disk.\n"
                "'Is this yours?' You nod.\n"
                "They bag it. 'Evidence.'\n"
                "You get a foil blanket.",
                [("Accept blanket. Cooperate.", 85)]
            ),
            85: (
                "Six weeks later: a letter.\n"
                "'Cylinder: decommissioned.\n"
                "Disk: returned (enclosed).'\n"
                "The Doom disk is inside.\n"
                "GOOD END: The Full Journey.",
                []
            ),

            # ── BAD ENDS ─────────────────────────────────────────────────
            99: (
                "BAD END.\n"
                "You are slightly radioactive.\n"
                "Badge blinks error codes.\n"
                "The cylinder is gone.\n"
                "The furry got away.",
                [("Start again", 0)]
            ),
            100: (
                "BAD END: Ratted Out.\n"
                "World of Techno rolls to\n"
                "the MOD liaison and beeps.\n"
                "Liaison: robot. You. Bag.\n"
                "Escorted out. No cylinder.\n"
                "No Doom disk. A letter.\n"
                "WoT: *bwee*",
                [("Start again", 0)]
            ),
            101: (
                "BAD END: Lost at Services.\n"
                "You stop at Membury.\n"
                "Set cylinder on the table.\n"
                "Get distracted by Greggs.\n"
                "Cylinder is gone.\n"
                "A child glows on the M4.\n"
                "You eat Greggs in silence.",
                [("Start again", 0)]
            ),
            102: (
                "BAD END: You Opened It.\n"
                "Just a little peek.\n"
                "It was not a little peek.\n"
                "Hair: different colour.\n"
                "Badge reads ERROR.\n"
                "Swap shop cordoned off.\n"
                "You owe the shopkeeper.",
                [("Start again", 0)]
            ),
        }

        self.stack = [0]
        self.selected_index = 0

    # ------------------------------------------------------------------ #
    def _get_options(self, node_id):
        """Return options list, appending Back if not at root."""
        options = list(self.nodes[node_id][1])
        if len(self.stack) > 1:
            options.append(("< Back", "back"))
        return options

    def _is_end_node(self, node_id):
        return len(self.nodes[node_id][1]) == 0

    # ------------------------------------------------------------------ #
    def update(self, delta):
        if self.button_states.get(BUTTON_TYPES["CANCEL"]):
            self.button_states.clear()
            self.minimise()
            return

        current_id = self.stack[-1]
        options = self._get_options(current_id)

        if self.button_states.get(BUTTON_TYPES["UP"]):
            self.button_states.clear()
            if self.selected_index > 0:
                self.selected_index -= 1
        elif self.button_states.get(BUTTON_TYPES["DOWN"]):
            self.button_states.clear()
            if self.selected_index < len(options) - 1:
                self.selected_index += 1
        elif self.button_states.get(BUTTON_TYPES["CONFIRM"]):
            self.button_states.clear()
            if self._is_end_node(current_id):
                self.minimise()
                return
            chosen = options[self.selected_index]
            if chosen[1] == "back":
                self.stack.pop()
                self.selected_index = 0
            else:
                self.stack.append(chosen[1])
                self.selected_index = 0

    # ------------------------------------------------------------------ #
    def draw(self, ctx):
        # Background
        ctx.save()
        ctx.rgb(0.05, 0.18, 0.05).rectangle(-120, -120, 240, 240).fill()
        ctx.restore()

        ctx.save()

        current_id = self.stack[-1]
        description, _ = self.nodes[current_id]
        options = self._get_options(current_id)
        is_end = self._is_end_node(current_id)

        desc_lines = description.splitlines()
        n_opts = 1 if is_end else len(options)

        font_size = 16
        line_h = font_size + 4   # 20
        opt_h  = font_size + 5   # 21
        sep_h  = font_size + 3   # 19
        total_h = (len(desc_lines) * line_h) + sep_h + (n_opts * opt_h)

        ctx.font_size = font_size
        # +font_size for baseline offset, +10 to shift content down into circle
        y = (-total_h // 2) + font_size + 10

        # ── Description ────────────────────────────────────────────────
        for line in desc_lines:
            if line.startswith("BAD END"):
                ctx.rgb(1.0, 0.2, 0.2)
            elif line.startswith("GOOD END: The Full Journey"):
                ctx.rgb(0.2, 1.0, 0.2)
            elif line.startswith("GOOD END"):
                ctx.rgb(1.0, 0.9, 0.0)
            else:
                ctx.rgb(0.9, 0.9, 0.9)
            w = ctx.text_width(line)
            ctx.move_to(-w / 2.0, y).text(line)
            y += line_h

        # ── Separator ──────────────────────────────────────────────────
        ctx.rgb(0.3, 0.3, 0.3)
        ctx.move_to(-95, y + 2)
        ctx.line_to(95, y + 2)
        ctx.stroke()
        y += sep_h

        # ── Options ────────────────────────────────────────────────────
        if is_end:
            ctx.rgb(0.4, 1.0, 0.4)
            label = "[CONFIRM to exit]"
            w = ctx.text_width(label)
            ctx.move_to(-w / 2.0, y).text(label)
        else:
            for idx, (label, _) in enumerate(options):
                if idx == self.selected_index:
                    ctx.save()
                    ctx.rgb(0.0, 0.3, 0.1).rectangle(
                        -95, y - font_size, 190, font_size + 3).fill()
                    ctx.restore()
                    ctx.rgb(0.2, 1.0, 0.4)
                else:
                    ctx.rgb(0.8, 0.8, 0.8)
                w = ctx.text_width(label)
                ctx.move_to(-w / 2.0, y).text(label)
                y += opt_h

        ctx.restore()


__app_export__ = EmfQuest
