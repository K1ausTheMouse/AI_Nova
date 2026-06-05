![Status](https://img.shields.io/badge/status-planning-blue)
![Python](https://img.shields.io/badge/python-3.x-yellow)
![Project](https://img.shields.io/badge/project-AI%20Assistant-purple)

# First GitHub Project
I previously worked on a similar project with an AI called from GROQ API into a Raspberry Pi. The system was able to communicate through speakers, a microphone, and the terminal...
However, due to a lack of planning and experience, The AI was given too much freedom and it ended up stress-testing its environment by generating large amounts of unusable files.
From that, I learned the importance of control, structure, and planning. This project is a more careful and thought-out attempt at building a similar system. :)


## Nova AI Concept

Nova is a personal project idea for a local AI assistant with memory and interaction capabilities.

## Goal
To build a basic system that can store information, respond to input, and improve interactions over time.

## Core Features
- Take user input (text, voice, touch, image)
- Store important information as memory
- Recall memory when needed
- Generate responses using an AI model
- Handle voice and sensor input


## System Design

### Memory Structure
Planned database tables:
- entities(people, AI's or objects)
- memories
- interactions
- environment

## Development Plan

### Stage 1
- Create database
- Store simple text memory
- Retrieve memory
- Connect AI model

### Stage 2
- Automatically save important information
- Search memory
- Improve responses using stored data

### Stage 3
- Voice input (speech → text)
- Voice output (text → speech)

### Stage 4
- Add sensors (touch)
- Detect input intensity
- Store sensor events
- React to touch

## Future Ideas
- App to control Nova's memory; delete or edit
- Camera input
- More advanced memory system
- More natural,fast responses
- Full physical system
- Human body


## What has been done.

- Designed and implemented an SQLite database in Python, including linked tables and foreign key relationships for AI memory management.


## Notes
Currently in planning and early prototyping stage.


## TODO

### Memory 
- Change log / audit trail
- Who changed it
- Old value
- New value
- Timestamp

### Enterity

### Enviromrnt

### Interaction
