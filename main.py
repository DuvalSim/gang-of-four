from flask import Flask, render_template
import socketio
from room_manager import RoomManager
from socket_manager import SocketManager
from deck import Card, Hand
from room import Room

import logging

logger = None

# Create an ASGI Socket.IO server
sio = socketio.AsyncServer(cors_allowed_origins='*', async_mode = 'asgi')
app = socketio.ASGIApp(sio)

room_manager = RoomManager()
socket_manager = SocketManager()

# Handle client connection
@sio.on('connect')
async def connect(sid, environ):
    print(f'Client {sid} connected')

# Handle client disconnection
@sio.event
async def disconnect(sid):
    # Check if user was in a room:
    await room_manager.on_user_disconnect(sid, sio)
    
    
    print(f'Client {sid} disconnected')

@sio.on('room:reconnect')
async def reconnect(sid, data):

    try:

        client_id = data["user_id"]

        room_id = room_manager.get_room_from_user(user_id=client_id)
        
        if room_id is None:
            await sio.emit('room:reconnect', {"error": "No room"}, to=sid)
            return
        
        client_room = room_manager.active_rooms[room_id]
        player = client_room.get_player(client_id)

        reconnect_data = {
            "room_info": client_room.get_room_info(),
            "game_state" : client_room.current_game.get_status() if client_room.current_game is not None else None,
            "cards" : player.get_status()["cards"],
            "room_manager": client_room.room_manager_user_id
        }

        await sio.emit("room:reconnect", reconnect_data, to=sid)

        # updat user socket
        await sio.leave_room(sid=socket_manager.get_user_socket_id(client_id), room=room_id)
        socket_manager.update_user_socket(client_id, sid)
        await sio.enter_room(sid=sid, room=room_id)

    except Exception as e:
        await sio.emit('room:reconnect', {"error": "Could not reconnect:" + str(e)}, to=sid)
        raise
    

# Handle a move from a player
@sio.on('room:create')
async def create_room(sid, data):

    
    
    try:

        room_id = room_manager.create_room()
        username = data["username"]
        user_id = data["user_id"]
        
        room_manager.join_room(room_id=room_id, client_id=user_id, socket_id=sid, username= username)
        await sio.enter_room(sid=sid, room=room_id)

        response_data = room_manager.active_rooms[room_id].get_room_info()
        await sio.emit('room:create', response_data, sid)
        
    except Exception as e:
        print(f'Error while creating room: {e}')
        await sio.emit('room:create', {'error': str(e)}, sid)
    

@sio.on('room:join')
async def join_room(sid, data):

    room_id = data["room_id"]
    username = data["username"]
    user_id = data["user_id"]

    try:
        room_manager.join_room(room_id=room_id, client_id=user_id, socket_id=sid, username=username)
        await sio.enter_room(sid=sid, room=room_id)

        response_data = room_manager.active_rooms[room_id].get_room_info()
        await sio.emit('room:join', response_data, to=sid)

        await sio.emit('room:update', response_data, to=room_id, skip_sid=sid)

    except Exception as e:
        print(f'Error while joining room: {e}')
        await sio.emit('room:join', {'error': str(e)}, sid)
        return 


@sio.on('game:start')
async def start_game(sid, data):
    user_id = data["user_id"]
    
    try:
        room_id = room_manager.get_room_from_user(user_id)
        if room_id is None:
            raise ValueError("Not in room")
        current_room = room_manager[room_id]
        current_room.start_game(user_id)

    except Exception as e:
        print("Error:", str(e))
        await sio.emit('game:start', {'error': str(e)}, sid)
        raise
    
    await sio.emit('game:status', current_room.current_game.get_status(), room=room_id)

    for player in current_room.get_players():
        data = player.get_status()
        await sio.emit('game:cards', data, to=socket_manager.get_user_socket_id(player.client_id))

    print("Done starting game")

