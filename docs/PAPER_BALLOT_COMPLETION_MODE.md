# Paper Ballot Completion Mode

Version: 0.9.2-beta v2

## Purpose

Paper ballot completion mode supports participants who started QR voting but could not finish because they closed the site, lost connection, or their phone died.

## Rules

1. The back-of-windscreen QR code must be scanned first to activate the voter token.
2. The platform stores the voter token in the database and remembers it in the phone session/cookie for convenience.
3. Votes already submitted by QR/electronic voting are final for that class/place.
4. A paper ballot can be tied to the participant's car number.
5. Staff may enter only remaining missing class/place votes.
6. If staff enters a paper vote for a class/place already completed, the system skips it and keeps the earlier QR/electronic vote.
7. The database remains the source of truth. The cookie/session only helps the voter resume without rescanning.

## Staff Workflow

1. Admin opens Paper Ballot Entry.
2. Staff enters participant car number and clicks Load voting status.
3. System shows completed and missing class/place choices.
4. Staff enters only missing paper votes.
5. System validates that each selected car is registered in that class.
6. System counts valid missing votes and skips duplicates.

## CSV Workflow

CSV templates include participant_car_number. When imported, the same rules apply: prior votes win and duplicates are skipped.
