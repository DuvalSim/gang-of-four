export const parseRoomInfo = (roomInfo) => {
    return {
        players: roomInfo.users,
        roomLeader: roomInfo.leader,
        roomId: roomInfo.room_id
    }
};