@sio.on('game:play')
async def play_game(sid, data):

    user_id = data["user_id"]

    room_id = data["room_id"]
    action = data["action"]
    cards_played = data["cards_played"]
    
    try:
        current_room = room_manager[room_id]
        current_hand = None
        if action == "play":
            current_hand = Hand.build_from_str(cards_played)
            current_room.current_game.play_turn(user_id, current_hand)
        else:
            current_room.current_game.play_turn(user_id, pass_turn=True)
    except Exception as e:
        print("Error:", str(e))
        await sio.emit('game:play', {'error': str(e)}, sid)
        raise
    
    play_data = {
        "player_play": user_id,
        "action": data["action"]}
    if action == "play":
        play_data["cards_played"] = [str(card) for card in current_hand.get_card_list()]  

    status_data = current_room.current_game.get_status()

    await sio.emit('game:play', play_data, room=room_id)

    if status_data.get("inter_round_info", None) is not None:
        for player in current_room.get_players():
            data = player.get_status()
            await sio.emit('game:cards', data, to=socket_manager.get_user_socket_id(player.client_id))   
    
    await sio.emit('game:status', status_data , room=room_id)


@sio.on('game:card_exchange')
async def card_exchange(sid, data):   
    
    room_id = data["room_id"]
    user_id = data["user_id"]
    card_to_exchange = data["card_to_give"]

    try:
        current_room = room_manager[room_id]
        winner_to_looser_card = Card.build_from_str(card_to_exchange)

        current_room.current_game.complete_card_exchanges(user_id, winner_to_looser_card)
    
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
            await sio.emit('game:cards', data, to=socket_manager.get_user_socket_id(player.client_id))

        await sio.emit('game:status', response_data, room=room_id)

def __is_authorized_user(user_id, sid) -> bool:
    expected_sid = socket_manager.get_user_socket_id(user_id)
    if expected_sid is None or (expected_sid != sid):
        return False
    else:
        return True
    
@sio.on('card:sort')
async def card_exchange(sid, data):   
     
    try:
        user_id = data["user_id"]
        sort_method = data["sort_method"]

        # Check that user is authorized
        if not __is_authorized_user(user_id, sid):
            raise ValueError("User not authorized")
        
        room_id = room_manager.get_room_from_user(user_id)
        player = room_manager.active_rooms[room_id].get_player(user_id)

        # return {"sort_order": "]"}
        
        sort_order = player.sort_cards(sort_method=sort_method)

        
        response_data = {
            "sort_order": sort_order
        }

        return response_data
    
    except Exception as e:
        print("Got error:", str(e))
        return {"error" : str(e)}
    

@sio.on('game:counter_last_card')
async def counter_last_card(sid, data):
    try:
        user_id = data["user_id"]

        # Check that user is authorized
        if not __is_authorized_user(user_id, sid):
            raise ValueError("User not authorized")
        
        room_id = room_manager.get_room_from_user(user_id)
        blocked_players_id = room_manager.active_rooms[room_id].current_game.counter_last_card(user_id)

        await sio.emit("game:counter_last_card", {"user_id": user_id, "blocked_players": blocked_players_id}, to=room_id)

        await __send_room_status(room_manager[room_id])
        
    
    except Exception as e:
        print("Got error:", str(e))
        return {"error" : str(e)}
    
    return {"status": "ok"}

@sio.on('game:call_last_card')
async def call_last_card(sid, data):
    try:
        user_id = data["user_id"]

        # Check that user is authorized
        if not __is_authorized_user(user_id, sid):
            raise ValueError("User not authorized")
        
        room_id = room_manager.get_room_from_user(user_id)
        room_manager.active_rooms[room_id].current_game.call_last_card(user_id)

        await sio.emit("game:call_last_card", {"user_id": user_id}, to=room_id)
        await sio.emit('game:status', room_manager.active_rooms[room_id].current_game.get_status(), room=room_id)
    
    except Exception as e:
        print("Got error:", str(e))
        return {"error" : str(e)}
    
    return {"status": "ok"}


async def __send_room_status(current_room: Room):

    room_id = current_room.room_id

    status_data = room_manager.active_rooms[room_id].current_game.get_status()
    if status_data.get("inter_round_info", None) is not None:
        for player in room_manager.active_rooms[room_id].get_players():
            data = player.get_status()
            await sio.emit('game:cards', data, to=socket_manager.get_user_socket_id(player.client_id))   

    await sio.emit('game:status', status_data , room=room_id)
    

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=5000, log_level="debug")
