# pyNLU

we will consider the following ADT for the representation of information:

### DEVICE
- deviceID (provides a unique identifier for the device)
- deviceReference (references can identify descriptors. We will used the following: light, owen, heating, door, ...)
- devicePlace (identifies the location in the environment: for instance: kitchen, bedroom, ...)
- deviceType (devices are classified taking into account their capabilities)
- deviceState (current state of the device - its structure and value depends on the deviceType)
- deviceProgram (this component will include an startProgram, an endProgram and a targetState)

We will concentrate on 2 types of Devices:

- deviceType: ON/OFF (they allow just two operations: turning it on or turning it off)
    - For instance, the light in the kitchen
- deviceType: Range (in this case the state can be described as a value in a range). In order to simplify the description, we will normalize all ranges to 0 - 100. 
    - For instance, the temperature of the owen, or the position of a blind: half raised can be expressed as state 50

Using this framework, we can define for instance an environment with the following devices:

Device

    deviceId: 1
    deviceReference: light
    devicePlace: kitchen
    deviceType: ON/OFF
    deviceState: OFF

Device

    deviceId: 2
    deviceReference: airConditioning
    devicePlace: diningRoom
    deviceType: Range
    deviceState: 0 [this means that currently this device is switched off]
    deviceProgram:
        startProgram: 2015/06/19/15:00
        endProgram: 2015/06/19/16:00
        targetState: 22

In this last case, if we assume that the state of the airConditioning can represent the desired temperature, we are stating that the device is currently switched off and we have programmed its activation at 3pm of today (19th of June) during an hour, with a desired temperature of 22 degrees.

In this case we will not cover cases where we have several devices with the same reference and place (like 2 lights in the kitchen). So, in fact, every device can be uniquely identified by the deviceId or the pair (deviceReference, devicePlace). From now on, each type we use deviceId, it is interchangeable by (deviceReference,devicePlace).

Although it is not a requirement for this assignment, you can simulate this functionality creating a class Device with several objets instantiated.

The basic funcionality we will demand to this class is:

    state <- getState(deviceId)
    boolean <- setState(deviceId, deviceState)
    boolean <- setProgram(deviceId, startProgram, endProgram, targetState)

This two last methods will return false in case of different errors: the deviceId doesn't exist, the program or the state cannot be assigned taking into account the deviceType ...

So, now we concentrate on the goal of the assignment. As I said, let's suppose we have this environment. The goal is to create an NLU interface.

In order to achieve that, we have to create a Feature-Structure based Grammar, able to understand and create semantic representation for the following type of sentences:

    Turn on the kitchen light.

In this case the representation, should be a FS (Feature Structure) with the following values:

    [ deviceOperation: setState ]
    [ deviceReference: light    ]
    [ devicePlace    : kitchen  ]
    [ deviceState    : 100      ]

That is, we need to incorporate an additional parameter or feature that will identify the type of operation we are asking the system to accomplish.

    How is the bedroom door ?

    [ deviceOperation: getState ]
    [ deviceReference: door     ]
    [ devicePlace    : bedroom  ]

    Please set on the air conditioning at 6pm at 25 degrees.


    [deviceOperation: setState                        ]
    [deviceReference: airConditioning                 ]
    [deviceProgram  : [ startProgram: [ hour: 18 ] ]  ]
    [                 [ targetState : 25           ]  ] 


In this last case we haven't identified the place of the device, so it is unespecified in the FS. Additionally, the data structures for dates can contain the features minute, hour, day, month, year. We will instantiate as much information as the input incorporates.