__author__ = 'pascalpoizat'

from NamedElement import NamedElement


class App (NamedElement) :
    """
    Application built over bricks.

    """

    def __init__(self, name, states=[], bricks=[]) :
        """
        Constructor.

        :param name: String, the name of the application
        :param states: List[State], states of the application with the first one being the initial state
        :param bricks: List[Brick], bricks over which the application operates
        :return:
        """
        NamedElement.__init__(self, name)
        self.states = states
        self.bricks = bricks

    def __repr__(self):
        """
        External representation: Arduino program

        :return: String
        """

        rtr = ""
        rtr = rtr + "// generated by ArduinoML\n";
        rtr = rtr + "\nvoid setup() {\n";
        rtr = rtr + "\n".join(map(lambda b: b.setup(), self.bricks))
        rtr = rtr + "\n}\n";
        rtr = rtr + "\nvoid loop() { state_%s(); }\n" % self.states[0].name
        for state in self.states:
            rtr = rtr + "\nvoid state_%s() {\n" % state.name
            # generate code for state actions
            for action in state.actions:
                rtr = rtr + "\tdigitalWrite(%d, %s);\n" % (action.actuator.pin, action.value)
            # generate code for the transition
            transition = state.transition
            rtr += "\tif (digitalRead(%d) == %s) { state_%s(); }\n" \
                   % (transition.sensor.pin, transition.value, transition.nextstate.name)
            # loop over state
            rtr = rtr + "\tstate_%s();" % state.name
            # end of state
            rtr = rtr + "\n};\n";
        # end
        return rtr;
