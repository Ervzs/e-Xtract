#test
from experta import Fact, KnowledgeEngine, Rule, DefFacts, W

class Device(Fact):
    pass

class DismantlingStep(Fact):
    pass

class DismantlingProcessProvider(KnowledgeEngine):
    @DefFacts()
    def initial_facts(self):
        yield Device(model="Unknown")

    @Rule(Device(model="Xiaomi-9"))
    def xiaomi_9_process(self):
        self.declare(DismantlingStep(step=1, action="Remove the tray", description="Use the ejection tool (aka Needle) or Paperclip. Push the tip all the way into the hole until the tray ejects, and then pull the tray of SIM and Memory card (Micro SD) out. ⚠️ Pay attention! The tool must be inserted into a hole on the edge of the phone's housing. Do not press too hard. It may break the tray eject mechanism."))
        self.declare(DismantlingStep(step=2, action="Open the back cover", description="We recommend using a special heating device such as a separator machine, heat gun, or heating mat. It will simplify the process. You can use a home hairdryer, but you will have to make a nozzle by hand or have a suitable one in the kit to gently heat and concentrate the heat flow in the right place. ℹ️️ The surface of the back cover must be heated to soften the adhesive underneath. The approximate heating temperature is 50° C / 125° F. Use a thin plastic film or pick for separation. To facilitate the process, you can use isopropyl alcohol. It is often most difficult to pass the tool between the parts to be divided. Choose the far edge from the FFC cables or buttons. Do not use a lever or any force for separation that could damage the elements inside."))
        self.declare(DismantlingStep(step=3, action="Unscrew the screws", description="Using a screwdriver (Phillips 1.5 mm PH000), unscrew 10 screws."))
        self.declare(DismantlingStep(step=4, action="Open the cover", description="Remove the cover with an NFC tag and antennas that protect the printed circuit board (PCB). Try to lift the covers by the edges and not push anything between them to not accidentally touch or short-circuit anything on the PCB."))
        self.declare(DismantlingStep(step=5, action="Disconnect the battery", description="Disconnect the battery from the motherboard connector."))
        self.declare(DismantlingStep(step=6, action="Remove the battery", description="Carefully remove the battery. It is glued to the case. You can use a thin plastic card or pick to separate it."))
        self.declare(DismantlingStep(step=7, action="Unscrew the screws (2pcs)", description="Unscrew the two screws securing the motherboard."))
        self.declare(DismantlingStep(step=8, action="Remove the motherboard cover", description="Carefully remove the plastic cover that protects the motherboard connectors."))
        self.declare(DismantlingStep(step=9, action="Disconnect the front camera", description="Disconnect the front camera connector from the motherboard."))
        self.declare(DismantlingStep(step=10, action="Remove the front camera", description="Carefully remove the front camera module."))
        self.declare(DismantlingStep(step=11, action="Disconnect the screen connector", description="Disconnect the display connector from the motherboard."))
        self.declare(DismantlingStep(step=12, action="Disconnect the touch screen connector", description="Disconnect the touchscreen connector from the motherboard."))
        self.declare(DismantlingStep(step=13, action="Disconnect other connectors", description="Disconnect any remaining connectors on the motherboard (e.g., for the side buttons)."))
        self.declare(DismantlingStep(step=14, action="Remove the motherboard", description="Carefully remove the motherboard from the phone case."))
        self.declare(DismantlingStep(step=15, action="Unscrew the screws (2pcs)", description="Unscrew the two screws securing the charging board."))
        self.declare(DismantlingStep(step=16, action="Disconnect the coaxial cable", description="Disconnect the coaxial cable from the charging board."))
        self.declare(DismantlingStep(step=17, action="Disconnect the charging port connector", description="Disconnect the charging port connector from the charging board."))
        self.declare(DismantlingStep(step=18, action="Remove the charging board", description="Carefully remove the charging board."))
        self.declare(DismantlingStep(step=19, action="Remove the earpiece speaker", description="Remove the earpiece speaker module."))
        self.declare(DismantlingStep(step=20, action="Remove the vibrator", description="Remove the vibrator motor."))
        self.declare(DismantlingStep(step=21, action="Remove the side buttons", description="Remove the side button assembly."))
        self.declare(DismantlingStep(step=22, action="Remove the loudspeaker", description="Remove the loudspeaker module."))
        self.declare(DismantlingStep(step=23, action="Remove the proximity sensor", description="Remove the proximity sensor module."))
        self.declare(DismantlingStep(step=24, action="Remove the display", description="Carefully remove the display assembly. This step often requires heating and specialized tools."))


engine = DismantlingProcessProvider()
engine.reset()

device_model = input("Enter device model: ")
engine.declare(Device(model=device_model))

engine.run()

for step in engine.facts.values():
    if isinstance(step, DismantlingStep):
        print(f"Step {step['step']}: {step['action']}")
        print(f"  Description: {step['description']}")
        print("-" * 20)
    else: 
        print("No steps found")
        break