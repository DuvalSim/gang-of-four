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
@sio.on('connect')
async def connect(sid, environ):
    print(f'Client {sid} connected')

# Handle client disconnection
@sio.event
async def disconnect(sid):
    print(f'Client {sid} disconnected')

# Handle a move from a player
@sio.on('room:create')
async def create_room(sid, data):

    room_id = room_manager.create_room()
    username = data["username"]
    user_id = data["user_id"]
    
    try:
        room_manager.join_room(room_id=room_id, client_id=user_id, username= username)
        await sio.enter_room(sid=sid, room=room_id)

        response_data = {"room_id": room_id, "players": room_manager.get_players_info(room_id)}
        await sio.emit('room:create', response_data, sid)
        
    except Exception as e:
        print(f'Error while creating room: {e}')
        await sio.emit('room:create', {'error': str(e)}, sid)

    print('send')

    

@sio.on('room:join')
async def join_room(sid, data):

    room_id = data["room_id"]
    username = data["username"]

    try:
        room_manager.join_room(room_id=room_id, client_id=sid, username=username)
        await sio.enter_room(sid=sid, room=room_id)

        response_data = {"room_id": room_id, "players": room_manager.get_players_info(room_id)}
        await sio.emit('room:join', response_data, to=sid)

        await sio.emit('room:update', response_data, to=room_id, skip_sid=sid)

    except Exception as e:
        print(f'Error while joining room: {e}')
        await sio.emit('room:join', {'error': str(e)}, sid)
        return 


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
        raise
    
    play_data = {
        "player_play": sid,
        "action": data["action"]}
    if action == "play":
        play_data["cards_played"] = [str(card) for card in current_hand.get_card_list()]  

    status_data = current_room.current_game.get_status()

    await sio.emit('game:play', play_data, room=room_id)

    if status_data.get("inter_round_info", None) is not None:
        for player in current_room.get_players():
            data = player.get_status()
            await sio.emit('game:cards', data, to=player.client_id)   
    
    await sio.emit('game:status', status_data , room=room_id)


@sio.on('game:card_exchange')
async def card_exchange(sid, data):   
    
    room_id = data["room_id"]
    card_to_exchange = data["card_to_give"]
    client_id = data["client_id"]

    try:
        current_room = room_manager[room_id]
        winner_to_looser_card = Card.build_from_str(card_to_exchange)

        current_room.current_game.complete_card_exchanges(client_id, winner_to_looser_card)
    
    except Exception as e:
        print("Error:", str(e))
        await sio.emit('game:card_exchange', {'error': str(e)}, sid)
        raise

    else:
        # card_exchange_data = {"winner": sid, "looser": current_room.current_game.last_round_looser.client_id ,"winner_to_looser_card": card_to_exchange}

        card_exchange_data = current_room.current_game.get_card_exchange_info()
        response_data = current_room.current_game.get_status()
        response_data["card_exchange_info"] = card_exchange_data

        # Send cards to looser and winner:
        for player in [current_room.get_player(card_exchange_data["last_looser"]), current_room.get_player(card_exchange_data["last_winner"])]:
            data = player.get_status()
            await sio.emit('game:cards', data, to=player.client_id)

        await sio.emit('game:status', response_data, room=room_id)



async def __send_room_status(current_room: Room):

    room_id = current_room.room_id

    await sio.emit('game:status', current_room.get_status(), room=room_id)

    for player in current_room.get_players():
        data = {"cards": [str(card) for card in player.get_cards_in_hand()]}
        await sio.emit('game:cards', data, to=player.client_id)
    




if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=5000, log_level="debug")
