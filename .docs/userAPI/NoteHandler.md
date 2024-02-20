## Note State Machine

A diagram that demonstrates the state machine which describes the possible states and transitions involved in intaking, transferring, and shooting a note. The diagram is written in [mermaid syntax](https://mermaid.js.org/syntax/stateDiagram.html). It will display prettier when viewed in GitHub.

```mermaid
stateDiagram-v2
	[*] --> Idle
	Idle --> Intaking: Intake triggered
	Intaking --> EnterTransfer: Note enters transfer
	Intaking --> Idle: Cancel intake
	EnterTransfer --> ExitTransfer: Note Exits Transfer
	ExitTransfer --> ReadyToShoot: Note in right spot
	ExitTransfer --> TransferAdjustReverse: Note needs adjusting
	TransferAdjustReverse --> ReadyToShoot: Note in right spot
	ReadyToShoot --> PreppingShooter: Shooter triggered
	PreppingShooter --> Shooting: Shooter up to speed
	Shooting --> Idle: Note shot
```