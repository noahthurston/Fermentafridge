# fsm.py


# Class for regulating the humidifier using a finite-state machine
class HumidityFSM:
    def __init__(self, goalHumidity, minHumidity, maxHumidity, humidityPlug, verbose=False):
        self.currState = 1
        self.goalHumidity = goalHumidity
        self.minHumidity = minHumidity
        self.maxHumidity = maxHumidity
        self.verbose = verbose
        self.humidityPlug = humidityPlug

    def setParameters(self, goalHumidity=None, minHumidity=None, maxHumidity=None):
        self.goalHumidity = goalHumidity if goalHumidity != None else self.goalHumidity
        self.minHumidity = minHumidity if minHumidity != None else self.minHumidity
        self.maxHumidity = maxHumidity if maxHumidity != None else self.maxHumidity

    # use the sensor reading to update the FSM state
    def updateState(self, humidity):
        ### Update state using sensor data
        # if in idle state
        if(self.currState==1):
            if(humidity<self.minHumidity):
                self.currState=2
                if self.verbose:
                    print("HUMIDITY FSM: changing idle-state to humidifying-state")
            else:
                if self.verbose:
                    print("HUMIDITY FSM: remaining in idle-state")
        
        # if in humidifying state
        elif(self.currState==2):
            if(humidity>self.goalHumidity):
                self.currState=1
                if self.verbose:
                    print("HUMIDITY FSM: changing humidifying-state to idle-state")
            else:
                if self.verbose:
                    print("HUMIDITY FSM: remaining in humidifying-state")
        
        # else state not found
        else:
            print("ERROR: No humidity FSM state found.")
            raise SystemExit

        ### With the updated state, change what devices are on and off
        if(self.currState==2):
            # plug on
            self.humidityPlug.turnOn()
        else:
            # plug off
            self.humidityPlug.turnOff()

    def getState(self):
        return self.currState

    def setState(self, stateInt):
        self.currState = stateInt


#  Class for regulating the heater/cooler using a finite-state machine
class TemperatureFSM:
    def __init__(self, goalTemp, minTemp, temperaturePlug, verbose=False):
        self.currState = 1
        self.goalTemp = goalTemp
        self.minTemp = minTemp
        self.verbose = verbose
        self.temperaturePlug = temperaturePlug

    def setParameters(self, goalTemp=None, minTemp=None):
        self.goalTemp = goalTemp if goalTemp != None else self.goalTemp
        self.minTemp = minTemp if minTemp != None else self.minTemp


    # use the sensor reading to update the FSM state
    def updateState(self, probeTemp, ambientTemp):
        ### Update state using sensor data
        # if in idle state
        if(self.currState==1):
            if(ambientTemp<self.minTemp and probeTemp<self.goalTemp):
                self.currState=2
                if self.verbose:
                    print("TEMPERATURE FSM: changing idle-state to heat-state")
            else:
                if self.verbose:
                    print("TEMPERATURE FSM: remaining in idle-state")
        
        # if in heating state
        elif(self.currState==2):
            if(ambientTemp<self.minTemp and probeTemp<self.goalTemp):
                self.currState=2
                if self.verbose:
                    print("TEMPERATURE FSM: remaining in heat-state")
            else:
                self.currState=1
                if self.verbose:
                    print("TEMPERATURE FSM: changing heat-state to idle-state")

        
        # else state not found
        else:
            print("ERROR: No humidity FSM state found.")
            raise SystemExit


        ### With the updated state, change what devices are on and off
        if(self.currState==2):
            # plug on
            self.temperaturePlug.turnOn()
        else:
            # plug off
            self.temperaturePlug.turnOff()


    def getState(self):
        return self.currState

    def setState(self, stateInt):
        self.currState = stateInt
