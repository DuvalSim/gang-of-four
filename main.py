from flask import Flask, render_template
import socketio
from room_manager import RoomManager
from deck import Card, Hand
from room import Room

import logging

logger = None

# Create an ASGI Socket.IO server
sio = socketio.AsyncServer(cors_allowed_origins='*', async_mode = 'asgi')
app = socketio.ASGIApp(sio)

room_manager = RoomManager()

# Handle client connection
@sio.event
async def connect(sid, environ):
    print(f'Client {sid} connected')
    await sio.emit('connect_ack', {"client_id": sid}, to=sid)

# Handle client disconnection
@sio.event
async def disconnect(sid):
    print(f'Client {sid} disconnected')

# Handle a move from a player
@sio.on('room:create')
async def create_room(sid, data):
    room_id = room_manager.create_room()
    
    
    try:
        room_manager.join_room(room_id=room_id, client_id=sid)
        await sio.enter_room(sid=sid, room=room_id)
        response_data = {"room_id": room_id}
        await sio.emit('room:create', response_data, sid)
    except Exception as e:
        print(f'Error while creating room: {e}')
        await sio.emit('room:create', {'error': str(e)}, sid)

    

@sio.on('room:join')
async def join_room(sid, data):

    room_id = data["room_id"]

    try:
        room_manager.join_room(room_id=room_id, client_id=sid)
        await sio.enter_room(sid=sid, room=room_id)
    except Exception as e:
        print(f'Error while joining room: {e}')
        await sio.emit('room:join', {'error': str(e)}, sid)
        return 

    await sio.emit('room:join', {"room_id": room_id, "players": room_manager.get_players(room_id)}, to=sid)

    await sio.emit('room:udpate', {"room_id": room_id, "players": room_manager.get_players(room_id)}, to=room_id)


@sio.on('game:start')
async def start_game(sid, data):
    room_id = data["room_id"]
    
    try:
        current_room = room_manager[room_id]
        current_room.start_game()        
    except Exception as e:
        print("Error:", str(e))
        await sio.emit('game:start', {'error': str(e)}, sid)
        raise
    
    await sio.emit('game:status', current_room.current_game.get_status(), room=room_id)

    for player in current_room.get_players():
        data = player.get_status()
        await sio.emit('game:cards', data, to=player.client_id)

    print("Done starting game")

@sio.on('game:play')
async def play_game(sid, data):


    room_id = data["room_id"]
    action = data["action"]
    cards_played = data["cards_played"]
    
    try:
        current_room = room_manager[room_id]
        current_hand = None
        if action == "play":
            current_hand = Hand.build_from_str(cards_played)
            current_room.current_game.play_turn(sid, current_hand)
        else:
            current_room.current_game.play_turn(sid, pass_turn=True)
    except Exception as e:
        print("Error:", str(e))
        await sio.emit('game:play', {'error': str(e)}, sid)
    
    play_data = {
        "player_play": sid,
        "action": data["action"]}
    if action == "play":
        play_data["cards_played"] = [str(card) for card in current_hand.get_card_list()]  

    status_data = current_room.current_game.get_status()

    await sio.emit('game:play', play_data, room=room_id)
    await sio.emit('game:status', status_data , room=room_id)

    print("Done handling play")
    

async def __send_room_status(current_room: Room):

    room_id = current_room.room_id

    await sio.emit('game:status', current_room.get_status(), room=room_id)

    for player in current_room.get_players():
        data = {"cards": [str(card) for card in player.get_cards_in_hand()]}
        await sio.emit('game:cards', data, to=player.client_id)
    




if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=5000, log_level="debug")
