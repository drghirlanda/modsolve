class design(list):
    '''An experimental design is a list of stimulus-response associations
    that specify what is trained.'''
    def __init__(self):
        '''When an experimental design is created, it has one empty phase
        representing the initial state of the experiment.'''
        super(design,self).append( {} )
        
    def append(self, newPhase):
        '''add phase to the design'''
        if design.checkArgument(self, newPhase):
            super(design, self).append(newPhase)
        else:
            print 'Error. Dictionary not added'
        
        
    def insert(self, index, newPhase):
        '''inserts phase into design'''
        if design.checkArgument(self, newPhase):
            super(design, self).insert(index, newPhase)
        else:
            print 'Error. Phase not added'
    
    def extend(self):
        '''add phases from list'''
        pass
    
    def len(self):
        return len(self)
    
    def checkArgument(self, newPhase):
        try:
            phase = dict(newPhase)
            keysList = phase.keys()
            valueList = phase.values();
            for i in keysList:
                element = str(i)
                if (element.isalpha()==False):
                    print "Stimulus have to be letters"
                    return False
            
            for i in valueList:
                elem = str(i)
                if(elem.isdigit()==False):
                    print "Response should be numeric"
                    return False
                
            return True
        except(NameError, TypeError, ValueError):
            print 'Invalid input. Should be dictionary'
    
    def printDesign(self):
        return str(self)
    
    def allStimuli(self):
        '''creates list of all stimulis in design'''
        stimuli = []
        for i in self:
            for j in i.keys():
                if j not in stimuli:
                    stimuli.append(j)
        return stimuli
    
    def values(self):
        '''create list of values for each stimuli'''
        val = []
        for i in self:
            val.extend(i.values())
        return val